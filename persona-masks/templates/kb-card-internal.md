---
type: internal_finding
id: "internal_{slug}"
title: "{本项目内部知识点标题（如：某模块/实验阶段实测核心结论与已排除死胡同）}"
date: "{YYYY-MM-DD}"
workstream: "{#实例或子项目名}"
status: verified            # 必选：skimmed（初步观察）| verified（经 a/c 核实的定论）| deprecated（被后续推翻，移入 _archive/）
stance: our_finding         # 固定为 our_finding（代表本项目自产的核心实测依据）
themes: ["{theme_slug}"]
---

<!-- 模板：复制为 `kb/cards/internal_{slug}.md`（或 `lit_kb/papers/internal_{slug}.md`）。用于沉淀本项目在推进中间产生的正负向核心知识点，防止跨会话漏读或重踩死胡同。删除本注释。 -->

# {本项目内部知识点标题}

- **所属主题路由（Theme Backlink）**：[{theme_slug}](../themes/{theme_slug}.md)（若本卡标 `status: deprecated` 并移入 `_archive/`，此相对链接改为 `../../themes/{theme_slug}.md`）

> **核心实测结论与决策影响（Core Empirical Takeaway & Implication）**：
> {一句话总结本阶段实测确认的核心规律、推翻了哪个天真假设，以及对下一步路线、架构或论文主张的决定性影响。}

## 1. 💡 已验证核心现象与精确数值（Verified Findings & Exact Metrics）
- **定量结论与效应量**：{列出经核验的关键数值、效应量、置信区间、p 值或性能读数，注明样本数、模型/环境与配置}
- **可直接复用的有效配方**：{在本项目已被证实有效的参数、结构、提示模具或校准方法}

## 2. 🔪 已证伪死胡同与防重踩指南（Falsified Hypotheses & Dead Ends Ruled Out）
- **被排除的方案与退化现象**：{明确记录哪些看似合理的想法在实测中无效、崩溃或负向叠加，给出具体退化数值}
- **根因诊断**：{为什么该方案在本项目行不通（如分布退化、耦合冲突、方差爆炸），供后续会话直接规避}

## 3. ⚙️ 关键实作参数、校准公式与魔鬼细节（Methodology & Guardrails）
- **核心参数与边界约束**：{必须锁定的种子、阈值、样本量下限、内存/并发护栏或解析规则}
- **复现命令或调用入口**：{最小复现命令或脚本参数}

## 4. 🔗 仓内原始证据路径与对外交付定位（Canonical Repo Paths & Framing）
- **法源、报告与提交路径**：{指向仓内具体的 `PLAN.md` / `PROGRESS.md`、任务书、`report-*.md`、审查报告、预注册或冻结哈希}
- **对外交付 / 写作定位**：{说明这组内部知识点在最终论文、技术报告或系统文档的哪一节扮演什么角色}
