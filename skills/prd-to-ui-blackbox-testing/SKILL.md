---
name: prd-to-ui-blackbox-testing
description: Drive PRD-to-script black-box UI testing workflows. Use when the input is a PRD (markdown or PDF) plus a test environment URL and test account, and the goal is to analyze requirements, assess risk, confirm scope with a human, explore the real product UI with Chrome MCP, decompose test elements, assemble test cases, produce black-box UI automation scripts, and iterate on failures until a usable script is delivered.
---

# PRD to UI Blackbox Testing

Run a staged black-box UI test production workflow from PRD input to usable automation script output.

This skill is the top-level workflow for PRD-driven UI black-box testing. It is not a single execution tool. It coordinates requirement understanding, product exploration, case generation, script production, and repair.

Prioritize explainability and coverage audit, not just a passing test run. A result like `5 passed` is not sufficient delivery by itself unless the user can also see:
- which PRD acceptance points were covered
- which concrete user-visible actions the script performed
- which cases were intentionally not automated
- which gaps remain and why

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
If the product contains multiple modules with shared business rules, shared components, billing logic, permissions, or terminology, create a product-level shared context first and let each module-level run reference it.
Always create a short product/module scope record before module-level understanding so the current target module is explicit.

## Mandatory stage order

Do not skip forward casually.

- Do not enter perception before understanding outputs exist.
- Do not enter perception before the human has either confirmed the understanding/risk view or explicitly accepted the default assumptions listed for this run.
- Do not enter generation before understanding outputs exist, perception logging has been completed, and the confirmation status is recorded.
- Do not enter iteration before generation outputs exist.

## Required inputs

Expect these inputs unless the user explicitly narrows scope:

- product name
- PRD file (`.md` or `.pdf`)
- test environment URL
- test account or account access details

For multi-module products, also expect:
- target module name
- any known product-level shared rules or components

If one is missing, identify it explicitly instead of guessing.
Always clarify what product is being tested before starting module-level analysis.
Try to extract the target module from the PRD first. If the module is still ambiguous after reading the PRD, ask the user instead of guessing.

## Stage summaries

### 1. AI understanding stage

Do:
- read the PRD
- identify the product first
- extract candidate modules from the PRD before locking module scope
- if module scope is still ambiguous, ask the user which module should be treated as the current target
- identify whether this is a single-module run or a product-with-modules run
- create product-level shared context when multiple modules share business rules/components
- build a product mental model before case design
- extract flows, modules, expected behavior, and ambiguity
- model core business objects, object relationships, user roles, and business-result expectations
- normalize terminology across PRD wording, UI wording, and platform/domain wording
- assess risks and priorities
- require human confirmation on understanding and risk scope

Human interaction rule:
- ask the user what product this is if the product name is not already explicit
- prefer PRD-derived module identification; only ask the user to confirm module scope when PRD evidence is insufficient or conflicting
- present a concise confirmation summary before leaving this stage
- call out the specific items that need human confirmation
- if the human does not answer every item, record which assumptions are being carried forward
- distinguish blocking vs non-blocking unanswered items
- do not silently behave as if confirmation happened

Must produce:
- `product-module-scope.md`
- `product-shared-context.md` when the module depends on product-level shared knowledge
- `platform-context.md`
- `spec-for-testing.md`
- `test-model.md`
- `requirements-analysis.md`
- `risk-assessment.md`
- `confirmation-status.md`

### 2. AI perception stage

Do:
- use Chrome MCP or equivalent browser exploration capability to inspect the real UI
- confirm whether PRD expectations match the product as observed
- collect AI-understandable facts about routes, controls, visible states, and key interaction points
- log what was explored and what was observed

Do not:
- treat perception notes as final test cases
- skip logging because the exploration felt obvious
- escalate destructive or high-impact interactions without explicit human approval

Must produce:
- `exploration-log.md`

### 3. AI generation stage

Do:
- decompose the explored UI into test elements
- assemble and audit cases through the middle-layer process
- write black-box UI automation scripts
- version case and script outputs
- make the generated automation understandable to a human reviewer, not only executable
- preserve a readable mapping from PRD/AC -> case -> script test

Must produce at least:
- a case pack markdown file
- a coverage audit markdown file
- an execution manifest markdown file
- one or more script files
- version metadata

Before claiming module-level delivery, run runtime validation.
Use strict validation before delivery:

```bash
cd <skill-root> && python3 scripts/validate_runtime.py runtime/<product> --strict
```

In strict mode, empty scope fields and module-directory mismatches are delivery-blocking errors, not warnings.
In strict mode, product/module scope conflicts across `product-module-scope.md`, module artifacts, and `versions.json` are also delivery-blocking errors.

### 4. AI iteration stage

Do:
- run the generated scripts
- analyze failures
- repair scripts when the issue is in the script, locator, wait strategy, or expectation
- record iteration results
- summarize the final executed scenarios in plain language so the user can tell what actually ran
- state clearly whether the run covered all in-scope cases or only a prioritized subset

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

- strict runtime validation passes
- platform context exists
- spec for testing exists
- test model exists
- understanding outputs exist
- perception log exists
- case output exists
- coverage audit exists
- execution manifest exists
- script output exists
- iteration result exists
- the executed cases are named and traceable back to ACs
- uncovered or deferred cases are listed explicitly
- the platform/domain vocabulary and UI terminology differences are stated clearly
- known limitations and open ambiguities are stated clearly
- the human-confirmation status is recorded clearly, including any assumptions that were not explicitly confirmed

## Output style

Be explicit about:
- current stage
- expected artifact from that stage
- what is blocked
- what was produced
- what remains before delivery
