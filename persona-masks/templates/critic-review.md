---
type: critic_review
project: "{项目名}"
instance: "#Demo"
task_id: "T{编号}"
review_round: 1
review_stage: "pre_dispatch"          # pre_dispatch | delivery_audit | final_audit
verdict: "blocking"                   # blocking | approved
blocking_count: 1
suggestion_count: 0
question_count: 0
ops_borrowed: false                   # 是否借用 e#ops 运行了只读量测／重算脚本
updated: "YYYY-MM-DD"
---

# c 审查报告：T{编号}（r1）

<!-- 模板：复制为 `tasks/T{编号}/c_runs/r{轮}/c_review.md` 或项目审计报告；YAML 头供 a 核对与 e#ops 聚合统计，正文保持只读核查记录。删除本注释。 -->

## 核验范围与依据
- **待审对象**：{任务书路径／交付工作树／构建成品路径}
- **重跑命令与结果**：{检查脚本输出摘要；涉及渲染产物须写明成品目视核验结论}
- **借用 `e#ops` 只读量测**（如有）：{无／统计脚本与冒烟摘要；确认零业务文件写入}

## 阻断（Blocking）
1. **{位置／条款}**：{具体错误或依据缺失}；最便宜鉴别：{命令或对照}。

## 建议（Suggestion）
- {无／具体条文；不替代 a 决策。}

## 提问（Question）
- {无／待 a 澄清的事实问题。}

## 结论
有阻断（需待作者逐条回应并修订后复审；无阻断时改写「无阻断，可交 e」或「无阻断，建议合格」并同步 YAML 头 `verdict: "approved"` 与 `blocking_count: 0`）。
