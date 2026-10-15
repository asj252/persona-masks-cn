# Persona Masks 0.7.0 · 安装与试用

本包为试用中的文件型 skill；只有 Markdown 指令与可选 Codex UI 元数据，没有服务、数据库或后台监听器。
包分三部分：**系统核心**（SKILL.md、references/、templates/，一定安装）；**习惯包**（habits/，逐包询问是否安装，装了才写进个人 PROFILE）；项目内容不在包内。

## 安装位置
将整个 persona-masks 文件夹复制到宿主的个人 skills 目录：
- Claude Code：`~/.claude/skills/persona-masks/`（Windows 为 %USERPROFILE%/.claude/skills/persona-masks/）
- Codex：`~/.agents/skills/persona-masks/`（Windows 为 %USERPROFILE%/.agents/skills/persona-masks/）

两处都装时须逐字相同。已有同名目录时先核对版本与本地修改，不直接覆盖。不要在同一宿主的多个扫描目录重复安装同名包。
在下一轮请求中用“使用 $persona-masks，a$kis$smd#Demo/Q1: …”。未显示时重启宿主。
只安装 skill 不会自动修改任何项目的 AGENTS.md、CLAUDE.md，也不修改任何宿主的设置。

资料目录默认是 $CODEX_HOME/persona-masks；未设置 CODEX_HOME 时为 ~/.codex/persona-masks。可在请求里明确指定另一目录。启用时确认实际路径。
PROFILE.md、LOG.md、smd.md、kis.md 是个人运行数据，不随包分发；首次使用按需建立。升级只更换 skill 文件，保留外部资料。删除包也不删除资料。
安装或升级时（有 agent 协助时），建议用户一次：建一个跨项目的工具心得目录（按工具分资料夹，记踩过的坑与做法；用哪个工具或 cli 派发 c、d 这类个人偏好也可写在那里），并在 PROFILE 加一条指针，让各面具用某个工具之前先读对应的资料夹。用户不要就不再提；本包不建这个目录，也不规定它的格式。

## 习惯包：安装时询问
询问只在有 agent 协助安装或升级、或用户要求时进行；日常调用不主动询问。流程：
1. 列出三个习惯包：

   | 包 | 一句话 | 依赖 |
   |---|---|---|
   | `module-tweaks` | smd 的行数限制只管终端命令；kis 只对启用的那一则生效 | 无 |
   | `brief-workflow` | a 写任务书、c 独立审查、e 默认由 a 以子 agent 派出实施（可另开 session）、c 查验、a 判定（含无原稿时先写大纲、终审与回顾） | 宿主的子 agent 与独立 worktree（另开 session 时需要跨 session 消息、任务芯片）、session 改名等；资料目录为 git 仓库 |
   | `craft` | 验收标准写得出检查脚本；统计推断先定分析单位；预先验算；起草前对照错误形状自查；另有七条（声明范围、替换句字数、替换表、未舍入的差值、c 的替换句预检、判定格子表、数字出处） | 无 |

2. 问用户是否安装、装哪几个；不装的照包默认。
3. 对选中的包，按 [习惯包](habits/README.md) 把规则写进资料目录的 PROFILE（来源栏标 `habits/<名称>@0.7.0`＋本次安装的 LOG 事件键），并记 LOG。包内另有前提的（如 `brief-workflow` 的资料目录须为 git 仓库），按该包说明处理。

升级说明按版本从新到旧排列，每一节只写该版本相对前一版本的变化；从更早的版本升级时，从对应的一节读起，向上依次读完每一节，各节里的迁移都要做。

## 从 0.6.2 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。核心的变化：实例名可以在中间用连字号（如 `#paper-ideas`）；`asd:` 不再是前缀，改说「用 asd 循环」；`references/loops.md` 改名为「循环」，新增循环 s-a-d（s 构思论文／专利 idea，a 写查重摘要，用户确认后 d 查重，a 判）；来源栏示例改标 `@0.7.0`。习惯包没有变化。
2. 项目层已有 `personas/INSTANCES.md` 或 `personas/README.md` 的，命名规则那一句在项目层优先：不改就照旧只用字母与数字；要用连字号，经用户同意先把那一句改成新模板的写法。

