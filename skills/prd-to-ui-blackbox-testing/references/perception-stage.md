# Perception Stage

## Goal

Use Chrome MCP to inspect the actual product UI so the AI works from observed reality instead of PRD assumptions alone.
Perception should not stop at “which controls exist.” It must also collect the platform-specific meanings and the before/after state evidence needed for business-level case design.
Perception is also the main evidence-gathering stage for the understanding layer. It should confirm, refine, or challenge the product mental model created earlier.

Read `references/chrome-mcp-usage.md` when deciding whether Chrome MCP is appropriate, what to collect, and how much interaction is justified.

## What Chrome MCP is for here

Use it to:
- navigate the real product UI
- inspect visible structure and controls
- confirm routes, pages, dialogs, forms, and state changes
- collect browser-native clues when needed
- verify how platform vocabulary appears in the real UI
- capture before/after state changes for key actions when it is safe to do so
- validate object relationships and user-visible evidence for business results
- close the highest-value understanding gaps before case generation

Do not use it here to claim final delivery. This stage is for understanding and traceability.

## Default execution pattern

Use this pattern unless the situation clearly calls for something else:

```text
platform-term check -> navigate -> snapshot -> inspect -> optional interaction -> before/after verify -> log
```

## Preferred evidence order

1. snapshot
2. screenshot when visual proof is needed
3. console/network only when ambiguity or failure justifies extra evidence

## Required output

### `exploration-log.md`
For each exploration pass, record:
- timestamp
- objective
- visited routes/pages
- key observed UI facts
- key controls and visible states
- platform terminology as seen in the UI
- object and object-relationship observations
- before/after state comparisons for key actions
- mismatches between PRD and UI
- mismatches against understanding artifacts when relevant
- artifact refs if captured

## Minimum perception standard for business platforms

If the product is a business platform with domain entities such as repository/version/image/tag/task/order/ticket, capture at least:
- one terminology mapping set: PRD term -> UI term
- three before/after state comparisons for meaningful actions if safely possible
- one object hierarchy observation, such as repo -> version or project -> task
- one explicit note on whether the understanding-layer object model remains valid

If a meaningful action cannot be executed safely:
- record the blocker
- record what evidence would be needed later
- do not silently downgrade the case layer into pure visibility testing
If a perception pass changes the understanding of objects, terminology, or success criteria:
- record the change explicitly
- mark which understanding artifact should be updated
- do not let generation continue on stale understanding docs

## MVP rule

In MVP, complete one clean perception pass and move forward. Do not build automatic re-entry into perception.
But even in MVP, include enough state evidence that later cases can distinguish:
- control exists
- action is possible
- action changes platform state
- observed UI evidence is strong enough or still weak for each important business result
