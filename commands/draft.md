# /veridictum:draft

Draft a legal memorandum using only verified citations from Veridictum's database.

## Usage

```
/veridictum:draft Argue that qualified immunity does not apply to excessive force during traffic stops
/veridictum:draft Brief supporting motion to dismiss for lack of personal jurisdiction
/veridictum:draft Memorandum on First Amendment protections for student speech
```

## Behavior

1. Accept the legal argument or topic to draft
2. Search for relevant cases using `search_cases` tool
3. Verify all citations using `verify_bulk_citations` tool
4. Draft the memorandum using ONLY verified citations
5. Format all citations in proper Bluebook format
6. Include CourtListener URLs for every cited case
7. Run a final hallucination check on the drafted document
8. Recommend the user run `/veridictum:check` on the final version

## Critical Rules

- NEVER include a citation that has not been verified through Veridictum
- NEVER fabricate or guess at case names, volumes, or page numbers
- ALWAYS call the verification API before including any citation
- If a citation cannot be verified, do NOT include it in the draft
- ALWAYS include CourtListener URLs — never truncate them
- ALWAYS recommend a final hallucination check before filing