## 从 0.6.1 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。核心没有变化。习惯包 `brief-workflow`：`roles.a-e-c-handoff` ④ 的 c 查验加变异试验（对交付的副本至少变异四次，看检查脚本能否判败）；`roles.work-cycle` ⑤ 加 e 的小修额度（任务书授权时，小改动阈值内直接修并补回归检查）与整流程预演，⑧ 终审改为先核结构再冷读，无人值守 ③ 加「不碰用户定过的措辞」与「判定时照常写记忆」，④ 停下时更新进度源、交接只放指针；`roles.report-channel` 加报告由 a 用程序存档、合计由 a 重算、c 的每轮提示与报告存进项目、e 的回报贴脚本输出原文；任务书模板的回报格式同步；来源栏示例改标 `@0.6.2`。
2. 已装 `brief-workflow` 的用户：`roles.a-e-c-handoff`、`roles.work-cycle`、`roles.report-channel` 三条按 [习惯包](habits/README.md) 的升级规则逐条询问是否更新 PROFILE，不自动改；没装的不受影响。

## 从 0.6.0 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。核心没有变化。习惯包 `craft`：`craft.ac-scriptable` 加反例干跑（手工造一两个反例，对应条目必须判败；全局条目先在基准稿上跑）；`craft.replacement-table` 把「该处」写明为「该文件」，加越界范围写成到合并提交为止、合并后的小改也走表、字节基准取工作区快照；新增 `craft.decision-table`（判定规则写成格子表并附合成例子，pilot 的可行性读数与效应读数分开）与 `craft.number-source`（数字标来源、临时脚本先入库、子 agent 的合计由主会话重算）；来源栏示例改标 `@0.6.1`。
2. 已装 `craft` 的用户：变更的两条与新增的两条按 [习惯包](habits/README.md) 的升级规则逐条询问是否更新或加入 PROFILE，不自动改；没装的不受影响。

## 从 0.5.3 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：`roles.md` 的 a 段加「框定」（写计划、呼叫 s 或 d 之前，写下宏观问题、服务哪个决定、叫停读数、方法层面的目标、授权写成当前状态，列出已有研究的入口并问用户一次；每批工作的汇总第一栏写离目标还差什么）；`options.md` 改为目录，s 每次就一个问题写一个新的选项档案（新增模板 `option-file.md`），包里其他地方说的 options 的行、列、O0 与归档指选项档案里的；`evaluation.md` 加「初评与补齐」（目标未确认时最多给 5 个方向写全评估列，其余初评搁置、确认后先补齐再判定；向用户只报短名单）；`project-memory.md` 加「状态只写一处」「交接只放指针」（新增模板 `handoff.md`），「一个单元一个持续的 c」补上载体无法续用时的含义，送审记录的结果由 a 回填；c 段加「无法续用时」（连续性靠文件）；`SKILL.md` 末段改为按宿主实际提供的能力说明；大纲、计划模板与 a 段加进度源的指向；来源栏示例改标 `@0.6.0`。
2. 已有 `personas/` 的项目不自动改：旧式 `options.md`（整张方向表）在用户同意迁移之前照旧使用，新方向照旧追加到那张表；用户同意时把它移成 `seeker/options/` 下的一个档案（如 `{日期}-既有方向.md`），`options.md` 改为目录。交接文件、进度源与送审记录的写法，用户同意时再按新模板改。
3. 习惯包本版没有变化，PROFILE 不需要改。

