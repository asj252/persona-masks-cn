---
type: handoff
project: "{项目名}"
instance: "#Demo"
active_task: "task.md"
progress_source: "personas/architect/task.md"
last_commit: "{short_sha}"
updated: "YYYY-MM-DD"
---

# 交接

<!-- 模板：复制为项目的交接文件（位置由项目定，如根目录的 `HANDOFF.md`），由 a 维护。删除本注释。 -->

项目章程：{大纲 `outline.md` 的链接}；全局控制：{若启用 `p`，记 `principal/quadrants.md`}。本档以指针为主：状态与决定写在各自的档里，这里写链接；「已被取代的决定」另列日期、用户原话与替代关系，供接手时辨认旧稿。写交接之前先提交，未提交的文件在别的 worktree 与云端会话里看不到；项目不是 git 仓库的，写明交接的时间。写交接前，先同步当前工作线的法定进度源（新项目为 `task.md`，兼容旧项目为 `<子目录>/PLAN.md`、`personas/architect/plan.md` 或 `INSTANCES.md`）与闭环字段，若本次含跨实例决定或根完结，一并同步 `outline.md`「已决定」及 `plan_history.md`；不能只在本档追加。

## 当前状态
- 进度源：{链接；新项目为当前工作线 `task.md` ＋ `implementation_plan.md`，兼容旧项目为 `<子目录>/PLAN.md` 或 `personas/INSTANCES.md`}；最近一次提交：{短提交号；项目不是 git 仓库的写「不适用」与交接时间}

## 已决定
- 跨实例／全仓决定见 {全局大纲「已决定」一节的链接}，单实例内部决定见 {当前工作线 `implementation_plan.md`、兼容旧 `PLAN.md` 或本交接档对应位置}；本次会话新增的决定已按范围写进去：{是／否；否的写原因}

## 已被取代的决定
- {旧决定与新决定的链接；日期；用户原话；标明哪些设计已被试用意见取代；没有写「无」}

## 队列
- {下一步做什么：指向计划节点、待办的行或任务书}

## 规则
- {项目指令档与本项目特有约定的链接}

## 派发命令
- {派 e、c、d 用的命令或提示存在哪里}

## 交接清单
- scratchpad 里产交付物的脚本已搬进仓库：{仓库路径与原位置；未搬的写原因与待授权事项；没有写「无」}。

## 文件地图
- {关键目录与文件，一行一条：路径加一句用途}

## 开场步骤
1. {接手的人先做什么：先读 `outline.md` 目标、阈值与 `implementation_plan.md` 框定，再沿 `task.md`（或兼容旧进度源）指针接手；核对哪个提交（不是 git 仓库的，核对交接时间之后改过的文件）、跑哪个检查}
