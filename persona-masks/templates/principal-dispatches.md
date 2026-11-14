---
type: principal_dispatches
role: "principal"
max_push_rounds: 5
active_dispatch_count: 1
circuit_broken_count: 0
updated: "YYYY-MM-DD"
---

# 跨机在途派发与科研闭环门禁台账（p 幕僚长）

<!-- 模板：按需复制到全局控制中心或资料目录 `principal/dispatches.md`。p 经 Inbox/SSH 唤醒或反推各专案 a，上限 5 轮；未问不主动向用户展开内部轮次细节。删除本注释。 -->

## 在途与待核验任务
| 派发号 | 专案 / 实例 | 目标主机 / 通道 | `p_push_round` | `closure.state` | `claim_100c`（<=100 字） | `evidence_ref` | `salient_property` | 状态 |
|---|---|---|---|---|---|---|---|---|
| `DSP-001` | `{project}` `#Demo` | `{host}` / `inbox` | `0 / 5` | `open` | `null` | `null` | `null` | `running` |

## 闭环核验与 5 轮反推约定
- **正向闭环（`claim_verified`）**：`claim_100c`（`<= 100` 字）＋ 非空 `evidence_ref` ＋ 非空 `salient_property`。
- **负向闭环（`falsified`）**：`claim_100c`（原主张为何错误）＋ `evidence_ref`（反面实测或 `kb/cards/internal_*` 死胡同卡）。
- **基建豁免（`infra_exempt`）**：须在派工单开篇显式声明为纯基建运维。
- **自动反推**：未达闭环且未触预算／安全红线而半路停工者，由 `p` 直接通过 Inbox／SSH 督促 `a` 继续推进；`p_push_round` 满 `5` 仍未闭环则自动标 `blocked` 熔断，升级至 `quadrants.md` 待拍板队列。