## 从 0.5.2 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：`roles.md`「分工的原则」改为戴任何主角色时都读，加「共享仓库」（只做限定路径的提交，不用 `add -A`、不 reset、不 amend）与「外部服务的费用」（第一次调用前核实计费，见到付费迹象或核实不了就停下问用户）两条；a 段加 a 的一次性探针例外（进入正式流程时交 e 并经 c 审查），以及交给 e 的任务书或计划先经独立的 c 审到没有阻断（用户明确说略过才略过）；c 段加送审包，以及 c 只由派发方派出、被派出的执行者不得自己派 c 或扮成 c；s、c、d 段与 `web.md` 去掉包内的工具偏好（原来 c 优先 codex cli、d 优先 antigravity cli），改为按 PROFILE 或项目层指定的派发偏好，没有指定时用宿主的独立上下文；安装说明加工具心得目录的一次性建议；习惯包 `brief-workflow` 的任务书模板加「c 审查」一行，`roles.a-e-c-handoff` ③ 派 e 前核对这一行，`roles.report-channel` 的派发偏好改指 PROFILE 或项目层；来源栏示例改标 `@0.5.3`。
2. 原来按包内默认让 c 优先派 codex cli、d 优先派 antigravity cli 的用户：升级时问用户是否把这两条写进 PROFILE（作为个人的派发偏好），写的照 PROFILE 的规则记 LOG；不写的，c 与 d 改用宿主的独立上下文。
3. 已装 `brief-workflow` 的用户：`roles.a-e-c-handoff`、`roles.report-channel` 两条按 [习惯包](habits/README.md) 的升级规则逐条询问是否更新 PROFILE，不自动改；已在用的任务书不追改，下一份起用新模板。

## 从 0.5.1 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：`roles.md` 的 s 与 d 加续用规定（同一单元以宿主的消息工具续用，派给 cli 时按宿主做得到的方式续用，不能续用就重开，仍是独立上下文）；习惯包 `brief-workflow` 的 e 改为返工续用（同一任务书的所有返工都续用原来的 e、在原分支接着提交，a 把修订提交到 e 的分支上，检查以最初的起点为准），`roles.report-channel` 写明 e 与 s 默认子 agent、持续的 c 与 d 按各自的派发偏好，以及持续的 c、s、d 的续用；任务书模板的「执行」一行与回报说明同步；来源栏示例改标 `@0.5.2`。
2. 已装 `brief-workflow` 的用户：`roles.a-e-c-handoff`、`roles.report-channel` 两条按 [习惯包](habits/README.md) 的升级规则逐条询问是否更新 PROFILE，不自动改。

## 从 0.5.0 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：记忆：a 有特权，可以写别的面具资料夹里的记忆，面具是已结束的子 agent 时由 a 在判定时代写（`project-memory.md`、`roles.md`、`personas-README.md` 同步）；`project-memory.md` 加一句：项目层可以指定进度源，指定了进度源的项目不要求建 `plan.md`；`SKILL.md` 第 29 行去掉 0.5.0 加的 wid 括注，改为「模块的调用方式以各自的参考文件为准」（`wid` 仍只接受 `wid:` 前缀与 `$wid` 模块写法，规则在 `wid.md`）；习惯包 `brief-workflow` 的 `roles.work-cycle` 加「无人值守」一段、`roles.a-e-c-handoff` 加终审一句、写明 e 不续用（每个任务书新开一个，返工也新开）并把引用的核心旧句对齐新句，`craft` 新增 `craft.replacement-table`、`craft.unrounded-diff`、`craft.c-sentence-precheck` 三条；来源栏示例改标 `@0.5.1`。
2. 已装习惯包的用户：新增与变更的条目按 [习惯包](habits/README.md) 的升级规则逐条询问是否加入 PROFILE，不自动改；没装的不受影响。
3. 已有 `personas/` 的项目不自动改；项目里的 `personas/README.md` 若仍是模板原文，用户同意时可把记忆一句与「不能写」一行换成新写法，项目有意定制的按项目层优先。

## 从 0.4.4 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：新增 `references/evaluation.md`（评估字段、端点、回填与校准）；`options.md` 的表加评估列和 O0「维持现状」一行；`outline.md` 加「判据与阈值」一节；一批用形容词做约束的规则改成了写明触发条件或数字的写法（新增条文的触发、小改动与重建比较的阈值、何时归 e、测试清单、判据的形式、归档、项目目录与模块关闭的信号、smd 与 kis 的风格词）；记忆改为每个面具写自己的；c 的意见分阻断、建议、提问三类；大纲只写项目为什么做、分几块、已决定什么，不记进度，计划的树根要写明服务大纲的哪一部分。
2. 习惯包本版没有变化，PROFILE 不需要改。
3. 已有 `personas/` 的项目不自动改；用户同意时，给 `options.md` 的表补上评估列（旧条目的 f、i、t、可撤回、成本、影响面填「未评估」，实际结果与实际贡献填「—」）并加 O0 一行，给 `outline.md` 补「判据与阈值」一节。不补时，a 在回复里写评估表（同样要有「维持现状」一行）和所用的阈值。旧 `outline.md` 的「结构」里已有的「状态」冻结、不再更新，进度以 `plan.md` 为准；`plan.md` 的树根补上「服务：大纲第 n 部分」，装了 `brief-workflow` 时叶子补任务书编号。项目里仍是模板原文的读取范围与归档说明可以换成新模板的指向句，项目有意定制的按项目层优先。

