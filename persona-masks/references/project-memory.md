# 项目层：项目仓库里的 `personas/`

## 定位
- **个人层**（资料目录）：跨项目的个人规则与学习记录（PROFILE、LOG、smd、kis），见 [资料与日志](state-and-log.md)。
- **项目层**（项目仓库的 `personas/`）：各面具在该项目的规矩与经验，随仓库版控，本地与云端 session、子 agent 都读得到。
- 冲突时项目层优先，但受 [角色](roles.md) 中 c 的下限约束，也不能扩大宿主或项目既有的权限。
- 没有 `personas/` 的项目照个人 PROFILE 与包默认；本文件其余部分只在项目有 `personas/` 时适用。

## 何时建立
不自动建立。由用户要求，或 a 提出、用户同意后，把本包 `templates/` 中需要的模板复制进项目，只建用得上的面具资料夹。
模板对应：`personas-README.md` → `personas/README.md`；`INSTANCES.md`；`outline.md` → `personas/architect/outline.md`；`backlogs.md` → `personas/architect/backlogs.md`；`plan.md` → `personas/architect/plan.md`；`plan-history.md` → `personas/architect/plan_history.md`；`options.md` → `personas/seeker/options.md`；`data-collected.md` → `personas/collector/data_collected.md`；`MEMORY.md` → `personas/<面具>/MEMORY.md`；`critic.md`；`critic-shapes.md` → `personas/critic/shapes.md`；`critic-log.md` → `personas/critic/log.md`；`engineer-preflight.md` → `personas/engineer/preflight.md`。后三者属于下文「项目可采用的做法」，不采用就不建。

## 首次提示
在主会话的项目目录里（有 `.git` 或明显的项目文件，家目录不算）首次戴主角色、该项目没有 `personas/`、本次会话还没提示过时，在首行标签之后提示一次，一行：本项目没有项目层记忆，要建吗？（最小／全套／不建；想不再提示请明说）。「最小」指 `README.md` 加所戴面具的 `MEMORY.md`。用户说「不建」只对本次会话生效，新会话照常提示一次；只有用户明确表述「不再提示」，才在资料目录的 PROFILE 记一行「已婉拒的项目」，只记项目路径（条目键 `project.declined`，来源栏填本次 LOG 事件键，并记 LOG；换克隆路径或 worktree 会重新提示），之后该项目不再提示。纯聊天、没有项目目录、只用共用模块、网页端、a 派发的子 agent、任务书拉起的、为独立审查另开的上下文不提示。提示不等于建立，用户同意后才建。

## 结构
```text
personas/
  README.md        本项目的面具分工、预设读与不能写、教训放哪
  INSTANCES.md     实例（#标签）与单元登记
  critic.md        本项目 c 的范围、权限与触发点（可选）
  <面具>/MEMORY.md 按实例分节的索引
  <面具>/<条目>.md 条目档，一档一主题
  architect/outline.md         大纲（a 维护）
  architect/backlogs.md        待办（a 维护）
  architect/plan.md            计划森林（a 维护）
  architect/plan_history.md    已完结的计划树（a 维护）
  seeker/options.md            选项（s 与 a 都可写）
  collector/data_collected.md  资料（d 维护）
```
后六份是管理项目的核心文件，用到时才从模板建立；项目已有等价的文档（如根目录的大纲或待办）时，在 `personas/README.md` 指向它，不重复建；没有 `personas/` 的项目，`options.md`、`plan.md` 与 `data_collected.md` 一样先问用户记在哪里，或只写在回复里。分工：`outline.md` 管结构与已决定的事，`backlogs.md` 管还没排期的单条事项，`plan.md` 管有层级、有完结的路线，`options.md` 的通过方向要做时，转成计划的节点或待办的一行，或直接写任务书。

## 读写规矩
- **读没有禁区**；`personas/README.md` 只定各面具的**预设读**与**不能写**（一张表）。开工先读所戴面具的 `MEMORY.md` 中 `#all` 与当前实例两节，条目按需再开。
- **谁的资料夹谁写**；其他面具可读不可改（`seeker/options.md` 例外，a 也写）。跨面具传话写在自己的资料夹或任务书里，让对方来读。
- `MEMORY.md` 是索引：按实例分节（`## #all`、`## #Demo`…），一行一条、指向条目档，不放内容。条目档写绝对日期，标所属实例；一个条目只存一份，与几个实例有关就在几节各列一行。
- **不重复项目已有文档**：现况、待办、决定、任务与验收、写作规范各有其档；面具资料夹只放那些文档放不下的东西（取舍理由、错误形状、按情境的检查表）。
- 有值得留的就当场写；没有就不写，不为写而写。

## 教训放哪
判准只有一句：**不管戴哪个面具，不知道这件事就会出事吗？**
- 会 → 项目指令档（如 AGENTS.md、CLAUDE.md），缩成一两行规则句，**经用户同意**后再写；不自动修改指令档。
- 不会 → 用得到它的那个面具的资料夹。
- 只对某一次工作成立的读数与结论 → 该工作的任务书或报告，不进任何指令档或面具资料夹。
- 只在一个实例验过的教训不升为通用（`#all`），要在两个实例各自验过；另一个实例沿用时标「沿用自 #Demo，未在本线验过」。

## 项目可采用的做法
下列做法**不是默认**，也不写成默认循环的一步；项目在 `personas/README.md` 或 `personas/critic.md` 写明采用哪几项才生效：
- **一个单元一个持续的 c**：单元（如 `#Demo/U{编号}`）内的任务书与交付都送同一个 c；单元结束就关，下一单元另开，跨单元经验只经错误形状传递。
- **c 写审计产出**：c 可以写项目的审计目录（诊断结果、报告），由 a 提交；c 仍不改待审物。（装了 `brief-workflow` 的，由该包规定。）
- **终审另开干净上下文的 c**：单元终审由新开的 c 执行，先只拿产物做冷读并写下记录，之后才读基线诊断；终审完成前不读本单元的任务书与 c 的记录。（装了 `brief-workflow` 的，由该包规定。）
- **c 的 `shapes.md` 与 `log.md`**：反复出现的错误形状（长什么样、这次怎么露出来、最便宜的鉴别）；每次送审记一行，事后回填挡下或误报，定期回看，只是多了仪式就撤掉。
- **工程师的按情境检查表**（`engineer/preflight.md`）：按情境列指针与一句提醒，内文以项目指令档为准。
- **单元结束后的回顾**：a 把本单元的新经验按上文判准分派到面具资料夹或指令档（后者经用户同意）。
- **起草任务书前对照错误形状自查**。（装了 `craft` 的，由该包规定。）

## 下限
项目层与习惯包都不能取消 c 的独立上下文、不能要求 c 接收作者的推理、不能给 c 否决权；也不能扩大宿主或项目既有的权限。
