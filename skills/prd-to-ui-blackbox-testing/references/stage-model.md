# Stage Model

## End-to-end flow

```text
Input
- PRD (md/pdf)
- test environment URL
- test account

-> product shared understanding stage (when multiple modules exist)
   - product-module-scope.md
   - product-shared-context.md
-> AI understanding stage
   - platform-context.md
   - requirements-analysis.md
   - risk-assessment.md
   - spec-for-testing.md
   - test-model.md
-> AI perception stage
   - exploration-log.md
-> AI generation stage
   - case-pack-vN.md
   - coverage-audit.md
   - execution-manifest.md
   - script files
   - versions.json
-> AI iteration stage
   - iteration-log.md
-> delivery
```

## Stage purposes

### AI understanding stage
Turn the PRD into a testable understanding of the product.

Outputs:
- `product-module-scope.md`
- `product-shared-context.md` when the product contains multiple modules with shared rules/components
- `platform-context.md`
- `requirements-analysis.md`
- `risk-assessment.md`
- `spec-for-testing.md`
- `test-model.md`

### AI perception stage
Use Chrome MCP to inspect the real UI and collect facts that reduce ambiguity.

Outputs:
- `exploration-log.md`

### AI generation stage
Convert understanding plus perception into test assets.

Outputs:
- case pack
- coverage audit
- execution manifest
- script files
- version metadata

### AI iteration stage
Run the scripts, analyze failures, repair when appropriate, and record what happened.

Outputs:
- `iteration-log.md`

## MVP note

For MVP:
- run the stages from top to bottom
- allow a product-level shared context layer before module-level understanding when needed
- do not automate full loop-back to perception
- if perception is wrong, record `perception_refresh_needed` and stop or escalate
- do not skip the intermediate testing-spec layer for platform products