## 从 0.4.3 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：`roles.md` 里 a 的长段按主题拆成短条目；a 读 `options.md` 的范围只在 `roles.md` 的 a 段写一处，`options.md` 模板和 `web.md` 里的同类说明改为指向它；`options.md` 模板「归档」注释补上「早已不相关的行」；`web.md` 两句改称「助手（如 Claude）」。规则本身没有变。
2. 习惯包本版没有变化，PROFILE 不需要改。
3. 已有 `personas/` 的项目不自动改：它们的 `options.md` 里若仍是 0.4.3 模板的读取范围说明（未经项目定制），本版规则的意思没有变，说明与规则仍然一致，可以不改；项目有意定制的说明按项目层优先；用户同意时，再把那两条换成指向 `roles.md` 的一句。

## 从 0.4.2 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：s 不再要求每个方向标明所否定的前提，也不再要求每次至少一个方向否定现行做法，a 交给 s 的已知条件不再要求写现行做法，`options.md` 第二列表头由「方向（否定了什么前提）」改为「方向」，读取范围与去重依据不再提「所否定的前提」；类型标签保留。变招三列的占位统一为「无变招」，判定列取值写「通过」；`options.md` 模板补「归档」一节的骨架。
2. 已装 `brief-workflow` 的：任务书模板 §5 的提交命令改为 `git commit -m <说明> -- <同一组路径>`；PROFILE 的条目无需改动，来源栏可补注 `habits/brief-workflow@0.4.3`。
3. 已有 `personas/` 的项目不自动改；用户同意时再把 `options.md` 的第二列表头改为「方向」，变招三列里的「—」改为「无变招」，并在末尾补上「归档」一节。

## 从 0.4.1 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：s 为每个方向写出第一次、第二次、第三次失败时各自的变招，`options.md` 的表格加三列，a 失败时先按变招改；e 也可以更新 `backlogs.md` 的条目与状态；`a:kis:smd:` 的冒号写法同样接受。
2. 已装 `brief-workflow` 的：`roles.a-e-c-handoff`、`roles.work-cycle` 两条改为默认由 a 以子 agent 派出 e（用户要求时才另开 session），内容不同的逐条询问用户，未答复前保留原条目。
3. 已有 `personas/` 的项目不自动改；用户同意时再把 `options.md` 补上三列（旧条目填「无变招」）、`backlogs.md` 的注释改为「a 维护，e 也可更新条目与状态」，并把 `personas/README.md`「不能写」行 e 的一列加上「`architect/backlogs.md` 的条目与状态除外」（项目层优先，不改的话 e 仍不能写）。

## 从 0.4.0 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。变化：默认入口是 a，不再按目的自动选角色、不自动换面具，a 也能自己提出计划，用户不满意时 a 自动以子 agent 呼叫 s；直接用 `s:`、`d:`、`c:`、`e:` 前缀时照办并标「直接入口，未经 a 判定」；s 不再限定「五个方向」，取消探索模式（删去 `references/explore.md`），s 一律先读 `options.md`、不与已有条目重复，对条件逐项标已满足／未满足／不确定；a 追问每个方向有几种执行可能；a 接手后先弄清现状；每则回复首行标角色与实例；项目没有 `personas/` 时在主会话首次戴面具提示一次；新增 `plan.md`（计划森林）与 `plan_history.md`（完结后迁出），`options.md` 由 a 与 s 都可以写。这些随核心安装，不写进 PROFILE（「已婉拒的项目」只在用户明确要求不再提示时才记）。
2. 习惯包本版没有新增或改动条目，PROFILE 的来源栏保持不变。
3. 已有 `personas/` 的项目不自动改；用户同意时再补建 `plan.md`、`plan_history.md`（以及 0.4.0 起的 `seeker/`、`collector/` 与其余文件）。

