# Generation Stage

## Goal

Turn understanding outputs and perception logs into black-box test assets.

Read `references/case-assembly.md` for the middle-layer process from AC decomposition to coverage audit.
Read `references/playwright-script-production.md` for the detailed rules for turning selected cases into Playwright black-box scripts.

## Inputs

Required:
- `platform-context.md`
- `spec-for-testing.md`
- `test-model.md`
- `requirements-analysis.md`
- `risk-assessment.md`
- `exploration-log.md`
- `confirmation-status.md`

Also required logically:
- a recorded confirmation status from the understanding stage

## Steps

1. Decompose test elements.
2. Assemble and audit cases.
3. Prioritize cases.
4. Write black-box UI automation scripts.
5. Write a human-readable execution manifest.
6. Version the outputs.

Before case generation, normalize terms using:
- PRD wording
- `platform-context.md`
- `spec-for-testing.md`
- `test-model.md`
- observed UI wording from `exploration-log.md`

Do not let the case pack mix terms casually. If PRD and UI use different names, record the mapping and keep it consistent.
Do not generate success-path cases that depend on unconfirmed destructive permissions or unconfirmed success criteria without labeling them deferred or assumption-based.
Do not let case generation ignore the understanding-layer models. Each selected case should be explainable through:
- target business object
- triggering action
- expected business result
- primary observation point
- whether the case depends on a confirmed fact or an assumption

## Required outputs

### Case pack
Create a markdown case pack such as:
- `runtime/blackbox/case-pack-v1.md`

Include for each case:
- case id
- goal
- target business object
- triggering action
- expected business result
- preconditions
- steps
- assertions
- primary observation point
- secondary observation point if relevant
- priority
- risk link
- confirmation / assumption link

### Coverage audit
Create:
- `runtime/blackbox/coverage-audit.md`

This is required, not optional. It must show:
- AC-to-case coverage
- whether each AC meets the minimum coverage threshold
- which ACs were not automated
- which ACs were deferred to later iterations

### Execution manifest
Create:
- `runtime/blackbox/execution-manifest.md`

This file exists to answer the user's practical question:
- what exactly did the automated script do?
- what did it click, fill, upload, verify, or intentionally avoid?
- which test in the script corresponds to which case IDs?
- how those actions relate to the platform's business objects

For each scripted test, include:
- script test title
- mapped case IDs
- mapped AC IDs
- mapped business objects
- mapped expected business results
- preconditions
- concrete actions performed in plain language
- visible assertions performed
- destructive/non-destructive classification
- whether it was executed in the current iteration

### Script output
Create one or more automation scripts under a scripts target chosen for the project.

### Version metadata
Track at least:
- case version
- script version
- source analysis files used
- source exploration log used
- source confirmation status used

## Script writing rule

Treat Chrome MCP findings as input to script writing, not as a substitute for script writing.
Use Playwright-style best practices for locators, waiting, and assertions when generating black-box UI scripts.
Do not stop at a runnable script. Also produce the human-readable companion artifacts needed to explain the script.
Do not convert a case into script steps unless the case still preserves the object -> action -> result -> observation chain.
