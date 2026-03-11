---
name: prd-to-ui-blackbox-testing
description: Drive PRD-to-script black-box UI testing workflows. Use when the input is a PRD (markdown or PDF) plus a test environment URL and test account, and the goal is to analyze requirements, assess risk, confirm scope with a human, explore the real product UI with Chrome MCP, decompose test elements, assemble test cases, produce black-box UI automation scripts, and iterate on failures until a usable script is delivered.
---

# PRD to UI Blackbox Testing

Run a staged black-box UI test production workflow from PRD input to usable automation script output.

This skill is the top-level workflow for PRD-driven UI black-box testing. It is not a single execution tool. It coordinates requirement understanding, product exploration, case generation, script production, and repair.

## Workflow model

Use four stages in order:

1. AI understanding stage
2. AI perception stage
3. AI generation stage
4. AI iteration stage

For MVP, optimize for a clean top-to-bottom run. Do not implement a full automatic loop back into perception. If iteration reveals a perception problem, record it and stop or escalate instead of silently re-running the whole pipeline.

Read these references as needed:

- `references/stage-model.md` for the end-to-end stage map
- `references/understanding-stage.md` for requirement analysis and risk review
- `references/perception-stage.md` for Chrome MCP exploration rules
- `references/chrome-mcp-usage.md` for when and how to use Chrome MCP during perception and repair
- `references/generation-stage.md` for test element decomposition, case assembly, and script writing
- `references/case-assembly.md` for the structured middle layer from AC decomposition to coverage audit
- `references/playwright-script-production.md` for turning cases and perception outputs into Playwright black-box scripts
- `references/iteration-stage.md` for run/fail/fix behavior
- `references/artifacts-and-versioning.md` for output files and version rules

Use the templates under `assets/templates/` when creating runtime artifacts for a real run.

## Mandatory stage order

Do not skip forward casually.

- Do not enter perception before understanding outputs exist.
- Do not enter generation before understanding outputs exist and perception logging has been completed.
- Do not enter iteration before generation outputs exist.

## Required inputs

Expect these inputs unless the user explicitly narrows scope:

- PRD file (`.md` or `.pdf`)
- test environment URL
- test account or account access details

If one is missing, identify it explicitly instead of guessing.

## Stage summaries

### 1. AI understanding stage

Do:
- read the PRD
- extract flows, modules, expected behavior, and ambiguity
- assess risks and priorities
- require human confirmation on understanding and risk scope

Must produce:
- `requirements-analysis.md`
- `risk-assessment.md`

### 2. AI perception stage

Do:
- use Chrome MCP or equivalent browser exploration capability to inspect the real UI
- confirm whether PRD expectations match the product as observed
- collect AI-understandable facts about routes, controls, visible states, and key interaction points
- log what was explored and what was observed

Do not:
- treat perception notes as final test cases
- skip logging because the exploration felt obvious

Must produce:
- `exploration-log.md`

### 3. AI generation stage

Do:
- decompose the explored UI into test elements
- assemble and audit cases through the middle-layer process
- write black-box UI automation scripts
- version case and script outputs

Must produce at least:
- a case pack markdown file
- one or more script files
- version metadata

### 4. AI iteration stage

Do:
- run the generated scripts
- analyze failures
- repair scripts when the issue is in the script, locator, wait strategy, or expectation
- record iteration results

If the root cause appears to be a perception mistake:
- mark `perception_refresh_needed`
- explain why
- do not silently restart the pipeline in MVP

Must produce:
- `iteration-log.md`

## Chrome MCP usage rule

Use Chrome MCP during:
- the perception stage, to understand the real product UI
- the iteration stage, only when you need to verify whether a script failure came from misunderstanding the UI

Read `references/chrome-mcp-usage.md` for the detailed decision rules, default evidence order, and MVP constraints.

Do not use Chrome MCP as the final delivery format. The delivery artifact is the script, not the exploration trace.

## Delivery rule

A run is only considered delivered when all of the following are true:

- understanding outputs exist
- perception log exists
- case output exists
- script output exists
- iteration result exists
- known limitations and open ambiguities are stated clearly

## Output style

Be explicit about:
- current stage
- expected artifact from that stage
- what is blocked
- what was produced
- what remains before delivery