## 从 0.3.0 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。核心的变化：删除共用模块 `t`，其内容并入 `smd`（旧 `t:` 视为 smd；资料目录里的 `t.md` 不自动改名，用户同意时可改名为 `smd.md` 并去掉复习格）；删除 `=文体` 前缀；新增主角色 `d`、循环 `asd` 与 s 的探索模式（0.4.1 起已取消）；c 与 d 的派发偏好；项目层新增 `outline.md`、`backlogs.md`、`options.md`、`data_collected.md` 四份核心文件的模板。这些随核心安装，不写进 PROFILE。
2. 已装的习惯包按 [习惯包](habits/README.md) 的「升级」重新比对同键条目：`brief-workflow` 的 `roles.a-e-c-handoff`、`roles.work-cycle`、`roles.report-channel` 与 `craft.precheck` 有改动；内容不同的逐条询问用户，未答复前保留原条目。已装 `craft` 的，新增的 `craft.claim-scope`、`craft.replacement-length` 逐条询问是否加入；都记进本次升级的 LOG 事件。
3. 已有 `personas/` 的项目不自动改；用户同意时再按新模板补建 `seeker/`、`collector/` 与六份文件。

## 从 0.2.0 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。新增共用模块 `wid` 随核心安装，不写进 PROFILE。
2. 已装的习惯包按 [习惯包](habits/README.md) 的「升级」重新比对同键条目：`brief-workflow` 的 `roles.a-e-c-handoff`、`roles.work-cycle`、`session.title-format`、`roles.report-channel` 与 `craft` 均有改动或新增；内容不同的逐条询问用户，未答复前保留原条目。已装 `craft` 的，新增的 `craft.precheck`、`craft.shapes-selfcheck` 逐条询问是否加入，加入的照「安装」写进 PROFILE；都记进本次升级的 LOG 事件。
3. 未装的习惯包照「安装时询问」处理。

## 从 0.1.0 升级
1. 更换 skill 文件（两处安装位置保持逐字相同），资料目录原样保留。
2. 按上一节询问是否安装习惯包。
3. PROFILE 已有同键条目时，与 [习惯包](habits/README.md) 的处理一致：内容相同只补注来源；内容不同逐条询问用户保留哪一份，未答复前保留原条目。

## 为项目建立 `personas/`
项目层记忆不自动建立。用户要求，或 a 提出、用户同意后，把本包 `templates/` 中用得上的模板复制进项目的 `personas/`（对应关系见 [项目层](references/project-memory.md)），再按项目填写。建立后，戴面具时先读 `personas/<面具>/MEMORY.md`。

## 网页端
网页端没有本机文件系统，只能精简使用（保留角色与两个循环，取消其余档案）：见 [网页端用法](references/web.md)（只手动维护合成一份的 `persona_brain.md`，格式与项目层六份文件相同，其余档案取消）。安装方式取决于宿主：支持上传 skill 的，把整个 persona-masks 文件夹打成 zip 上传；不支持的，把 `SKILL.md` 与 `references/` 下的各文件内容放进项目说明或项目文件；缺哪个文件，对应规则就不可用。界面与限制以宿主官方说明为准，本包未在网页端实测。

## 其他支持 Agent Skills 的宿主
保留 SKILL.md、references、templates、habits 的相对布局，按宿主的 skills 安装位置放置；agents/openai.yaml 只供 Codex 使用。首次明确资料目录。是否支持文件持久化、子 agent 和美元式 skill 调用取决于宿主，不能仅凭文件兼容宣称已测试兼容。
角色/模块前缀是本 skill 的文本约定，不是另行注册的宿主命令。

## 试用与调整
例如：“人格面具系统调整：本项目 smd 每次只给一步，其他项目维持完整步骤。”
skill 应记录 LOG，并仅在实际授权的范围更新 PROFILE。普通任务不写流水账。尚未采纳的想法与已经改动的规则分开。
不要将个人 LOG/表格/PROFILE 一起打包。此版尚未证明比普通提示更有效，也不提供强制路由或自动日志监听。

依据：[Codex 官方 skills 文档](https://learn.chatgpt.com/docs/build-skills)。
