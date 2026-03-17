# Output Outline

This note is for maintaining the skill itself. It explains why the current workflow produces multiple “understanding-layer” artifacts before case/script generation, and what each one is meant to prevent.

## Why the workflow now has more than PRD -> cases -> script

For simple pages, PRD plus a quick UI scan may be enough.

For platform-style products, that shortcut causes predictable failures:
- the model treats the product as generic CRUD UI
- PRD terms and real UI terms drift apart silently
- case coverage over-focuses on visibility and under-covers business results
- a passing Playwright run is mistaken for full PRD coverage

The current artifact chain is meant to prevent exactly those failure modes.

## Recommended artifact order

Use this order when the skill executes:

```text
PRD + environment info
-> platform-context.md
-> requirements-analysis.md
-> risk-assessment.md
-> exploration-log.md
-> spec-for-testing.md
-> test-model.md
-> case-pack-vN.md
-> coverage-audit.md
-> execution-manifest.md
-> script files
-> iteration-log.md
```

The exact timing can vary slightly, but these dependencies should remain true:
- `platform-context.md` should exist before case design becomes serious
- `spec-for-testing.md` should normalize PRD wording against observed UI wording
- `test-model.md` should define how the platform ought to be tested, not just what the UI contains
- `coverage-audit.md` and `execution-manifest.md` should exist before claiming delivery

## Artifact purposes

### `platform-context.md`
Purpose:
- define what kind of platform this is
- define business objects and their relationships
- define vocabulary and term mapping

Prevents:
- flattening a domain platform into generic UI testing
- confusing adjacent concepts such as repo/version/tag vs file/list/form

### `requirements-analysis.md`
Purpose:
- decompose the PRD into functions, ACs, ambiguities, and scope

Prevents:
- ad hoc test generation from vague PRD summaries

### `risk-assessment.md`
Purpose:
- identify high-value and high-risk paths

Prevents:
- investing script effort first in low-value UI checks

### `exploration-log.md`
Purpose:
- capture the real UI structure and observed state
- record PRD/UI mismatches
- record before/after state evidence when safe

Prevents:
- inventing selectors or behavior from memory
- claiming a business rule without observed evidence

### `spec-for-testing.md`
Purpose:
- rewrite the PRD into testing-oriented feature specs
- combine PRD expectations with current product reality
- capture reality gaps and automation boundaries

Prevents:
- forcing scripts to follow the PRD literally when the product differs
- mixing product intent and current implementation without traceability

### `test-model.md`
Purpose:
- define the object model, observation points, and coverage layers
- separate structure checks, precondition checks, business-result checks, linkage checks, and reality checks

Prevents:
- calling static UI checks “coverage” for result-oriented ACs
- losing sight of what must still be covered at L3/L4 business-result level

### `case-pack-vN.md`
Purpose:
- generate executable black-box cases from the prior layers

Prevents:
- jumping directly from UI exploration into scripts without case discipline

### `coverage-audit.md`
Purpose:
- show AC coverage status and under-covered areas

Prevents:
- treating `N passed` as equivalent to full PRD coverage

### `execution-manifest.md`
Purpose:
- explain what the script actually did in plain language

Prevents:
- opaque automation where only Playwright readers can tell what ran

### `iteration-log.md`
Purpose:
- record failure classification, repairs, reruns, and final execution status

Prevents:
- losing the reasoning behind script changes

## A practical rule of thumb

If a user asks:
- “what platform is this really?”
  - the answer should be in `platform-context.md`
- “what should be tested according to PRD plus reality?”
  - the answer should be in `spec-for-testing.md`
- “how should this platform be tested?”
  - the answer should be in `test-model.md`
- “what exactly did the script do?”
  - the answer should be in `execution-manifest.md`
- “did we cover everything?”
  - the answer should be in `coverage-audit.md`

If one document is trying to answer all of these questions at once, the workflow is collapsing and should be corrected.

## Maintenance guidance

When modifying this skill in the future:
- do not remove the intermediate artifacts unless a better structured replacement exists
- keep the delivery gate strict around explainability and coverage traceability
- prefer strengthening terminology mapping and state-evidence capture over adding more generic test-writing rules
- if you simplify the workflow, make sure you are not reintroducing the original failure mode: “tests pass, but nobody knows what was actually covered”
