# Stage Model

## End-to-end flow

```text
Input
- PRD (md/pdf)
- test environment URL
- test account

-> AI understanding stage
-> AI perception stage
-> AI generation stage
-> AI iteration stage
-> delivery
```

## Stage purposes

### AI understanding stage
Turn the PRD into a testable understanding of the product.

Outputs:
- `requirements-analysis.md`
- `risk-assessment.md`

### AI perception stage
Use Chrome MCP to inspect the real UI and collect facts that reduce ambiguity.

Outputs:
- `exploration-log.md`

### AI generation stage
Convert understanding plus perception into test assets.

Outputs:
- case pack
- script files
- version metadata

### AI iteration stage
Run the scripts, analyze failures, repair when appropriate, and record what happened.

Outputs:
- `iteration-log.md`

## MVP note

For MVP:
- run the stages from top to bottom
- do not automate full loop-back to perception
- if perception is wrong, record `perception_refresh_needed` and stop or escalate
