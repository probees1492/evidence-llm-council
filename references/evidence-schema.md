# Evidence ledger format

Save `evidence/ledger.json` as UTF-8 JSON:

```json
{
  "scope": {"question":"...", "period_start":"2026-09-01", "period_end":"2026-10-28", "systems":["Confluence","Jira"]},
  "evidence": [
    {"id":"E001", "source_type":"Confluence", "title":"Project milestones", "url":"https://...", "source_date":"2026-10-10", "accessed_date":"2026-10-28", "locator":"heading: Milestones", "excerpt":"Short source passage", "reliability":"direct", "notes":"..."}
  ]
}
```

Required evidence fields: `id`, `source_type`, `title`, `locator`, `excerpt`. For traceability require at least one of `url` or `file_path`, using real locators only. `source_date`, `accessed_date`, `reliability`, `notes` optional but recommended. `source_type`: e.g. Jira, Confluence, Gmail, GitHub, document, interview, user_statement. `reliability` is a provenance assessment, not a model-generated truth score. Never copy secrets into excerpts. Avoid storing personal email addresses or private customer data where not necessary.
