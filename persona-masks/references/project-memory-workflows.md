# 项目层动作细则

来自 T031（issue #77、作者“执行3 + 4”）：由 [项目层入口](project-memory.md) 按动作读取；项目适用条件与权限下限仍以入口为准。

## setup：建档与结构

建档前先补读本文件 manage（CLI 的 setup 自动附上），包含等价文档不重复建、存放处询问、工作线与计划管理约束。

### 何时建立
不自动建立。由用户要求，或 a 提出、用户同意后，把本包 `templates/` 中需要的模板复制进项目，只建用得上的面具资料夹。
模板对应（全部 Markdown 模板均含 `snake_case` YAML frontmatter）：`personas-README.md` → `personas/README.md`；`INSTANCES.md`；`kis.md` → `personas/kis.md`（启用 kis 时用的项目共用元素表）；`outline.md` → `personas/architect/outline.md`（静态总目标、代号表、决定与阈值）；`implementation_plan.md` → 子项目的 `<子目录>/implementation_plan.md`（或 `personas/architect/implementation_plan.md`，对齐 Antigravity `/plan` 设计契约与 `budget_envelope`）；`task.md` → 子项目的 `<子目录>/task.md`（或 `personas/architect/task.md`，法定进度源：合并步骤树与 `## Backlog`，YAML 头含硬 DDL、状态与认知闭环字段，跨专案四象限归全局 `principal/quadrants.md`）；兼容旧模板 `plan.md`（`<子目录>/PLAN.md` 或 `plan.md`）与 `backlogs.md`（`personas/architect/backlogs.md`，供 `0.8.x` 旧项目沿用，不强制改名）；`plan-history.md` → `personas/architect/plan_history.md`；`options.md` → `personas/spark/options.md`；`option-file.md` → `personas/spark/options/<YYYY-MM-DD>-<短名>.md`（一个问题一份）；`handoff.md` → 项目的交接文件（位置由项目定，如根目录的 `HANDOFF.md`）；`data-collected.md` → `personas/collector/data_collected.md`；`kb-README.md` → `kb/README.md`（或 `lit_kb/README.md`，问题／工作线到主题的索引）；`kb-PROTOCOL.md` → `kb/PROTOCOL.md`（或 `lit_kb/PROTOCOL.md`）；`kb-theme.md` → `kb/themes/<主题>.md`（Tier 2 路由表）；`kb-card-external.md` → `kb/cards/<id>.md`（或 `lit_kb/papers/<citekey>.md`，Tier 3 外部基准卡）；`kb-card-internal.md` → `kb/cards/internal_<slug>.md`（或 `lit_kb/papers/internal_<slug>.md`，Tier 3 内部知识点卡）；`MEMORY.md` → `personas/<面具>/MEMORY.md`；`critic.md`；`critic-shapes.md` → `personas/critic/shapes.md`；`critic-log.md` → `personas/critic/log.md`；`critic-review.md` → `tasks/<任务>/c_runs/<轮>/c_review.md`（含 YAML 头审查结论）；`engineer-preflight.md` → `personas/engineer/preflight.md`。全局 `p` 端另备 4 份可选模板：`principal-quadrants.md`、`principal-dispatches.md`、`principal-resources.yaml`、`principal-telemetry.jsonl` → 复制至全局控制中心或资料目录 `principal/` 下对应文件名（去掉 `principal-` 前缀）。后几类属「项目或全局可采用的做法」，不采用就不建。

