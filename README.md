# Veridictum — Legal Citation Verification Plugin

**The picks and shovels of Legal AI.**

Verify legal citations against 14.2 million real court cases to prevent AI hallucinations. Every legal AI tool generates citations — Veridictum verifies them.

## What it does

Veridictum integrates directly into Claude to provide:

- **Citation Verification** — Check any legal citation against real court records in real-time
- **Hallucination Detection** — Scan entire legal documents for fabricated citations
- **Case Law Search** — Find real cases by topic, keyword, or legal principle
- **Verified Drafting** — Draft legal memos using only citations confirmed to be real

## Installation

### From Cowork
```
claude plugin install veridictum
```

### From GitHub
```
claude plugin marketplace add veridictum/veridictum-plugin
claude plugin install veridictum@veridictum-plugin
```

## Setup (60 seconds)

### Option A: Guided setup (recommended)
After installing, just type:
```
/veridictum:setup
```
Claude will walk you through creating an account and connecting your API key — conversationally, step by step.

### Option B: Quick setup
If you already have your API key:
```
/veridictum:setup vd_key_your_key_here
```

### Option C: Environment variable (advanced)
```bash
export VERIDICTUM_API_KEY="your-api-key-here"
```

**Your API key is stored only on your local machine** at `~/.veridictum/config.json` with secure file permissions. It is never shared with Anthropic, Claude, or any third party.

## Slash Commands

| Command | Description |
|---------|-------------|
| `/veridictum:setup` | Connect your Veridictum account (one-time) |
| `/veridictum:verify` | Verify one or more legal citations |
| `/veridictum:check` | Check a document for hallucinated citations |
| `/veridictum:search` | Search 14.2M cases by topic or keyword |
| `/veridictum:draft` | Draft a legal memo with only verified citations |

## Examples

### Verify a citation
```
/veridictum:verify 384 U.S. 436
```
✅ Miranda v. Arizona, 384 U.S. 436 (1966)
- Court: Supreme Court of the United States
- CourtListener: https://www.courtlistener.com/opinion/107252/miranda-v-arizona/

### Check for hallucinations
```
/veridictum:check [paste your legal document]
```
- Total citations: 5
- Verified: 4 ✅
- Suspicious: 1 ⚠️
- Hallucination risk: LOW

### Search case law
```
/veridictum:search qualified immunity excessive force
```
Returns verified cases with full citations and CourtListener links.

### Draft with verified citations
```
/veridictum:draft Argue that qualified immunity does not apply to excessive force during traffic stops. Include 5+ citations.
```
Drafts a complete memo using only citations verified against real court records.

## Why Veridictum?

AI hallucinations in legal citations have led to:
- **Court sanctions** against lawyers (Mata v. Avianca, 2023)
- **Disciplinary proceedings** for filing fabricated cases
- **Loss of client trust** when AI-generated citations turn out to be fake

Veridictum ensures every citation is real before it reaches a courtroom.

## Pricing

| Tier | Price | For |
|------|-------|-----|
| Student | Free | Law students with .edu email |
| Professional | $49/month | Solo practitioners |
| Firm | $199/month | Up to 5 users |

## Available on

- ✅ Claude (Cowork Plugin + MCP)
- ✅ ChatGPT (Custom GPT)
- ✅ Microsoft Copilot (Copilot Studio Agent)
- ✅ Web App (veridictum.legal)

## Support

- Website: [veridictum.legal](https://veridictum.legal)
- Email: support@veridictum.legal

## License

MIT

---

*Built by a radiologist who taught himself to code. Because AI should never hallucinate in a courtroom.*
