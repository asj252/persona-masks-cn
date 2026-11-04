---
type: external_ref
id: "{citekey_or_id}"
title: "{完整外部文献、基准方案或技术文档标题}"
year: {YYYY}
venue_or_source: "{会议/期刊/仓库/官方文档}"
status: verified            # 必选：skimmed（初读）| verified（已核实细节）| deprecated（淘汰封存）
stance: baseline            # 必选：baseline（直接对照基线）| supports（支撑我方）| contradicts（竞争/反驳）| methodology（借镜方法/指标）
themes: ["{theme_slug}"]
---

<!-- 模板：复制为 `kb/cards/{citekey_or_id}.md`（或 `lit_kb/papers/{citekey}.md`）。仅收录 Top 10%–20% 的关键外部基准，严禁写空泛背景摘要。删除本注释。 -->

# {完整外部文献、基准方案或技术文档标题}

- **所属主题路由（Theme Backlink）**：[{theme_slug}](../themes/{theme_slug}.md)（若本卡标 `status: deprecated` 并移入 `_archive/`，此相对链接改为 `../../themes/{theme_slug}.md`）

> **核心结论与对本项目的切入点（Core Takeaway & Gap）**：
> {一句话总结该来源的核心做法与量化结果，并明确指出它没有解决本项目的什么问题、留给我们什么切入点。}

## 1. 💡 可复用设计 / 借镜点（Stealable Ideas）
- **实验 / 架构 / 对照设计**：{哪些基线设定、消融设计、协议或模块接口可以直接沿用}
- **评估指标 / 检验 / 可视化**：{哪个公式、统计检验或图表做法值得本项目采用}

## 2. 🔪 致命缺陷与本项目切入点（Critique & Boundary）
- **前提漏洞或未控变量**：{漏掉了什么关键干扰因素、边界条件或系统约束}
- **失效边界**：{在什么数据分布、规模、延迟或设定下会退化；本项目如何针对性改进}

## 3. ⚙️ 关键实作参数、精确数值与魔鬼细节（Setup & Exact Metrics）
- **具体提示模板 / 算法步骤 / 配置参数**：{记录原文关键模板、公式或超参数，注明章节或代码位置}
- **核心数值基准**：{记录复现或横向对比需要对齐的精确数值与样本规模}

## 4. 🔗 原始出处与可直接引用的原文金句（Source & Direct Quotes）
- **原始链接 / 路径**：{URL、DOI 或仓库路径}
- **原文关键引句**：
  - > "{原文中代表其核心主张或承认自身局限的原句}"（{页码或章节}）—— **用途**：{在本项目报告、论文或架构文档中的引用位置}
