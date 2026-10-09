# Persona Masks 0.4.4 · 安装与试用

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

## 习惯包：安装时询问
询问只在有 agent 协助安装或升级、或用户要求时进行；日常调用不主动询问。流程：
1. 列出三个习惯包：

   | 包 | 一句话 | 依赖 |
   |---|---|---|
   | `module-tweaks` | smd 的行数限制只管终端命令；kis 只对启用的那一则生效 | 无 |
   | `brief-workflow` | a 写任务书、c 独立审查、e 默认由 a 以子 agent 派出实施（可另开 session）、c 查验、a 判定（含无原稿时先写大纲、终审与回顾） | 宿主的子 agent 与独立 worktree（另开 session 时需要跨 session 消息、任务芯片）、session 改名等；资料目录为 git 仓库 |
   | `craft` | 验收标准写得出检查脚本；统计推断先定分析单位；预先验算；起草前对照错误形状自查；另有两条（声明范围、替换句字数） | 无 |

2. 问用户是否安装、装哪几个；不装的照包默认。
3. 对选中的包，按 [习惯包](habits/README.md) 把规则写进资料目录的 PROFILE（来源栏标 `habits/<名称>@0.4.4`＋本次安装的 LOG 事件键），并记 LOG。包内另有前提的（如 `brief-workflow` 的资料目录须为 git 仓库），按该包说明处理。

升级说明按版本从新到旧排列，每一节只写该版本相对前一版本的变化；从更早的版本升级时，从对应的一节读起，向上依次读完每一节，各节里的迁移都要做。

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
网页端没有本机文件系统，只能精简使用（保留角色与 asd，取消其余档案）：见 [网页端用法](references/web.md)（只手动维护合成一份的 `persona_brain.md`，格式与项目层六份文件相同，其余档案取消）。安装方式取决于宿主：支持上传 skill 的，把整个 persona-masks 文件夹打成 zip 上传；不支持的，把 `SKILL.md` 与 `references/` 下的各文件内容放进项目说明或项目文件；缺哪个文件，对应规则就不可用。界面与限制以宿主官方说明为准，本包未在网页端实测。

## 其他支持 Agent Skills 的宿主
保留 SKILL.md、references、templates、habits 的相对布局，按宿主的 skills 安装位置放置；agents/openai.yaml 只供 Codex 使用。首次明确资料目录。是否支持文件持久化、子 agent 和美元式 skill 调用取决于宿主，不能仅凭文件兼容宣称已测试兼容。
角色/模块前缀是本 skill 的文本约定，不是另行注册的宿主命令。

## 试用与调整
例如：“人格面具系统调整：本项目 smd 每次只给一步，其他项目维持完整步骤。”
skill 应记录 LOG，并仅在实际授权的范围更新 PROFILE。普通任务不写流水账。尚未采纳的想法与已经改动的规则分开。
不要将个人 LOG/表格/PROFILE 一起打包。此版尚未证明比普通提示更有效，也不提供强制路由或自动日志监听。

依据：[Codex 官方 skills 文档](https://learn.chatgpt.com/docs/build-skills)。
