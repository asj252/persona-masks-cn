---
type: principal_quadrants
role: "principal"
pull_on_demand: true
active_project_count: 1
pending_decision_count: 1
updated: "YYYY-MM-DD"
---

# 全局工作线艾森豪威尔四象限（p 幕僚长）

<!-- 模板：按需复制到全局控制中心或资料目录 `principal/quadrants.md`。p 默认只向用户输出本表与待拍板队列表，底层 Token／耗时／轮次留在 dispatches.md 与 telemetry.jsonl，用户不问不主动展开。删除本注释。 -->

## Q1 重要且紧急（Important & Urgent）
| 专案 / 实例 | 当前工作 | 硬 DDL | `quota_boost` | 闭环进度 | 待用户拍板 |
|---|---|---|---|---|---|
| `{project}` `#Demo` | `P-Demo-1.2`（`task.md`） | `YYYY-MM-DD` | `false` | `open`（推进中） | {需拍板红线；无写「无」} |

## Q2 重要不紧急（Important & Not Urgent）
| 专案 / 实例 | 当前工作 | 硬 DDL | `quota_boost` | 闭环进度 | 待用户拍板 |
|---|---|---|---|---|---|
| — | — | `null` | `false` | — | — |

## Q3 不重要紧急（Not Important & Urgent）
| 专案 / 实例 | 当前工作 | 硬 DDL | `quota_boost` | 闭环进度 | 待用户拍板 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## Q4 不重要不紧急（Not Important & Not Urgent）
| 专案 / 实例 | 当前工作 | 硬 DDL | `quota_boost` | 闭环进度 | 待用户拍板 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 待用户拍板队列（硬 DDL 临近或配额刷新已推高候选权重；最终优先序拍板权归用户）
1. `{专案 #实例}`：{1–2 句抉择背景 ＋ 预算或 DDL 影响}。
