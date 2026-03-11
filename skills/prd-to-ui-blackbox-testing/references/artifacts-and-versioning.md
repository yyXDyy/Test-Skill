# Artifacts and Versioning

## Runtime working area

Use:

```text
runtime/blackbox/
├── requirements-analysis.md
├── risk-assessment.md
├── exploration-log.md
├── case-pack-v1.md
├── iteration-log.md
└── versions.json
```

## Minimum required artifacts

### Understanding
- `requirements-analysis.md`
- `risk-assessment.md`

### Perception
- `exploration-log.md`

### Generation
- `case-pack-vN.md`
- script files
- `versions.json`

### Iteration
- `iteration-log.md`

## Version rules

Track versions at minimum for:
- case pack
- script output

A simple JSON shape is enough for MVP:

```json
{
  "case_version": "v1",
  "script_version": "v1",
  "based_on": {
    "requirements": "requirements-analysis.md",
    "risk": "risk-assessment.md",
    "exploration": "exploration-log.md"
  },
  "status": "draft"
}
```

## Delivery check

Before claiming delivery, verify that:
- all stage artifacts exist
- script version is identified
- known limitations are stated
- open ambiguities are stated
