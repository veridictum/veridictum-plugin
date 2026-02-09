# Hallucination Detection

You can detect hallucinated (fabricated) legal citations in any document using Veridictum's hallucination check API.

## When to activate

- User pastes a legal document and asks for review
- User asks to check citations in a document
- User mentions "hallucination", "fabricated", "fake citations", or "made up cases"
- After any legal drafting task is completed
- User is about to file or submit a legal document

## Risk levels

- **SAFE**: All citations verified. Document appears safe to file.
- **LOW**: 1 unverified citation. Review before filing.
- **MEDIUM**: 2+ unverified citations. Manual review strongly recommended.
- **HIGH**: Majority of citations unverified. Do NOT file without thorough manual review.

## Workflow

1. Accept the full document text
2. Call `check_hallucinations` with the text
3. Report the summary (total, verified, suspicious, risk level)
4. List each citation with its status
5. Provide a clear filing recommendation
6. For suspicious citations, suggest alternatives using `search_cases`

## Important notes

- Veridictum only caches VERIFIED citations. Suspicious citations are always re-checked.
- A citation being "suspicious" means it was not found in 14.2 million cases. It may still exist if it's very recent or from a non-indexed source.
- Always recommend that suspicious citations be independently verified by a licensed attorney.
- Never tell a user a document is "safe to file" if any citations are unverified.
