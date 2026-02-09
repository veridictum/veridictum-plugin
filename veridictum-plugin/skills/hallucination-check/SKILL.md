# Hallucination Detection

You can detect hallucinated (fabricated) legal citations in any document — including output from other legal AI tools like Harvey, CoCounsel, or ChatGPT — by extracting citations yourself and verifying them against Veridictum's deterministic database of 14.2 million real court cases.

## When to activate

- User pastes a legal document and asks for review
- User asks to check citations in a document
- User mentions "hallucination", "fabricated", "fake citations", or "made up cases"
- User pastes output from another AI tool and wants it verified
- After any legal drafting task is completed
- User is about to file or submit a legal document

## Workflow — Two-step process: YOU extract, Veridictum verifies

### Step 1: YOU extract the citations (AI-powered extraction)

Read the full document text carefully and extract EVERY legal citation you can find. Look for:

- Standard Bluebook citations: `Miranda v. Arizona, 384 U.S. 436 (1966)`
- Volume/reporter citations: `384 U.S. 436`
- Pinpoint citations: `384 U.S. at 444`
- Federal Reporter citations: `485 F.3d 463`
- Federal Supplement citations: `123 F. Supp. 2d 456`
- Short-form references: `Miranda, 384 U.S. at 444`
- Informal references with enough detail to identify: `the Court's holding in Scott v. Harris`
- State reporter citations: `123 Cal. App. 4th 456`
- Citations with "See", "See also", "Cf.", "But see" signal prefixes

Be thorough. Extracting every citation is critical — a missed citation could be a hallucinated one.

Compile a clean list of all citations found, normalized to their most complete form.

### Step 2: Veridictum verifies (deterministic database check)

Send the extracted citations to the `verify_bulk_citations` tool. This calls Veridictum's API, which checks each citation against 14.2 million real court records. This step is deterministic — no AI involved — the citation either exists in the database or it doesn't.

### Step 3: Report the results

Calculate and display:

**Summary**
- Total citations found: [count]
- Verified: [count] ✅
- Suspicious: [count] ⚠️
- Hallucination risk level: SAFE / LOW / MEDIUM / HIGH

**Citation Details**
For each citation:
- ✅ or ⚠️ status indicator
- Case name, court, date decided (for verified citations)
- Full CourtListener URL — never truncate or omit these links
- Warning message (for suspicious citations)

**Filing Recommendation**
- SAFE: "All citations verified. Document appears safe to file."
- LOW: "1 unverified citation. Review flagged citation before filing."
- MEDIUM: "2+ unverified citations. Manual review strongly recommended."
- HIGH: "Majority of citations unverified. Do NOT file without thorough manual review."

### Step 4: Suggest alternatives for suspicious citations

For any citation that cannot be verified, use `search_cases` to find similar real cases that might be what the author intended. Present these as suggestions: "Did you mean [verified case]?"

## Risk level calculation

- **SAFE**: 0 suspicious citations out of total
- **LOW**: 1 suspicious citation out of total
- **MEDIUM**: 2+ suspicious citations, but majority are verified
- **HIGH**: 50% or more citations are suspicious

## Why this two-step approach?

The power of this approach is the separation of concerns:
- **YOU** (Claude) are excellent at reading documents and understanding context — you catch citations that regex would miss, including informal references, citations with typos, and non-standard formats.
- **Veridictum** is a deterministic database — it does not use AI for verification. A citation either matches a real case in 14.2 million records or it doesn't. There is no guessing, no confidence score, no hallucination risk in the verification step itself.

This means the verification results are trustworthy in a way that AI-only systems cannot match.

## Important notes

- Veridictum only caches VERIFIED citations. Suspicious citations are always re-checked via the API.
- A citation being "suspicious" means it was not found in 14.2 million cases. It may still exist if it is very recent or from a non-indexed court.
- Always recommend that suspicious citations be independently verified by a licensed attorney.
- Never tell a user a document is "safe to file" if any citations are unverified.
- This skill works on documents from ANY source — user-drafted, AI-generated, output from Harvey, CoCounsel, ChatGPT, Gemini, or any other tool.
