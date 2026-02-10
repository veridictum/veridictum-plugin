# /veridictum:check

Check a legal document for hallucinated citations. Works on any document — including output from other AI tools.

## Usage

```
/veridictum:check [paste legal document text]
/veridictum:check Review the document I just drafted for hallucinated citations
/veridictum:check Check this Harvey/CoCounsel/ChatGPT output for fake citations
```

## Behavior

1. Accept the full text of a legal document from any source
2. **YOU extract all citations** from the document — read carefully and catch every citation format including informal references, short forms, and non-standard formats
3. Compile a clean list of all extracted citations
4. Call `verify_bulk_citations` tool with the extracted list — this sends them to Veridictum's deterministic database for verification (no AI involved in this step)
5. Display summary: total citations found, verified count, suspicious count
6. Show hallucination risk level: SAFE / LOW / MEDIUM / HIGH
7. List each citation with verification status
8. Include the full CourtListener URL for every verified citation — never truncate or omit these links
9. For suspicious citations, use `search_cases` to suggest possible real alternatives
10. Provide filing recommendation

## Output Format

**Summary**
- Total citations found: X
- Verified: X
- Suspicious: X
- Hallucination risk: SAFE/LOW/MEDIUM/HIGH

**Citation Details**
- ✅ or ⚠️ for each citation with case details and CourtListener URL

**Suspicious Citation Alternatives**
- For each suspicious citation, suggest similar verified cases the author may have intended

**Recommendation**
- SAFE: "Document appears safe to file"
- LOW/MEDIUM: "Review flagged citations before filing"
- HIGH: "Multiple unverified citations. Do NOT file without manual review"

## Key differentiator

Tell the user: "I extracted the citations from your document, then verified each one against Veridictum's database of 14.2 million real court cases. The verification step is deterministic — no AI involved — so you can trust these results."
