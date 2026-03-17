# Case Assembly

## Goal

Bridge the gap between perception outputs and final script production by turning PRD understanding into structured acceptance points, design plans, and executable black-box case packs.
The middle layer must preserve platform semantics. If the product is a domain platform, do not flatten it into generic button/modal/list test design.

Use this reference as the middle layer between:
- understanding/perception
- playwright script production

This stage should reduce ambiguity before code is written.

---

## Overall phase model

Use four sub-phases in order:

1. requirement parsing and AC decomposition
2. test design planning (per F#)
3. case generation (per F#)
4. coverage reconciliation and completeness audit

For MVP, this middle layer can remain document-driven. It does not need full automation before the top-to-bottom workflow is usable.

---

# Phase 1: Requirement parsing and AC decomposition

## Role

Act as a senior test analyst.

## Goal

Read the PRD and decompose it into:
- 一级模块
- 功能点目录
- 原子验收点（AC）
- 待确认问题

## Inputs

- PRD filename
- PRD content
- `platform-context.md` when available
- `spec-for-testing.md` when available
- `test-model.md` when available

## Required output order

### 1. 一级模块识别
Output:
- `一级模块 = xxx`
- `依据：xxx`

Use the filename first as a module signal, but only keep it if it is consistent with PRD content.

### 2. 功能点目录
Use a table:

| F# | 功能名称 | 优先级 | 关键规则摘要 | 主要业务对象 | 主要业务结果 |

Rules:
- list every function point found in the PRD
- do not omit low-priority functions if they are explicitly in scope
- keep each row concise and test-oriented

### 3. 原子验收点清单
Use a table:

| AC# | 归属F# | 验收点描述（一句话，一个规则） | 优先级 | 可观察输出类型 | 业务对象 | 业务结果类型 |

Rules:
- each AC must contain exactly one testable rule/behavior/display expectation
- granularity standard: one assertion should be enough to validate the AC
- do not combine multiple behaviors into one AC
- observable output type should describe how it can be seen, e.g. text / state / navigation / visibility / disablement / toast / modal / request result visible in UI
- if the AC describes an object change or business result, identify the target object and the result type explicitly

### 4. 待确认问题
Use a table:

| Q# | 问题描述 | 涉及F#/AC# | 默认假设A | 默认假设B |

Rules:
- every PRD ambiguity or contradiction must be listed
- if you need an assumption, surface it here
- do not silently invent missing behavior

## Constraints

- use only PRD-defined content
- if a capability is not defined, do not invent it
- if an assumption is unavoidable, list it in Q#
- keep domain terms stable; if PRD and UI terms differ, normalize them using platform context and perception logs rather than mixing them casually

## Stage artifact

Recommended file:
- `runtime/blackbox/requirements-analysis.md`

---

# Phase 2: Test design planning (per F#)

## Role

Act as a senior test designer.

## Goal

Plan the testing approach for one function point at a time. Do not generate full case rows yet.

## Inputs

- 一级模块
- current F# and its description
- related AC list for that F#
- related default assumptions
- relevant platform/domain semantics
- observation guidance from `test-model.md`
- confirmation constraints from `confirmation-status.md` when available

## Required output

### 每个AC的测试设计
Use a table:

| AC# | 设计方法 | 用例规划 | 所属模块路径 | 需要模拟？ | 主观察点 | 依赖确认项 |

### 设计方法选择规则

Apply these rules:

- input domain present -> ECP (valid center + one per invalid class) + BVA (three-point boundary style)
- mutual exclusion / dependency -> COC (<=4 conditions full combination, >4 use pairwise)
- state transition -> STM (state list + transition matrix)
- submit / delete / change -> ET (repeat submit, timeout, concurrency, authorization)
- text input -> security checks (XSS / SQLi / special characters, one each)

Add these prioritization rules:
- if an AC describes a business result, include at least one result-validating case, not only visibility cases
- if an AC implies a state change, include before/after design
- if an AC involves a platform object relationship, include at least one case that reflects that relationship explicitly
- if the real UI currently blocks the PRD success path, split design into:
  - reality-check case
  - deferred success-path case
- if a result can only be weakly observed, mark that weakness and add a stronger observation direction if available

### 模块路径分配规则

- business rule / validation / state / permission -> `/{{module}}/业务/{{F#标题}}/...`
- pure UI display / layout / disablement -> `/{{module}}/UI/{{页面名}}/...`

### 预估用例数
Use a table:

| AC# | 预估条数 | 方法分布 |

## Constraints

- P0 AC >= 3 planned cases
- P1 AC >= 2 planned cases
- P2 AC >= 1 planned case
- for P0 AC, avoid spending all planned cases on static visibility unless the AC itself is only about display

## Stage artifact

Recommended file pattern:
- `runtime/blackbox/design-plan-Fx.md`

---

# Phase 3: Case generation (per F#)

## Role

Act as a senior test engineer.

## Goal

Generate complete black-box case rows from the approved design plan for one F# at a time.

## Inputs

- F# description
- AC list under that F#
- test design plan from Phase 2
- related default assumptions
- platform/domain terminology
- perception-stage before/after state evidence
- business-result and observation models from `test-model.md`
- confirmation outcomes from `confirmation-status.md`

## Required output format

Use this markdown table exactly:

| Case ID | 用例名称 | 所属模块 | 目标业务对象 | 触发动作 | 前置条件 | 步骤描述 | 预期结果 | 主观察点 | 备注 | 用例等级 |

## Three mandatory rules

### Rule 1: single assertion
The `预期结果` field must contain only one observable result.

Forbidden indicators include:
- 且
- 并且
- 同时
- 以及
- `;`
- `&`
- `and`

If a row needs any of these to express the expectation, split it into multiple cases.

### Rule 2: explicit data
Preconditions and steps must use explicit values.

Good examples:
- 应用名=`test-app-01`
- 端口=`8080`
- 角色=`viewer`

Bad examples:
- 某个应用
- 合法值
- 正确的xxx

### Rule 3: fixed note format
Use this exact format:

`方法:ECP; AC:AC-xxx; F:F?; 对象:obj; 结果:result; 观察:primary-observation; 假设:None; 确认:C-xxx/None; 模拟:none`

Every segment is required. If none applies, keep `None` / `none`.

## Simulation precondition rule

If an AC requires simulation, the precondition must explicitly say:
- simulation method
- target data shape

Examples:
- `mockMetrics, CPU=80%`
- `response replay, status=500`
- `traffic shaping, delay=30s`

## Constraints

- only black-box cases
- do not require reading database or source code
- allowed tools include UI interaction, browser DevTools, and packet capture tools
- invalid classes and boundary checks should stay single-field and single-boundary when possible
- for platform/business systems, prefer these case classes in this order when relevant:
  - business-result case
  - state-transition case
  - terminology/structure case
  - pure visibility case
- do not let an AC be “covered” only by control existence if the real user expectation is object creation, mutation, deletion, refresh, or aggregation change
- do not generate a case row that lacks an explicit observation point when the expected result is business-critical
- if a case relies on an unconfirmed assumption, mark it in the note field and keep that dependency traceable

## Stage artifact

Recommended file pattern:
- `runtime/blackbox/case-pack-vN.md`

---

# Phase 4: Coverage reconciliation and completeness audit

## Role

Act as a test quality auditor.

## Goal

Check whether generated cases cover the AC inventory and whether they meet the minimum planning standard.

## Inputs

- complete AC list from Phase 1
- all generated cases from Phase 3

## Required output

### 1. AC coverage matrix
Use a table:

| AC# | F# | 优先级 | 对应用例数 | 是否达标 | 缺口说明 |

Thresholds:
- P0 >= 3
- P1 >= 2
- P2 >= 1

### 2. Coverage gap list
List uncovered or under-covered ACs and suggest supplemental case directions.

Also identify:
- ACs covered only by static visibility checks
- ACs still missing business-result coverage
- ACs that rely on platform terminology assumptions not yet verified
- ACs that still lack strong observation points
- ACs whose current cases depend on unconfirmed assumptions

### 3. Case statistics
Summarize:
- total count
- distribution by module path
- distribution by P0/P1/P2
- distribution by method (ECP/BVA/ET/COC/STM)

### 4. Single-assert self-check
Scan all `预期结果` fields and list rows containing:
- 且
- 并且
- 同时
- 以及
- `;`
- `&`
- `and`

### 5. Risk prompts
List:
- case coverage relying on default assumptions
- case coverage relying on simulation
- Q# items that should be confirmed first

## Stage artifact

Recommended file:
- `runtime/blackbox/coverage-audit.md`

---

## How this middle layer connects to script production

Do not jump from PRD or perception directly into scripts if the case layer is still fuzzy.

Preferred bridge:

```text
requirements-analysis + risk-assessment + exploration-log
-> Phase 1 AC decomposition
-> Phase 2 design planning
-> Phase 3 case generation
-> Phase 4 coverage audit
-> playwright script production
```

When the understanding layer is strong, the bridge should remain traceable as:

```text
business object
-> triggering action
-> expected business result
-> observation point
-> case
-> script
```

## MVP note

For MVP, it is acceptable if:
- the Phase 1-4 outputs are markdown artifacts
- script production consumes these artifacts manually or semi-manually
- not every metric is automatically computed yet

The important part is that the chain is explicit and traceable.
