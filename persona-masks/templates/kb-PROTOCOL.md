# 项目核心知识库规范（Tier 2 & Tier 3 Specification）

<!-- 模板：复制为项目的 `kb/PROTOCOL.md`（或 `lit_kb/PROTOCOL.md`，由 a 与 d 共同维护）。按本项目类型调整后删除本注释。 -->

本知识库围绕**本项目自身的核心目标、工作线、假设与瓶颈**建立，采用**「渐进式索引（Index-First）」**与**「外部基准 + 内部自产知识点双源沉淀（Dual-Source Intake）」**，防止上下文膨胀与跨会话重踩死胡同。规则详见 persona-masks 包 `references/kb.md`。

## 1. 三层分工与目录结构

- **Tier 1（外部全局名册／原始账本）**：如外部电子表格、GitHub Issues、实验原始 JSON 账本。保留在原处，不在 Markdown 目录中为所有扫描过的条目重复建低密度摘要档。
- **Tier 2（`themes/*.md` — 项目核心议题路由表与对比矩阵）**：100% 围绕本项目正在攻坚的 2–5 个核心工作线／问题／模块建立。一般外部参考只在矩阵记一行，不建 Tier 3 独立档。
- **Tier 3（`cards/*.md` 或 `papers/*.md` — 高密度证据卡与内部知识点卡）**：双源收录——
  1. **外部核心基准（`type: external_ref` 或 `paper_note`）**：仅收录 Top 10%–20% 的核心对照基线、直接竞争方案或方法论基石（`stance: baseline | supports | contradicts | methodology`）。
  2. **本项目内部自产知识点（`type: internal_finding`, `stance: our_finding`）**：收录本项目各阶段产生的**已验证核心结论、有效参数配方，以及「被实测证伪的死胡同（Negative Results）」**，档名统一为 `internal_{slug}.md`。

目录层级（缩进列表）：
- `kb/`（或 `lit_kb/`）
  - `PROTOCOL.md`：本规范
  - `themes/`（Tier 2）：围绕本项目核心工作线／模块的路由表
    - `{theme_slug}.md`
  - `cards/`（或 `papers/`，Tier 3）：外部核心基准卡 + 内部自产知识点卡
    - `{citekey_or_id}.md`
    - `internal_{slug}.md`
    - `_archive/`：淘汰或失参考价值的卡片（`status: deprecated`）移入此处

## 2. 检索与写入守则

1. **开工先读 Tier 2（Read-First）**：`a` 规划方案、`d` 查资料、`s` 构思方向前，先读 `themes/*.md`；仅当需核对具体数值、参数、提示模板或原文引句时，才按需展开 Tier 3 卡片。跨主题过滤可用 `rg "stance: our_finding"`、`rg "status: verified"`。
2. **收尾双源沉淀（Write-Back）**：每完成一轮外部文献调研、实验分析或阶段性自主运行，`a` 或 `d` 必须将新获悉的外部核心依据与**本项目新产生的内部知识点（含正负向结论）**增量写入 `themes/*.md` 与 `cards/*.md`（或 `papers/*.md`），并保持 Tier 2 矩阵与 Tier 3 卡片双向同步。
