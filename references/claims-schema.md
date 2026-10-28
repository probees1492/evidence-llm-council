# Claims contract

Save `report/claims.json` as UTF-8 JSON:

```json
{
  "claims": [
    {"id":"C001", "text":"Milestone was completed Oct 10", "kind":"F", "evidence_ids":["E001"], "contradicts":[]},
    {"id":"C002", "text":"Schedule risk is material", "kind":"I", "evidence_ids":["E001"], "assumptions":["staffing remains constant"]},
    {"id":"C003", "text":"Long-term performance impact is unknown", "kind":"U", "evidence_ids":[]}
  ]
}
```

Allowed `kind`: F (fact), I (interpretation), U (unknown). Evidence IDs must exist; material F and I claims require at least one. An I without evidence must have `assumptions` and is flagged for manual review. Empty claim text is invalid. Logical and semantic source verification MUST still be done by the agent: a valid reference ID alone does not establish that the source supports the text.
