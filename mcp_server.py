#!/usr/bin/env python3
"""
Veridictum MCP Server - Citation Verification for Claude Cowork

Provides legal citation verification tools directly within Claude
conversations via the Model Context Protocol (MCP).

Tools:
  - setup_api_key: Save your Veridictum API key (first-time setup)
  - verify_citation: Verify a single legal citation
  - verify_bulk_citations: Verify multiple citations at once
  - search_cases: Search for legal cases by topic or keyword
  - check_hallucinations: Check a legal document for hallucinated citations

API Key Resolution Order:
  1. VERIDICTUM_API_KEY environment variable
  2. ~/.veridictum/config.json local config file
  3. If neither exists, prompts user to run setup

Requires: pip install mcp httpx
"""

import os
import json
from pathlib import Path
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

VERIDICTUM_API_URL = os.environ.get("VERIDICTUM_API_URL", "https://veridictum.legal")
CONFIG_DIR = Path.home() / ".veridictum"
CONFIG_FILE = CONFIG_DIR / "config.json"

server = Server("veridictum")


def load_api_key():
    """
    Load API key using priority order:
    1. Environment variable VERIDICTUM_API_KEY
    2. Local config file ~/.veridictum/config.json
    3. Returns empty string if neither exists
    """
    # Priority 1: Environment variable
    env_key = os.environ.get("VERIDICTUM_API_KEY", "")
    if env_key:
        return env_key

    # Priority 2: Local config file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("api_key", "")
        except (json.JSONDecodeError, IOError):
            return ""

    return ""


def save_api_key(api_key: str):
    """Save API key to local config file ~/.veridictum/config.json"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config = {"api_key": api_key, "api_url": VERIDICTUM_API_URL}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    # Secure the file - owner read/write only
    CONFIG_FILE.chmod(0o600)


def get_headers():
    """Return authorization headers for Veridictum API."""
    api_key = load_api_key()
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def check_api_key_configured():
    """
    Check if API key is configured. Returns an error message if not,
    or None if everything is fine.
    """
    api_key = load_api_key()
    if not api_key:
        return (
            "⚠️ Veridictum API key not configured.\n\n"
            "To get started, you need a free API key:\n\n"
            "1. Go to https://veridictum.legal and create an account\n"
            "2. Go to your Dashboard → API Keys → Generate New Key\n"
            "3. Copy your API key\n"
            "4. Run the setup command: tell Claude to use the setup_api_key tool "
            "with your key, or type /veridictum:setup\n\n"
            "Free tier available for law students. "
            "Professional plans start at $49/month.\n\n"
            "Your API key is stored securely on your local machine only."
        )
    return None


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="setup_api_key",
            description=(
                "Save your Veridictum API key for citation verification. "
                "This is a one-time setup. Get your free API key at "
                "https://veridictum.legal/dashboard. Your key is stored "
                "securely on your local machine at ~/.veridictum/config.json "
                "and is never shared with anyone."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your Veridictum API key from https://veridictum.legal/dashboard"
                    }
                },
                "required": ["api_key"]
            }
        ),
        Tool(
            name="verify_citation",
            description=(
                "Verify a single legal citation against Veridictum's database of "
                "14.2 million real court cases. Returns verification status, case name, "
                "court, date decided, and CourtListener URL. Use this BEFORE citing any "
                "case in legal writing to ensure it is real. "
                "If the tool returns an API key error, guide the user through setup."
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

    # Handle setup separately - no API key needed for this
    if name == "setup_api_key":
        api_key = arguments.get("api_key", "").strip()
        if not api_key:
            return [TextContent(
                type="text",
                text="❌ No API key provided. Please provide your Veridictum API key."
            )]

        # Validate the key by making a test request
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{VERIDICTUM_API_URL}/health",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    }
                )
                # If we get a 401, the key is invalid
                if response.status_code == 401:
                    return [TextContent(
                        type="text",
                        text=(
                            "❌ Invalid API key. Please check your key and try again.\n\n"
                            "You can find your API key at: https://veridictum.legal/dashboard"
                        )
                    )]
        except Exception:
            # If health check fails, save anyway - server might be temporarily down
            pass

        # Save the key
        try:
            save_api_key(api_key)
            return [TextContent(
                type="text",
                text=(
                    "✅ API key saved successfully!\n\n"
                    f"Your key is stored securely at: {CONFIG_FILE}\n"
                    "This file is readable only by your user account.\n\n"
                    "You're all set! Try verifying a citation:\n"
                    "  \"Verify 384 U.S. 436\"\n\n"
                    "Or search for cases:\n"
                    "  \"Search for cases about qualified immunity\"\n\n"
                    "Available commands:\n"
                    "  /veridictum:verify  - Verify citations\n"
                    "  /veridictum:search  - Search case law\n"
                    "  /veridictum:check   - Check document for hallucinations\n"
                    "  /veridictum:draft   - Draft a memo with verified citations"
                )
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to save API key: {str(e)}"
            )]

    # For all other tools, check API key first
    key_error = check_api_key_configured()
    if key_error:
        return [TextContent(type="text", text=key_error)]

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

            # Handle authentication errors gracefully
            if response.status_code == 401:
                return [TextContent(
                    type="text",
                    text=(
                        "❌ API key is invalid or expired.\n\n"
                        "Please get a new key at https://veridictum.legal/dashboard\n"
                        "Then run /veridictum:setup to update it."
                    )
                )]

            if response.status_code == 403:
                return [TextContent(
                    type="text",
                    text=(
                        "❌ Your subscription does not include this feature.\n\n"
                        "Upgrade your plan at https://veridictum.legal/pricing\n"
                        "  - Student: Free (with .edu email)\n"
                        "  - Professional: $49/month\n"
                        "  - Firm: $199/month (up to 5 users)"
                    )
                )]

            if response.status_code == 429:
                return [TextContent(
                    type="text",
                    text=(
                        "⏳ Rate limit reached. Please wait a moment and try again.\n\n"
                        "Need higher limits? Upgrade at https://veridictum.legal/pricing"
                    )
                )]

            response.raise_for_status()
            result = response.json()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except httpx.HTTPStatusError as e:
            return [TextContent(
                type="text",
                text=f"API Error {e.response.status_code}: {e.response.text}"
            )]
        except httpx.ConnectError:
            return [TextContent(
                type="text",
                text=(
                    "❌ Could not connect to Veridictum servers.\n\n"
                    "Please check your internet connection and try again.\n"
                    "If the issue persists, check https://veridictum.legal for status updates."
                )
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
