# Understanding Stage

## Goal

Read the PRD and produce a human-reviewable understanding of what should be tested and what is risky.

## Inputs

- PRD markdown or PDF
- optional environment notes
- optional user scope constraints

## Steps

1. Read the PRD.
2. Extract product flows, modules, and expected user-visible behavior.
3. Extract ambiguity, missing details, and test data assumptions.
4. Assess risk by path, module, and user impact.
5. Ask for human confirmation of understanding and risk priority.

## Required outputs

### `requirements-analysis.md`
Include:
- summary of target scope
- user journeys
- key pages/modules
- acceptance behavior
- ambiguity list
- out-of-scope notes if any

### `risk-assessment.md`
Include:
- high-risk flows
- high-value flows
- likely brittle areas
- data/environment dependencies
- recommended execution priority
- points requiring human confirmation

## Gate

Do not enter perception until the human has confirmed or corrected the analysis/risk view.