### 结构
- `personas/`
  - `README.md`：本项目的面具分工、预设读与不能写、教训放哪。
  - `INSTANCES.md`：实例（#标签）与单元登记。
  - `critic.md`：本项目 c 的范围、权限与触发点（可选）。
  - `kis.md`：项目共用元素表（启用 kis 时按需建立）。
  - `<面具>/MEMORY.md`：按实例分节的索引。
  - `<面具>/<条目>.md`：条目档，一档一主题。
  - `architect/outline.md`：项目静态大纲与章程（总目标、内部代号对照表、跨实例决定、判据与代理指标阈值，已去除进度指针表与甘特排程，a 维护）。
  - `implementation_plan.md`（子项目目录 `<子目录>/implementation_plan.md` 或 `architect/implementation_plan.md`）：可选的设计契约、目标与主要条件、`budget_envelope` 与变更契约（a 维护）。
  - `task.md`（子项目目录 `<子目录>/task.md` 或 `architect/task.md`）：法定进度源——标准复选框步骤树 ＋ 底部 `## Backlog` 节 ＋ 硬 DDL、状态与科研闭环 YAML 头（a 维护；`## Backlog` 条目与状态 e 也可更新）。兼容 `0.8.x` 旧项目沿用 `<子目录>/PLAN.md`／`architect/plan.md` ＋ `architect/backlogs.md`。
  - `architect/plan_history.md`：已完结或久未更新归档搁置的计划树（a 维护）。
  - `spark/options.md`：选项与点子资产索引，链接到 `spark/options/` 下的独立选项档案（s 与 a 都可写）；每个问题独立成档并保有专属 O0，避免跨实例单表覆盖；历史档案可跨项目正向检索复用。
  - `collector/data_collected.md`：单次查证的网址与原始证据流水表（d 维护）。
- `kb/`（或 `lit_kb/`，项目根目录的核心知识库，见 [kb](kb.md)；用到时经用户同意从 `templates/kb-*.md` 建立，a 与 d 共同维护）：
  - `README.md`（已有小写 `readme.md` 也接受）：问题／工作线到相关主题的轻量入口。
  - `PROTOCOL.md`：本项目三层知识库规范。
  - `themes/<主题>.md`（Tier 2）：100% 围绕本项目核心工作线／问题／模块的主题综述与横向对比路由矩阵（README 选择后的相关主题）。
  - `cards/<id>.md` 或 `papers/<citekey>.md`（Tier 3）：Top 10%–20% 关键外部基准卡，以及本项目实测产生的**内部知识点卡**（`internal_<slug>.md`，含已验证结论与已证伪死胡同），淘汰项移入 `_archive/`。

## manage：管理与记忆

`personas/` 核心管理文件、工作线双档（`implementation_plan.md` ＋ `task.md`）与可选的 `kb/`（或 `lit_kb/`）用到时才从模板建立；项目已有等价文档时，在 `personas/README.md` 指向它，不重复建；没有 `personas/` 的项目，`options.md`、`task.md`（或旧制 `plan.md`）与 `data_collected.md` 一样先问用户记在哪里，或只写在回复里。分工：`outline.md` 去进度化后只当本项目静态章程（总目标、内部代号对照表、跨实例决定、判据与代理指标阈值），**不再维护**「工作线与战役指针表」或甘特排程（跨项目四象限总览上移至 `p` 的 `principal/quadrants.md`，单专案步骤进度留在各子项目局部 `task.md`）；项目选择双档时，在子项目或 `architect/` 建立 `implementation_plan.md`（设计规范＋`budget_envelope`）与作为**法定进度源**的 `task.md`（复选框步骤树＋底部 `## Backlog` 节＋内生状态与可选科研闭环 YAML 块；单实例决定记在 `implementation_plan.md` 或 `HANDOFF.md`）；`0.8.x` 旧项目已有 `<子目录>/PLAN.md`／`architect/plan.md` ＋ `architect/backlogs.md` 的保持原样兼容，不强制自动改名；`plan_history.md` 收已完结（成功、失败或被取代）及久未更新（如两个月）经用户同意移入并标为「搁置」的计划树；`options.md` 的通过方向要做时，转成 `task.md` 的步骤／Backlog 行，或直接写任务书。多实例项目的计划树编号按实例隔离（`P-<实例>-<序号>`），各实例跨同实例全部子项目与 `plan_history.md` 独立递增；单实例可用 `P1、P2`，已冻结旧树不回溯改号。日常执行只更新局部法定进度源（`task.md` 或兼容旧 `PLAN.md`），仅在结案或经用户确认归档搁置时迁入 `plan_history.md`。

