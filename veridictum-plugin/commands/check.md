# /veridictum:check

Check a legal document for hallucinated citations. Paste or reference the document text.

## Usage

```
/veridictum:check [paste legal document text]
/veridictum:check Review the document I just drafted for hallucinated citations
```

## Behavior

1. Accept the full text of a legal document
2. Call `check_hallucinations` tool with the document text
3. Display summary: total citations found, verified count, suspicious count
4. Show hallucination risk level: SAFE / LOW / MEDIUM / HIGH
5. List each citation with verification status
6. Provide filing recommendation

## Output Format

**Summary**
- Total citations found: X
- Verified: X
- Suspicious: X
- Hallucination risk: SAFE/LOW/MEDIUM/HIGH

**Citation Details**
- ✅ or ⚠️ for each citation with case details
- Include the full CourtListener URL for every verified citation — never truncate or omit these links

**Recommendation**
- SAFE: "Document appears safe to file"
- LOW/MEDIUM: "Review flagged citations before filing"
- HIGH: "Multiple unverified citations. Do NOT file without manual review"
