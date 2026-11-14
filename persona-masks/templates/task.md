---
type: project_tasks
project: "{项目名}"
instance: "#Demo"                     # 对应 INSTANCES.md 的实例标签
active_plan_id: "P-Demo-1"            # 跨同实例独立递增的计划树号
deadline: null                        # 硬 DDL（YYYY-MM-DD）；无则填 null
status: "in_progress"                 # in_progress | blocked | paused | completed
closure:
  state: "open"                       # open | claim_verified | falsified | infra_exempt
  claim_100c: null                    # 闭环时必填：<=100 字明确主张（或为何原主张错误的证伪说明）
  evidence_ref: null                  # 闭环时必填：支撑证据或反面实测路径（如报告图或 kb 卡）
  salient_property: null              # 正向闭环必填：1 个具亮点的描述性性质；负向证伪或基建豁免填 null
frozen_guard: null                    # 单实验冻结哈希隔离保护声明（如 PLAN-E1.frozen.md）；无则填 null
updated: "YYYY-MM-DD"
---

# 任务与进度（#Demo）

<!-- 模板：复制为工作线目录 `<子目录>/task.md` 或单目录项目 `personas/architect/task.md`（法定进度源：a 单点维护主步骤树与顶层内生状态/闭环 YAML；跨专案四象限、配额加权 quota_boost 与督促轮次 p_push_round 均由全局 p 在 principal/ 统一记录，p 与 e#ops 仅只读提取本文件、不直接改写；e 可追加底部 Backlog 并更新完成状态，不改优先级与主步骤树。兼容旧制项目延续 `PLAN.md` + `backlogs.md`）。复选框约定：[ ] 待办 | [/] 进行中 | [x] 成功完结 | [-] 失败或被取代（保留原行写明原因，根完结后整棵树迁入 plan_history.md）。删除本注释。 -->

## Active Plan: P-Demo-1 {计划标题}
- **设计规范**：[implementation_plan.md](./implementation_plan.md)
- **叫停条件**：{触发转向或停工的量化读数。}

### 步骤树
- [x] **P-Demo-1.1** 最小真实冒烟（跑通核心链路与缓存命中核验） — `YYYY-MM-DD`；任务书：`T001`
- [/] **P-Demo-1.2** {主实验或主体实现} — 任务书：`T002`
  - [x] **P-Demo-1.2.1** 预演脚本与负对照干跑通过
  - [ ] **P-Demo-1.2.2** 产出效应量表与个案切片（待闭环核验）
- [ ] **P-Demo-1.3** 沉淀内部知识点卡并按需更新 Tier 2 `kb/themes/` 路由表

---

## Backlog（暂缓与待排期事项）

| 编号 | 状态 | 优先级 | 事项（做什么、为什么） | 来源 | 关联任务书/日期 |
|---|---|---|---|---|---|
| B1 | `[ ]` | 高 | {一句话：做什么、为什么} | `Q1/O2` | — |
| B2 | `[x]` | 中 | {e 实施中发现并已随手修复的周边事项} | `e` 实施追加 | `T001` (YYYY-MM-DD) |

<!-- e#ops 跨仓零 Token 汇总参考查询：
yq --front-matter=extract -o=json '{"project": .project, "instance": .instance, "plan": .active_plan_id, "deadline": .deadline, "status": .status, "closure": .closure}' "$PROJECTS_ROOT"/**/task.md
-->
