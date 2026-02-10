# /veridictum:verify

Verify one or more legal citations against Veridictum's database of 14.2 million real court cases.

## Usage

```
/veridictum:verify 384 U.S. 436
/veridictum:verify Miranda v. Arizona, 384 U.S. 436 (1966)
/veridictum:verify 347 U.S. 483, 410 U.S. 113, 575 U.S. 348
```

## Behavior

1. Parse the input for one or more legal citations
2. If single citation: call `verify_citation` tool
3. If multiple citations: call `verify_bulk_citations` tool
4. Display results with ✅ for verified and ⚠️ for suspicious
5. Include CourtListener URLs for all verified citations
6. Show overall hallucination risk level for bulk verification

## Output Format

For each citation:
- ✅ or ⚠️ status indicator
- Case name (if verified)
- Court and date decided
- Direct CourtListener link
- Warning if suspicious: "Do not rely on this citation without independent verification"
