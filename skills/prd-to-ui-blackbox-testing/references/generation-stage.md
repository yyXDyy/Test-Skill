# Generation Stage

## Goal

Turn understanding outputs and perception logs into black-box test assets.

Read `references/case-assembly.md` for the middle-layer process from AC decomposition to coverage audit.
Read `references/playwright-script-production.md` for the detailed rules for turning selected cases into Playwright black-box scripts.

## Inputs

Required:
- `requirements-analysis.md`
- `risk-assessment.md`
- `exploration-log.md`

## Steps

1. Decompose test elements.
2. Assemble and audit cases.
3. Prioritize cases.
4. Write black-box UI automation scripts.
5. Version the outputs.

## Required outputs

### Case pack
Create a markdown case pack such as:
- `runtime/blackbox/case-pack-v1.md`

Include for each case:
- case id
- goal
- preconditions
- steps
- assertions
- priority
- risk link

### Script output
Create one or more automation scripts under a scripts target chosen for the project.

### Version metadata
Track at least:
- case version
- script version
- source analysis files used
- source exploration log used

## Script writing rule

Treat Chrome MCP findings as input to script writing, not as a substitute for script writing.
Use Playwright-style best practices for locators, waiting, and assertions when generating black-box UI scripts.
