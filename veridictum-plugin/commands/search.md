# /veridictum:search

Search Veridictum's database of 14.2 million court cases for relevant case law.

## Usage

```
/veridictum:search qualified immunity excessive force
/veridictum:search First Amendment student speech
/veridictum:search breach of fiduciary duty Delaware
```

## Behavior

1. Accept a legal topic, keyword, case name, or legal principle
2. Call `search_cases` tool with the query
3. Display results with case names, citations, courts, dates, and CourtListener links
4. All results are verified real cases from the database

## Output Format

For each result:
- Case name and citation in Bluebook format
- Court
- Date decided
- Relevance score
- Direct CourtListener link