- **不重复项目已有文档**：现况、待办、决定、任务与验收、写作规范各有其档；面具资料夹只放那些文档放不下的东西（取舍理由、错误形状、按情境的检查表）。
- **状态只写一处，日常只改局部**：任务与计划节点的当前状态只写在法定进度源（新项目为各工作线／子项目的 `task.md`，兼容旧项目为 `<子目录>/PLAN.md`、单目录 `architect/plan.md` 或 `INSTANCES.md`；项目另指定了进度源的写在那里）。法定进度源的步骤树与顶层内生状态／闭环 YAML 头统一由专案 a 单点维护（跨专案四象限、`quota_boost` 与 `p_push_round` 统一在全局 `principal/` 记录，p 与 `e#ops` 对专案文件仅只读扫描、绝不直接改写），e 只可追加或勾选 `task.md` 底部的 `## Backlog` 条目（或兼容旧 `architect/backlogs.md`），不擅改主步骤树与优先级。任务书的状态栏与 e 的回报是该任务自己的记录，照写。`outline.md`、交接与汇总不另写子节点状态句，只引用法定进度源（`e#ops` 通过读取各仓 `task.md` 头部 YAML 向全局 `principal/quadrants.md` 与个人科研助理 WebApp 汇总看板状态）。项目可以加一个检查脚本，找出别处与进度源不一致的状态句。
- 每个面具写自己的记忆，写在自己的资料夹，不替别的面具写（a 有特权，可以写别的面具的记忆）。当场写的有三类：用户说「记下」「记住」（写在哪里按「教训放哪」一节的判准；判为项目指令档的，先提出规则句，经用户同意再写）；用户纠正了本面具的做法（写被纠正的做法和纠正后的做法）；本面具的产出被判定（采纳、否决、成立、不成立）时，写判定的理由或错误形状（面具是已结束的子 agent 时，由 a 在判定时代写）。其余不当场写。

### 教训放哪
判准只有一句：**不管戴哪个面具，不知道这件事就会出事吗？**
- 会 → 项目指令档（如 AGENTS.md、CLAUDE.md），缩成一两行规则句，**经用户同意**后再写；不自动修改指令档。
- 不会 → 用得到它的那个面具的资料夹。
- 项目在推进中间（实验拆解、统计校准、正式集分析、调参融合、架构取舍、概念拆解）产生的跨会话**核心内部知识点**（已验证的定量效应量／有效配方，以及**被实测证伪的死胡同**）→ 项目设有 `kb/`（或 `lit_kb/`）时，由 a 或 d 按 [kb](kb.md) 同步沉淀进 Tier 2 `themes/*.md` 路由矩阵与 Tier 3 `internal_<slug>.md` 卡片，不塞进面具手艺资料夹；其余只对单次任务成立的过程读数仍留在该工作的任务书或报告。
- 只在一个实例验过的教训不升为通用（`#all`），要在两个实例各自验过；另一个实例沿用时标「沿用自 #Demo，未在本线验过」。

## freeze：实验如何冷冻

