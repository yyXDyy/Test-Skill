# Perception Stage

## Goal

Use Chrome MCP to inspect the actual product UI so the AI works from observed reality instead of PRD assumptions alone.

Read `references/chrome-mcp-usage.md` when deciding whether Chrome MCP is appropriate, what to collect, and how much interaction is justified.

## What Chrome MCP is for here

Use it to:
- navigate the real product UI
- inspect visible structure and controls
- confirm routes, pages, dialogs, forms, and state changes
- collect browser-native clues when needed

Do not use it here to claim final delivery. This stage is for understanding and traceability.

## Default execution pattern

Use this pattern unless the situation clearly calls for something else:

```text
navigate -> snapshot -> inspect -> optional interaction -> verify -> log
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
- mismatches between PRD and UI
- artifact refs if captured

## MVP rule

In MVP, complete one clean perception pass and move forward. Do not build automatic re-entry into perception.
