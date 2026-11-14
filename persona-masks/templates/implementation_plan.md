---
type: implementation_plan
project: "{项目名}"
instance: "#Demo"
plan_id: "P-Demo-1"
charter_ref: "../../personas/architect/outline.md"
options_ref: null                     # 源自 s 的通过方向如 Q1/O1；无则填 null
review_tier: "confirm"                # explore | collect | confirm
c_verdict: "pending"                  # pending | blocking | approved | skipped_by_user
budget_envelope:                      # 由 p 下发或任务书交接点核定的资源边界
  target_host: "{目标主机名}"
  preferred_executor: "{执行载体，如 codex-cli}"
  max_wall_hours: 4.0
  paid_api_cap_usd: 15.0
status: "active"                      # draft | active | frozen | archived
updated: "YYYY-MM-DD"
---

# Implementation Plan: P-Demo-1 {计划标题}

<!-- 模板：复制为工作线目录 `<子目录>/implementation_plan.md` 或单目录项目 `personas/architect/implementation_plan.md`（由 a 维护）。对齐 Antigravity `/plan` 工件结构与五项框定。删除本注释。 -->

## 1. Goal & Framing（目标与五项框定）
- **宏观问题与交付对象**：{项目要交出什么、谁来评判、在全局中的位置。}
- **服务的决定**：{这项工作帮用户或研究定下哪一个明确取舍。}
- **叫停或转向读数**：{看到什么具体定量或门禁失败就停下或转向。}
- **方法层目标**：{写成可验证方法问题，不写成某实例好不好。}
- **当前授权状态**：{例如获批额度上限 `15 USD`；禁止修改已冻结 `exp1/PLAN-E1.frozen.md`。}
- **既有研究入口**：{`kb/themes/{主题}.md`、`personas/spark/options/` 等内部文献或前作路径。}

## 2. User Review Required（需人工拍板的红线）
> [!IMPORTANT]
> - 除超出预算包络（`budget_envelope`）或触发上述叫停读数外，获准按 `task.md` 连续推进至达成「100 字以内主张＋证据＋亮点性质（或证伪＋死胡同卡）」科研认知闭环。

## 3. Proposed Changes（模块与文件变更契约）

### {模块分组}
- `[MODIFY]` `{path/to/file}`：{具体变更契约与不变量。}
- `[NEW]` `{path/to/new_file}`：{新文件职责、参考实现差分测试要求。}

## 4. Verification Plan（验证与验收计划）

### Automated Tests（脚本可机械判定）
1. **负对照干跑**：{构造缺漏／越界／损坏样本运行检查脚本，断言全部判败。}
2. **最小真实冒烟**：{先跑最小真实样本，核验关键字段、`cached_tokens` 缓存命中率与编码正常。}

### Closure Deliverables（科研认知闭环交付标准）
- 产出一句 `<= 100` 字明确主张（或负向证伪说明）、对应证据路径（SVG 图表须目视核验无截断重叠）、1 个具亮点描述性性质（正向闭环），并按需沉淀进 `kb/` 卡片。
