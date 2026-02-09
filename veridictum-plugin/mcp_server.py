#!/usr/bin/env python3
"""
Veridictum MCP Server - Citation Verification for Claude Cowork

Provides legal citation verification tools directly within Claude
conversations via the Model Context Protocol (MCP).

Tools:
  - verify_citation: Verify a single legal citation
  - verify_bulk_citations: Verify multiple citations at once
  - search_cases: Search for legal cases by topic or keyword
  - check_hallucinations: Check a legal document for hallucinated citations

Requires: pip install mcp httpx
"""

import os
import json
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

VERIDICTUM_API_URL = os.environ.get("VERIDICTUM_API_URL", "https://veridictum.legal")
VERIDICTUM_API_KEY = os.environ.get("VERIDICTUM_API_KEY", "")

server = Server("veridictum")


def get_headers():
    """Return authorization headers for Veridictum API."""
    headers = {"Content-Type": "application/json"}
    if VERIDICTUM_API_KEY:
        headers["Authorization"] = f"Bearer {VERIDICTUM_API_KEY}"
    return headers


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="verify_citation",
            description=(
                "Verify a single legal citation against Veridictum's database of "
                "14.2 million real court cases. Returns verification status, case name, "
                "court, date decided, and CourtListener URL. Use this BEFORE citing any "
                "case in legal writing to ensure it is real."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "citation": {
                        "type": "string",
                        "description": "Legal citation in Bluebook format (e.g., '384 U.S. 436' or 'Miranda v. Arizona, 384 U.S. 436 (1966)')"
                    }
                },
                "required": ["citation"]
            }
        ),
        Tool(
            name="verify_bulk_citations",
            description=(
                "Verify multiple legal citations at once against Veridictum's database. "
                "Returns verification status for each citation plus an overall hallucination "
                "risk level (LOW/MEDIUM/HIGH). Maximum 50 citations per request."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "citations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of legal citations to verify (max 50)"
                    }
                },
                "required": ["citations"]
            }
        ),
        Tool(
            name="search_cases",
            description=(
                "Search Veridictum's database of 14.2 million court cases by topic, "
                "keyword, case name, or legal principle. Returns verified cases with "
                "full citations, court info, and CourtListener links. Use this to find "
                "real cases to support legal arguments."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query: legal topic, keywords, case name, or legal principle"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (1-20, default 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="check_hallucinations",
            description=(
                "Scan a legal document for hallucinated citations. Extracts all citations "
                "from the text, verifies each one against Veridictum's database, and returns "
                "a hallucination risk assessment (SAFE/LOW/MEDIUM/HIGH). Use this BEFORE "
                "filing or submitting any legal document."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Full text of the legal document to analyze"
                    }
                },
                "required": ["text"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            if name == "verify_citation":
                response = await client.post(
                    f"{VERIDICTUM_API_URL}/verify",
                    headers=get_headers(),
                    json={"citation": arguments["citation"]}
                )

            elif name == "verify_bulk_citations":
                response = await client.post(
                    f"{VERIDICTUM_API_URL}/verify/bulk",
                    headers=get_headers(),
                    json={"citations": arguments["citations"]}
                )

            elif name == "search_cases":
                params = {"q": arguments["query"]}
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                response = await client.get(
                    f"{VERIDICTUM_API_URL}/search",
                    headers=get_headers(),
                    params=params
                )

            elif name == "check_hallucinations":
                response = await client.post(
                    f"{VERIDICTUM_API_URL}/hallucination-check",
                    headers=get_headers(),
                    json={"text": arguments["text"]}
                )

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

            response.raise_for_status()
            result = response.json()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except httpx.HTTPStatusError as e:
            return [TextContent(
                type="text",
                text=f"API Error {e.response.status_code}: {e.response.text}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