- **实验如何冷冻（活体进度源与单实验冻结哈希分离）**：包含多个实验或需公开预注册的项目中，承载日常步骤树、跨实验排期与后续实验增补的**活体进度源**（如 `<子目录>/PROGRESS.md` 或持续演进的总纲档）**不得**纳入任何单实验的冻结清单（`freeze.json`）或公开预注册离线校验器（`verify_prereg.py`）的 SHA-256 绑定白名单。每个实验在进入冻结（如 S5）与公开预注册时，须单独生成只属于该实验的自包含冻结规范（如 `exp1-en/PLAN-E1.md` → `PLAN-E1.frozen.md`、`exp2-zh/PLAN-E2.md`）；单实验的 `freeze.json` 与公开预注册校验器只绑定该实验自身的冻结规范、材料、提示模板与代码哈希，使后续新增实验（如实验 2、实验 3）或更新活体进度源时，已冻结实验的校验哈希零改动、100% 保持通过。若项目早期已将顶层总纲 `PLAN.md` 的 SHA-256 绑入单实验（如实验 1）的预注册校验器，则将该 `PLAN.md` 就地封存为不可变快照（在法定进度源 `PROGRESS.md` 头部注明「总纲 `PLAN.md` 受预注册哈希保护，不直接改写」），日常步骤树与新增实验节点统一写入 `PROGRESS.md`，各后续实验的细化设计分别写入各自的独立计划档（如 `exp2-zh/PLAN-E2.md`、`exp3-en/PLAN-E3.md`）。

## handoff：交接

- **交接只放指针**：交接文件按模板 `handoff.md` 分节（当前状态、已决定、已被取代的决定、队列、规则、派发命令、交接清单、文件地图、开场步骤），全局入口指向大纲，状态与决定以链接指向进度源、大纲与指令档；交接不能代替对大纲、计划与目标缺口的更新；已被取代的决定另列日期、用户原话与替代关系，避免接手者沿用旧稿。交接清单核对 scratchpad 里产交付物的脚本是否已搬进仓库，未搬的说明原因与待授权事项。写交接之前先提交：未提交的文件在别的 worktree 与云端会话里看不到；项目不是 git 仓库的，写明交接的时间。

## review：项目可采用的做法

下列做法**不是默认**，也不写成默认循环的一步；项目在 `personas/README.md` 或 `personas/critic.md` 写明采用哪几项才生效：
- **一个单元一个持续的 c**：单元（如 `#Demo/U{编号}`）内的任务书与交付都送同一个 c；单元结束就关，下一单元另开，跨单元经验只经错误形状传递。载体无法续用时，「持续」指同一份记忆与错误形状，不指同一个会话（见 [角色](roles.md) 的 c 段）。
- **c 写审计产出**：c 可以写项目的审计目录（诊断结果、报告），由 a 提交；c 仍不改待审物。（装了 `brief-workflow` 的，由该包规定。）
- **终审另开干净上下文的 c**：单元终审由新开的 c 执行，先只拿产物做冷读并写下记录，之后才读基线诊断；终审完成前不读本单元的任务书与 c 的记录。（装了 `brief-workflow` 的，由该包规定。）
- **c 的 `shapes.md` 与 `log.md`**：反复出现的错误形状（长什么样、这次怎么露出来、最便宜的鉴别）；每次送审记一行，事后由 a 回填挡下或误报（c 多半已经结束），定期回看，只是多了仪式就撤掉。
- **工程师的按情境检查表**（`engineer/preflight.md`）：按情境列指针与一句提醒，内文以项目指令档为准。
- **单元结束后的回顾**：a 把本单元的新经验按上文判准分派到面具资料夹或指令档（后者经用户同意）。
- **起草任务书前对照错误形状自查**。（装了 `craft` 的，由该包规定。）

## kis：项目表与迁移

- `personas/kis.md` 是项目共用元素表，启用 kis 的角色或单用 kis 的执行者可读，由 a、启用 kis 且有写权限的 s／e／d，或单用 kis 且有写权限的执行者维护；这一共用表不受「谁的资料夹谁写」限制，但仍受宿主、任务书与项目权限约束（只读派发的 c 或受写权限限制的执行者只读查表，新条目写在回复中，有 a 时交 a 记入、单用时供用户保存，且 c 不改待审物）。只在用户同意后从模板建立；项目已有等价表时在 `personas/README.md` 指向它，不重复建。
- 旧个人 `kis.md` 不自动迁移。用户同意并选定条目后，保留来源地迁入；已有相同拆法时补来源，不同视角并列，目标内容有冲突时请用户取舍，不覆盖；个人旧表保留。没有项目或用户不建表时只在回复里给出条目。
