---
type: spark_options
project: "{项目名}"
instance: "#Demo"
question_id: "Q1"
title: "{问题简述}"
stage: "stage1_diverged"            # stage1_diverged | stage2_expanded | stage2_evaluated
status: "pending"                   # pending | judging | resolved_pass | resolved_all_failed
candidate_count: 0                  # 不含 O0 的候选总数
max_vs_weight: 0.0                  # 初探阶段最高 VS 典型度权重，供分布检索参考
passed_ids: []                      # 经 a 判定通过的候选编号列表；未判或全败填 []
framing_ref: "exempt"               # 指向 implementation_plan.md#1-goal--framing 或 exempt
condition_changed_at: null          # 条件变化后追加复议时填 YYYY-MM-DD；无则填 null
updated: "YYYY-MM-DD"
---

# Q{编号} {问题}

<!-- 模板：复制为 `personas/spark/options/{YYYY-MM-DD}-{短名}.md`，并在 `personas/spark/options.md` 目录里登记一行（s 与 a 都可写）。删除本注释。 -->

- 目标与判据：{一两句；判据含可检查的量加阈值，或附通过条件的是／否问句}
- 框定：{指向 `implementation_plan.md` §1 框定，见 references/roles.md 的 a 段「框定」；简单场景免打扰填「—（免框定）」}
- 建档：{YYYY-MM-DD}；条件变化后的追加：{日期与哪个条件变了；没有写「无」}

本档记 s 就上面这个问题提出的方向与 a 的判定。s 与 a 都可以写：s 记方向，a 记判定与理由（也可以自己加方向）；通过与未通过的方向都记，未通过的写理由，避免下次重复提。a 判可行性（见循环 asd）。

| 编号 | 方向 | 相对典型度（VS 估算） | 依据（`data_collected.md` 的条目） | a 的判定 | 理由 | 日期 | 可行性 f | 重要性 i | t（验证：要做什么、最小一步） | 可撤回 | 成本 | 影响面 | 实际结果 | 实际贡献 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| O0 | 维持现状 | — | {D1、D2…；无资料支撑的写「无来源」} | — | {a 的理由，一两句} | {YYYY-MM-DD} | {0–1} | {0–1} | {要做什么、最小一步；不写填「—」} | {是／否} | {数和单位} | {数和单位} | — | — |
| O1 | {一句话} | {0–1 或百分比} | {D1、D2…；无资料支撑的写「无来源」} | {待判／通过／未通过} | {a 的理由，一两句} | {YYYY-MM-DD} | {0–1} | {0–1} | {要做什么、最小一步；不写填「—」} | {是／否} | {数和单位} | {数和单位} | {1／0／—} | {0–1／—} |

- 每个方向在「方向」栏注明类型：虚构／推测／有部分依据。
- 读取范围与归档：a 读哪些行、未通过的行何时搬进「归档」，以 persona-masks 包 references/roles.md 的 a 段「a 读 `options.md` 的范围」为准，本档不另写。
- asd 内未判的写「待判」，asd 外 a 没有判定的写「—」，两者都是活动条目。
- 评估列（f、i、t、可撤回、成本、影响面、实际结果、实际贡献）的定义、端点、回填与校准，以 persona-masks 包 references/evaluation.md 为准，本档不另写；O0 是「维持现状」一行，每次评估都要有；旧条目没有评估列时，f、i、t、可撤回、成本、影响面填「未评估」，实际结果与实际贡献填「—」；O0 的判定、实际结果、实际贡献写「—」。
- 本档不写失败变招；点子保持纯粹发散，复杂的实施容错、替代路径与步骤切换写在 `implementation_plan.md`／`task.md`（或兼容旧 `plan.md`／`PLAN.md`）中，不压在点子本身。相对典型度（VS 估算）由 s 初探时估算（提取自 s 第一阶段管线分隔行响应的 `Weight`），不要求权重和为 1。栏位按需填写，初探阶段仅需单句方向与 VS 估算。
- 没有 a 的判定时（s 单独记下方向、不在循环 asd 内），「a 的判定」与「理由」两列写「—」；a 在 asd 外评估并取舍时，判定与理由照常写。「日期」列写 a 最近一次改「a 的判定」的日期，a 还没判的写 s 记下方向的日期。
- 目标与判据未经用户确认时的「初评搁置」与「待补」，见 persona-masks 包 references/evaluation.md 的「初评与补齐」。
- 通过的方向要做时，转成 `task.md` 的步骤或 `## Backlog` 一行（兼容旧制时为 `plan.md`／`backlogs.md`），或直接写任务书；本档不写实施细节。
- 判定不是「待判」、且日期距今超过归档天数（默认 30 天，见 `outline.md` 的「判据与阈值」）的条目（O0 除外），a 可以移到本档末尾的「归档」一节，移时不改内容；归档的方向仍算已有条目，s 读全部条目，复议须注明哪个条件变了。

## 归档

<!-- 未通过的行，以及日期距今超过归档天数、判定不是待判的行（O0 除外），整行搬到这里，列与上表相同。 -->
