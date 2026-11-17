#!/usr/bin/env python3
"""persona-masks 规则按需装配（只读、可选）。

按调用前缀解析主角色、共用模块、实例、问题与循环，只输出当次要读的规则段落
（角色前言、当前主角色常驻段与「分工的原则」、已启用模块及阶段／动作、当次循环）与项目记忆路径，
供宿主或命令行装配提示词。规则以各参考文件原文为准，本脚本只按标题切段。
只用 Python 3.8 以上的标准库；只读文件，不写文件、不联网、不执行别的命令。

用法（在任意目录执行，路径按本文件所在的 skill 目录解析）：
  python3 scripts/load_mask_context.py 'a$wid#Demo/Q1'
  python3 scripts/load_mask_context.py p#global --json
  python3 scripts/load_mask_context.py a --loop s-a-d --cwd <项目目录>
  python3 scripts/load_mask_context.py 'wid:'          # kb 的单次问答快照
  python3 scripts/load_mask_context.py a --stage dispatch --stage close
  python3 scripts/load_mask_context.py kb --kb-action create --kb-action write
  python3 scripts/load_mask_context.py --project-action freeze --cwd <项目目录>
  python3 scripts/load_mask_context.py a --principle git --principle ask
  python3 scripts/load_mask_context.py --selftest      # 内置自检
别名：模块 wid -> kb（`wid` 写在开头、前面没有 `$` 时是快照）；循环 s-a-d、sad -> asd（查重子模式）。
退出码：0 成功；2 前缀或参数无法解析（未登记的角色、模块不自动创造）；3 规则文件缺少要找的段落。
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ROLES = {  # 代号：（中文名，roles.md 里的段标题开头，项目层资料夹候选）
    "p": ("幕僚长", "## p 幕僚长", ()),
    "s": ("思索者", "## s 思索者", ("spark", "seeker")),
    "a": ("建筑师", "## a 建筑师", ("architect",)),
    "e": ("工程师", "## e 工程师", ("engineer",)),
    "c": ("批判者", "## c 批判者", ("critic",)),
    "d": ("数据家", "## d 数据家", ("collector",)),
}
ROLES_FILE = "references/roles.md"
PRINCIPLES = "## 分工的原则"
MODULES = {"kis": "references/kis.md", "kb": "references/kb.md"}
MODULE_ALIASES = {"wid": "kb"}
LOOPS = {"asd": ("asd", False), "s-a-d": ("asd", True), "sad": ("asd", True)}
LOOPS_FILE = "references/loops.md"
DUP_HEADING = "## 查重子模式"
SNAPSHOT_HEADING = "## snapshot："
WORKFLOWS = "references/architect-workflows.md"
MAINTENANCE = "references/kb-maintenance.md"
PROJECT_ENTRY = "references/project-memory.md"
PROJECT_WORKFLOWS = "references/project-memory-workflows.md"
PROJECT_ACTIONS = {
    "setup": "授权建档／模板／结构（自动附 manage）",
    "manage": "新计划／管理／归档／记忆与教训（建档另读 setup）",
    "freeze": "实验冻结／预注册／修改可能受保护的计划之前",
    "handoff": "交接之前（含提交前提）",
    "review": "考虑或采用项目可选审查做法之前",
    "kis": "项目 kis 表权限／旧个人表迁移",
}
PROJECT_DEPS = {"setup": ("manage",)}
COMMON = "references/common-workflows.md"
PRINCIPLE_ACTIONS = {
    "write": "写资料／日志／表／KB／快照等文件前",
    "git": "任何 Git 写操作前（同时读 write）",
    "ask": "向用户提问／列选择前",
    "slides": "使用已有模板制作简报前",
    "dispatch": "派发代理前",
}
PRINCIPLE_DEPS = {"git": ("write",)}
STAGES = {
    "plan": "计划／框定／管理",
    "dispatch": "派工前；对象 s/d/c/e 用 --dispatch-to，未选附 plan、ideate",
    "ideate": "呼叫 s／候选／options",
    "evaluate": "评估／回应／回填：用 --evaluation-action；未选全读并附 ideate",
    "deliver": "收件／改稿／交付",
    "close": "自主运行／阶段收尾",
}
KB_ACTIONS = {
    "create": "建库／扩充／新增卡片或主题",
    "write": "修改卡片／双源沉淀；新增前补 create",
    "archive": "封存（自动附 write）",
    "snapshot": "wid: 保存本则问答",
}
STAGE_DEPS = {"dispatch": ("plan", "ideate"), "evaluate": ("ideate",)}
DISPATCH_DEPS = {"s": ("plan", "ideate"), "d": ("plan",), "c": (), "e": ()}
EVALUATION_DEPS = {
    "assess": ("context", "fields", "assess"), "respond": ("context", "respond"),
    "backfill": ("context", "fields", "backfill"), "check": ("context", "fields", "assess", "check"),
}
EVALUATION_ALL = ("context", "fields", "assess", "respond", "backfill", "check")
EVALUATION_HEADS = {
    "context": "# 评估：", "fields": "## 字段", "assess": "## 初评与补齐",
    "respond": "## 回应 c 的意见", "backfill": "## 回填与校准", "check": "## c 查验评估是否齐全",
}
ACTION_HEADS = {
    "create": ("structure", "create"), "write": ("structure", "write"),
    "archive": ("structure", "write", "archive"), "snapshot": ("snapshot",),
}
NAME_RE = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\Z")
QUESTION_RE = re.compile(r"[A-Za-z0-9]+\Z")
HEADING_RE = re.compile(r"(#{1,6}) ")


class UsageError(Exception):
    """前缀或参数无法解析。"""


class MissingSection(Exception):
    """规则文件里找不到要切的段落。"""


def parse_prefix(prefix):
    """解析 `角色[$模块…][#实例][/问题]:`，也接受冒号连接模块（`a:kis:kb:`）与只用模块（`kb:`、`$kis`、`wid:`）。"""
    res = {"role": None, "modules": [], "aliases": {}, "instance": None, "question": None, "snapshot": False}
    body = re.sub(r"\s*:\s*", ":", (prefix or "").strip())  # 空格只允许在冒号前后（如 `wid : …`）
    if body.endswith(":"):
        body = body[:-1]
    if not body:
        return res
    if re.search(r"\s", body):
        raise UsageError(f"前缀「{prefix}」里有空白：空格只允许在冒号前后")
    if "/" in body:
        body, question = body.split("/", 1)
        if not QUESTION_RE.match(question):
            raise UsageError(f"问题名「{question}」只用英文字母与数字，不能为空")
        res["question"] = question
    if "#" in body:
        body, instance = body.split("#", 1)
        if not NAME_RE.match(instance):
            raise UsageError(f"实例名「{instance}」只用英文字母与数字，中间可用连字号，不放开头与结尾、不连用两个")
        res["instance"] = instance
    head = body.replace(":", "$").lower()
    if not head:
        return res
    tokens = head.split("$")
    first, rest = tokens[0], tokens[1:]
    if first in ROLES:
        res["role"] = first
    elif first == "wid":
        res["snapshot"] = True
    elif first in MODULES or first in MODULE_ALIASES:
        rest = [first] + rest
    elif first != "":
        raise UsageError(f"未登记的角色或模块「{first}」：角色只有 {'/'.join(ROLES)}，模块只有 {'/'.join(MODULES)}（别名 wid、t）")
    for tok in rest:
        name = MODULE_ALIASES.get(tok, tok)
        if name not in MODULES:
            raise UsageError(f"未登记的模块「{tok}」：模块只有 {'/'.join(MODULES)}（别名 wid、t）")
        if tok in MODULE_ALIASES:
            res["aliases"][tok] = name
        if name not in res["modules"]:
            res["modules"].append(name)
    return res


def read(skill, rel):
    path = skill / rel
    if not path.is_file():
        raise MissingSection(f"缺少规则文件 {rel}")
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def sections(text):
    """切成（标题行，层级，起始行，结束行）；代码块里的 # 不算标题。"""
    lines = text.split("\n")
    heads, fence = [], False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
            continue
        m = None if fence else HEADING_RE.match(line)
        if m:
            heads.append((i, len(m.group(1)), line))
    out = []
    for k, (i, level, line) in enumerate(heads):
        end = next((j for j, lv, _ in heads[k + 1:] if lv <= level), len(lines))
        out.append((line, level, i, end))
    return lines, out


def cut(text, heading, rel):
    lines, secs = sections(text)
    for line, _level, start, end in secs:
        if line.startswith(heading):
            return line, "\n".join(lines[start:end]).strip("\n")
    raise MissingSection(f"{rel} 里找不到以「{heading}」开头的标题")


def drop(text, heading, rel):
    lines, secs = sections(text)
    for line, _level, start, end in secs:
        if line.startswith(heading):
            return "\n".join(lines[:start] + lines[end:]).strip("\n")
    raise MissingSection(f"{rel} 里找不到以「{heading}」开头的标题")


def skill_version(skill):
    m = re.search(r'^\s*version:\s*"([^"]+)"', read(skill, "SKILL.md"), re.M)
    return m.group(1) if m else "unknown"


def data_dir(explicit):
    if explicit:
        return Path(explicit).expanduser()
    if os.environ.get("CODEX_HOME"):
        return Path(os.environ["CODEX_HOME"]).expanduser() / "persona-masks"
    return Path.home() / ".codex" / "persona-masks"


STRONG_MARKS = ("personas", ".git")
WEAK_MARKS = ("AGENTS.md", "CLAUDE.md", "README.md", "kb", "lit_kb")


def detect_project(cwd):
    """从 cwd 向上找项目根，家目录及其以上不算项目；只检查是否存在。
    先找第一个含 `personas/` 或 `.git` 的目录；都没有时，取最近一个含 `AGENTS.md`、`CLAUDE.md`、`README.md`
    （project-memory.md「首次提示」的项目标记）或 `kb/`、`lit_kb/`（kb 不要求先有 personas/）的目录。"""
    start = Path(cwd).expanduser().resolve()
    if not start.is_dir():
        raise UsageError(f"--cwd 不是目录：{start}")
    home = Path.home().resolve()
    stop = {home, *home.parents}
    root = weak = None
    for d in [start] + list(start.parents):
        if d in stop:
            break
        if any((d / m).exists() for m in STRONG_MARKS):
            root = d
            break
        if weak is None and any((d / m).exists() for m in WEAK_MARKS):
            weak = d
    root = root or weak
    if root is None:
        return {"root": None, "start": str(start), "personas": False, "kb_dir": None, "kb_index": None}
    kb = next((n for n in ("kb", "lit_kb") if (root / n).is_dir()), None)
    index = None
    if kb:
        candidates = [root / kb / name for name in ("README.md", "readme.md")]
        # Windows is case-insensitive: inspect names to preserve the existing spelling.
        names = {p.name for p in (root / kb).iterdir() if p.is_file()}
        hit = next((p for p in candidates if p.name in names), candidates[0])
        index = {"path": str(hit), "exists": hit.is_file()}
    return {"root": str(root), "start": str(start), "personas": (root / "personas").is_dir(), "kb_dir": kb, "kb_index": index}


def assemble(prefix="", loop=None, cwd=None, data=None, skill=None, detect=True, stages=None, kb_actions=None, project_actions=None, principles=None, dispatch_to=None, evaluation_actions=None):
    skill = Path(skill) if skill else Path(__file__).resolve().parent.parent
    parsed = parse_prefix(prefix)
    role, modules, notes = parsed["role"], list(parsed["modules"]), []
    loop_name, dup = None, False
    if loop:
        key = loop.strip().lower()
        if key not in LOOPS:
            raise UsageError(f"未登记的循环「{loop}」：只有 asd（别名 s-a-d、sad 开启查重子模式）")
        loop_name, dup = LOOPS[key]
        if role is None:
            role = "a"
            notes.append("循环由 a 主控：未指定主角色，按 a 装配")
    requested_stages, actions = list(stages or []), list(kb_actions or [])
    dispatch_to = list(dict.fromkeys(dispatch_to or []))
    evaluation_actions = list(dict.fromkeys(evaluation_actions or []))
    for target in dispatch_to:
        if target not in DISPATCH_DEPS:
            raise UsageError("未登记的派发对象：" + str(target))
    if dispatch_to and role != "a":
        raise UsageError("--dispatch-to 只适用于 a 主角色")
    for action in evaluation_actions:
        if action not in EVALUATION_DEPS:
            raise UsageError("未登记的评估动作：" + str(action))
        if role != ("c" if action == "check" else "a"):
            raise UsageError("评估动作与主角色不适用：" + action)
    project_actions = list(dict.fromkeys(project_actions or []))
    for name in project_actions:
        if name not in PROJECT_ACTIONS:
            raise UsageError(f"未登记的项目动作「{name}」：只有 {'/'.join(PROJECT_ACTIONS)}")
    requested_project_actions, project_actions = project_actions, []

    def project_add(name):
        for dep in PROJECT_DEPS.get(name, ()):
            project_add(dep)
        if name not in project_actions:
            project_actions.append(name)

    for name in requested_project_actions:
        project_add(name)
    for name in requested_stages:
        if name not in STAGES:
            raise UsageError(f"未登记的阶段「{name}」：只有 {'/'.join(STAGES)}")
    for name in actions:
        if name not in KB_ACTIONS:
            raise UsageError(f"未登记的 kb 动作「{name}」：只有 {'/'.join(KB_ACTIONS)}")
    if requested_stages and role != "a":
        raise UsageError("--stage 只适用于 a 主角色")
    active_stages = []

    def stage_add(name):
        deps = STAGE_DEPS.get(name, ())
        if not loop_name and name == "dispatch" and dispatch_to:
            deps = tuple(dep for target in dispatch_to for dep in DISPATCH_DEPS[target])
        if not loop_name and name == "evaluate" and evaluation_actions:
            deps = ()
        for dep in deps:
            stage_add(dep)
        if name not in active_stages:
            active_stages.append(name)

    if loop_name and role == "a":
        for name in ("plan", "dispatch", "ideate", "evaluate"):
            stage_add(name)
    for name in requested_stages:
        stage_add(name)
    if dispatch_to:
        stage_add("dispatch")
    if evaluation_actions and role == "a":
        stage_add("evaluate")
    evaluation_parts = []
    if "ideate" in active_stages:
        evaluation_parts.append("context")
    if "evaluate" in active_stages and (loop_name or not evaluation_actions):
        evaluation_parts.extend(EVALUATION_ALL)
    else:
        for action in evaluation_actions:
            evaluation_parts.extend(EVALUATION_DEPS[action])
    evaluation_parts = list(dict.fromkeys(evaluation_parts))
    if any(name in actions for name in ("create", "write", "archive")) and "kb" not in modules:
        modules.append("kb")
    project = detect_project(cwd or os.getcwd()) if detect else {"root": None, "start": None, "personas": False, "kb_dir": None, "kb_index": None}
    if role in ("a", "d", "s") and project["kb_dir"] and "kb" not in modules:
        modules.append("kb")
        notes.append(f"项目根目录有 {project['kb_dir']}/：a、d、s 默认按 kb 联动")
    for alias, name in parsed["aliases"].items():
        notes.append(f"别名 {alias} -> {name}")
    if parsed["snapshot"] and "snapshot" not in actions:
        actions.append("snapshot")
    if "archive" in actions and "write" not in actions:
        actions.append("write")
    if "close" in active_stages and "kb" in modules and "write" not in actions:
        actions.append("write")
    actions = list(dict.fromkeys(actions))
    requested_principles = list(principles or [])
    if "dispatch" in active_stages:
        requested_principles.append("dispatch")
    if actions:
        requested_principles.append("write")
    active_principles = []

    def principle_add(name):
        if name not in PRINCIPLE_ACTIONS:
            raise UsageError(f"未登记的公共原则「{name}」：只有 {'/'.join(PRINCIPLE_ACTIONS)}")
        for dep in PRINCIPLE_DEPS.get(name, ()):
            principle_add(dep)
        if name not in active_principles:
            active_principles.append(name)

    for name in requested_principles:
        principle_add(name)
    secs, seen = [], set()

    def add(rel, heading=None, without=None, preamble=False):
        text = read(skill, rel)
        if preamble:
            lines, spans = sections(text)
            end = next((start for _h, level, start, _end in spans if level == 2), len(lines))
            title, body = "前言", "\n".join(lines[:end]).strip("\n")
        elif heading:
            title, body = cut(text, heading, rel)
        else:
            title, body = text.split("\n", 1)[0], (drop(text, without, rel) if without else text.strip("\n"))
        key = (rel, title)
        if key not in seen:
            seen.add(key)
            secs.append({"file": rel, "heading": title, "text": body})

    if role or active_principles:
        add(ROLES_FILE, preamble=True)
        add(ROLES_FILE, PRINCIPLES)
    if role:
        add("references/role-" + role + ".md", ROLES[role][1])
        if role in ("s", "d", "c", "e"):
            notes.append("直接用该前缀进入时，首行标签后加一行「直接入口，未经 a 判定」（a／p 派发、任务书拉起、为独立审查另开的上下文不加）")
        if role == "e" and parsed["instance"] == "ops":
            notes.append("e#ops 是只读统计实例：严禁改任何专案的业务代码、实验数据与文稿，见 e 段「专用只读／统计实例」")
    for name in active_principles:
        add(COMMON, "## " + name + "：")
    for name in active_stages:
        add(WORKFLOWS, "## " + name + "：")
    for name in evaluation_parts:
        rel = "references/evaluation-" + name + ".md"
        # Require the expected heading even when the complete file is assembled.
        source = read(skill, rel)
        cut(source, EVALUATION_HEADS[name], rel)
        if name == "assess":
            for heading in ("## 场地与代理指标", "## 流程轻重"):
                cut(source, heading, rel)
        add(rel)
    for name in modules:
        add(MODULES[name])
    for name in actions:
        for heading in ACTION_HEADS[name]:
            add(MAINTENANCE, "## " + heading + "：")
    if project_actions:
        add(PROJECT_ENTRY)
        for name in project_actions:
            add(PROJECT_WORKFLOWS, "## " + name + "：")
    if parsed["snapshot"]:
        notes.append("wid: 快照只对本则生效；位置依次为本次指定路径、personas/README.md 的「wid 默认目录」、kb/（或 lit_kb/）下的 snapshots/，都没有就先问")
    if loop_name:
        add(LOOPS_FILE, without=None if dup else DUP_HEADING)
        if dup:
            notes.append("查重子模式：查重摘要经用户确认后才派 d")
    memory, readme = None, None
    if project["root"]:
        root = Path(project["root"])
        readme = {"path": str(root / "personas" / "README.md"), "exists": (root / "personas" / "README.md").is_file()}
        folders = ROLES[role][2] if role else ()
        if folders:
            cands = [root / "personas" / f / "MEMORY.md" for f in folders]
            hit = next((c for c in cands if c.is_file()), cands[0])
            memory = {"path": str(hit), "exists": hit.is_file()}
        if role and role != "p" and not project["personas"]:
            notes.append("项目没有 personas/：首次戴专案主角色时按 project-memory.md「首次提示」提示一次")
    ddir = data_dir(data)
    data_info = {"path": str(ddir), "profile_exists": (ddir / "PROFILE.md").is_file()}
    if role == "p":
        data_info["principal_exists"] = (ddir / "principal").is_dir()
    tag = None
    if role:
        tag = f"〔{role} {ROLES[role][0]}" + (f"#{parsed['instance']}" if parsed["instance"] else "") + \
              (f"/{parsed['question']}" if parsed["question"] else "") + "〕"
    # Pending routes contain locators and triggers, never unloaded rule text.
    pending = []
    if role or modules or actions or active_principles:
        pending += [{"file": COMMON, "heading": "## " + name + "：", "trigger": trigger}
                    for name, trigger in PRINCIPLE_ACTIONS.items() if name not in active_principles]
    if role == "a":
        pending += [{"file": WORKFLOWS, "heading": "## " + name + "：", "trigger": trigger}
                    for name, trigger in STAGES.items() if name not in active_stages]
    if "kb" in modules:
        pending += [{"file": MAINTENANCE, "heading": "## " + name + "：", "trigger": trigger}
                    for name, trigger in KB_ACTIONS.items() if name not in actions]
    if project_actions:
        pending += [{"file": PROJECT_WORKFLOWS, "heading": "## " + name + "：", "trigger": trigger}
                    for name, trigger in PROJECT_ACTIONS.items() if name not in project_actions]
    if evaluation_parts:
        pending += [{"file": "references/evaluation-" + name + ".md", "heading": EVALUATION_HEADS[name],
                     "trigger": "另做 " + name + " 动作前按 evaluation.md 补读完整依赖"}
                    for name in EVALUATION_DEPS if name not in evaluation_actions
                    and name not in evaluation_parts]
    return {
        "version": skill_version(skill), "prefix": prefix or "", "role": role, "instance": parsed["instance"],
        "question": parsed["question"], "modules": modules, "aliases": parsed["aliases"], "snapshot": parsed["snapshot"],
        "loop": loop_name, "dup_check": dup, "tag": tag, "data_dir": data_info,
        "project": dict(project, personas_readme=readme, memory=memory), "notes": notes,
        "stages": active_stages, "kb_actions": actions, "project_actions": project_actions,
        "dispatch_to": dispatch_to, "evaluation_actions": evaluation_actions, "evaluation_parts": evaluation_parts,
        "principles": active_principles, "pending": pending, "sections": secs,
    }


def render(res):
    yes = {True: "存在", False: "不存在"}
    out = [f"<!-- persona-masks {res['version']} · load_mask_context：只读装配，规则以各文件原文为准 -->", "# 装配摘要"]
    if res["tag"]:
        out.append(f"- 首行标签：{res['tag']}")
    out.append(f"- 主角色：{res['role'] or '无（只用共用模块）'}；实例：{res['instance'] or '—'}；问题：{res['question'] or '—'}")
    out.append(f"- 共用模块：{'、'.join(res['modules']) or '无'}" + ("；wid: 快照" if res["snapshot"] else ""))
    if res["loop"]:
        out.append(f"- 循环：{res['loop']}" + ("（查重子模式）" if res["dup_check"] else ""))
    if res["stages"] or res["kb_actions"]:
        out.append(f"- 阶段：{'、'.join(res['stages']) or '无'}；kb 动作：{'、'.join(res['kb_actions']) or '无'}")
    if res["dispatch_to"]:
        out.append("- 派发对象：" + "、".join(res["dispatch_to"]) + "；写计划／冒烟／长任务／估时先补 plan；呼叫／续接 s 补 ideate")
    if res["evaluation_actions"]:
        out.append("- 评估动作：" + "、".join(res["evaluation_actions"]) + "；已读：" + "、".join(res["evaluation_parts"]))
    if res["project_actions"]:
        out.append(f"- 项目动作：{'、'.join(res['project_actions'])}")
    if res["principles"]:
        out.append(f"- 公共动作：{'、'.join(res['principles'])}")
    d = res["data_dir"]
    out.append(f"- 资料目录：{d['path']}（PROFILE.md {yes[d['profile_exists']]}）")
    pj = res["project"]
    if pj["root"]:
        line = f"- 项目根：{pj['root']}；personas/README.md {yes[pj['personas_readme']['exists']]}"
        if pj["memory"]:
            line += f"；{pj['memory']['path']} {yes[pj['memory']['exists']]}"
        line += f"；知识库：{pj['kb_dir'] + '/' if pj['kb_dir'] else '无'}"
        out.append(line)
        if pj["kb_index"]:
            index = pj["kb_index"]
            out.append(f"- KB 索引入口（仅检测，未读取）：{index['path']} {yes[index['exists']]}"
                       + ("；缺索引只列主题文件名／标题，再选择相关主题，不自动建档" if not index["exists"] else ""))
    out += [f"- 提示：{n}" for n in res["notes"]]
    if res["pending"]:
        out.append("- 动作前须补读（跨阶段读齐，中途变化先补读）：")
        out += [f"  - {r['trigger']} → {r['file']} / {r['heading']}" for r in res["pending"]]
    out.append("")
    out.append("# 规则段落")
    for s in res["sections"]:
        out += ["", f"<!-- 来源：{s['file']} · {s['heading']} -->", s["text"]]
    return "\n".join(out) + "\n"


def selftest(skill=None):
    """内置自检：解析与切段，不检测项目、不写文件。"""
    fails = []

    def check(name, cond):
        print(f"[{'通过' if cond else '未通过'}] {name}")
        if not cond:
            fails.append(name)

    def heads(res):
        return [s["heading"] for s in res["sections"]]

    r = assemble("a$wid#Demo/Q1:", skill=skill, detect=False)
    check("a$wid#Demo/Q1：a 常驻段＋分工的原则＋kb 入口，别名 wid->kb", r["role"] == "a" and r["modules"] == ["kb"]
          and r["aliases"] == {"wid": "kb"} and r["tag"] == "〔a 建筑师#Demo/Q1〕"
          and any(h.startswith(PRINCIPLES) for h in heads(r)) and any(h.startswith("## a 建筑师") for h in heads(r))
          and not any(h.startswith("## s 思索者") for h in heads(r)) and any(s["file"] == MODULES["kb"] for s in r["sections"]))
    r = assemble("p#global", skill=skill, detect=False)
    check("p#global：只装 p 段", r["role"] == "p" and r["modules"] == [] and any(h.startswith("## p 幕僚长") for h in heads(r))
          and not any(h.startswith("## a 建筑师") for h in heads(r)))
    r = assemble("a:kis:kb:", skill=skill, detect=False)
    check("a:kis:kb:：冒号连接模块", r["modules"] == ["kis", "kb"])
    r = assemble("kis:", skill=skill, detect=False)
    check("kis:：单用模块", r["role"] is None and r["modules"] == ["kis"])
    r = assemble("wid:", skill=skill, detect=False)
    check("wid:：只装 kb 快照与写入公共边界", r["snapshot"] and r["modules"] == []
          and r["principles"] == ["write"]
          and sum(s["heading"].startswith(SNAPSHOT_HEADING) for s in r["sections"]) == 1
          and not any(s["heading"].startswith("## structure：") for s in r["sections"]))
    r = assemble("a", loop="s-a-d", skill=skill, detect=False)
    check("--loop s-a-d：asd 含查重子模式", r["loop"] == "asd" and r["dup_check"] and DUP_HEADING in r["sections"][-1]["text"])
    r = assemble("a", loop="asd", skill=skill, detect=False)
    check("--loop asd：不含查重子模式", r["loop"] == "asd" and not r["dup_check"] and DUP_HEADING not in r["sections"][-1]["text"])
    r = assemble("", loop="sad", skill=skill, detect=False)
    check("只给循环：按 a 装配", r["role"] == "a" and r["dup_check"])
    r = assemble("e#ops", skill=skill, detect=False)
    check("e#ops：e 段含只读统计实例", r["role"] == "e" and any("e#ops" in s["text"] for s in r["sections"] if s["heading"].startswith("## e")))
    r = assemble("a#paper-ideas", skill=skill, detect=False)
    check("实例名可含连字号", r["instance"] == "paper-ideas")
    r = assemble(" a : kis : kb : ", skill=skill, detect=False)
    check("冒号前后可有空格", r["role"] == "a" and r["modules"] == ["kis", "kb"])
    r = assemble("wid : ", skill=skill, detect=False)
    check("wid : 冒号前空格仍是快照", r["snapshot"])
    for bad in ["smd:", "t:", "a$smd:", "a$t:", "x$kis", "a$foo", "a#-bad", "a#bad-", "a#a--b", "a$$kis", "a/ ", "a/中文", "a/Q-1", "a$k is", "a $kis"]:
        try:
            assemble(bad, skill=skill, detect=False)
            check(f"拒收「{bad}」", False)
        except UsageError:
            check(f"拒收「{bad}」", True)
    try:
        assemble("a", loop="xyz", skill=skill, detect=False)
        check("拒收未登记的循环", False)
    except UsageError:
        check("拒收未登记的循环", True)
    for role in ROLES:
        r = assemble(role, skill=skill, detect=False)
        pre = [s for s in r["sections"] if s["file"] == ROLES_FILE and s["heading"] == "前言"]
        check(f"{role}：前言一次且未夹全篇", len(pre) == 1 and "本包不强制绑定单一供应商" in pre[0]["text"]
              and "## 分工的原则" not in pre[0]["text"])
        if role != "a":
            check(f"{role}：未装 a 细则", not any(s["file"] == WORKFLOWS for s in r["sections"]))
    r = assemble("a", stages=["dispatch", "evaluate", "dispatch"], skill=skill, detect=False)
    check("阶段依赖与去重", set(r["stages"]) == {"plan", "ideate", "dispatch", "evaluate"}
          and len(r["sections"]) == len({(s["file"], s["heading"]) for s in r["sections"]}))
    check("evaluate 包含 options 归档读取边界", "归档里的行只读标题和 a 自己写的理由" in render(r))
    r = assemble("kb", kb_actions=["write"], skill=skill, detect=False)
    check("write 先补 create 路由但不装映射或快照", "扩充前须补读 create" in render(r)
          and not any(s["heading"].startswith(("## create：", SNAPSHOT_HEADING)) for s in r["sections"]))
    r = assemble("kb", kb_actions=["create", "write", "create"], skill=skill, detect=False)
    check("已有 kb 新增卡片：create + write 及结构去重", set(r["kb_actions"]) == {"create", "write"}
          and sum(s["heading"].startswith("## structure：") for s in r["sections"]) == 1)
    r = assemble("kb", kb_actions=["archive"], skill=skill, detect=False)
    check("archive 自动附 write", set(r["kb_actions"]) == {"archive", "write"})
    r = assemble("wid$kb:", skill=skill, detect=False)
    check("快照与 kb 组合可达且去重", r["modules"] == ["kb"] and r["kb_actions"] == ["snapshot"]
          and sum(s["heading"].startswith(SNAPSHOT_HEADING) for s in r["sections"]) == 1)
    for args in ({"stages": ["unknown"]}, {"kb_actions": ["unknown"]}, {"project_actions": ["unknown"]}):
        try:
            assemble("a", skill=skill, detect=False, **args)
            check("拒收未知阶段／动作", False)
        except UsageError:
            check("拒收未知阶段／动作", True)
    for prefix in ("p", "s", "e", "c", "d", "kb", "wid:"):
        try:
            assemble(prefix, stages=["plan"], skill=skill, detect=False)
            check(f"{prefix} 拒收不适用阶段", False)
        except UsageError:
            check(f"{prefix} 拒收不适用阶段", True)
    for prefix in ("", "p", "a", "c", "kb", "kis"):
        r = assemble(prefix, project_actions=["freeze", "freeze"], skill=skill, detect=False)
        check(f"{prefix or '无角色'}：显式项目动作去重且不切角色", r["role"] == parse_prefix(prefix)["role"]
              and r["project_actions"] == ["freeze"]
              and sum(s["file"] == PROJECT_ENTRY for s in r["sections"]) == 1
              and sum(s["file"] == PROJECT_WORKFLOWS for s in r["sections"]) == 1
              and "SHA-256" in render(r))
    r = assemble("a", skill=skill, detect=False)
    check("默认不追加项目入口或细则", not any(s["file"] in (PROJECT_ENTRY, PROJECT_WORKFLOWS) for s in r["sections"]))
    r = assemble("", project_actions=["manage"], skill=skill, detect=False)
    text = render(r)
    check("无角色 manage 独立保全计划编号/归档同意/日常局部更新", r["role"] is None and r["project_actions"] == ["manage"]
          and all(t in text for t in ("多实例项目的计划树编号按实例隔离", "经用户同意移入并标为「搁置」", "日常执行只更新局部法定进度源")))
    r = assemble("", project_actions=["setup", "manage", "setup"], skill=skill, detect=False)
    check("setup单向先附manage并去重", r["project_actions"] == ["manage", "setup"]
          and sum(s["file"] == PROJECT_WORKFLOWS for s in r["sections"]) == 2
          and "项目已有等价文档时" in render(r) and "先问用户记在哪里" in render(r))
    r = assemble("", principles=["git", "write", "git"], skill=skill, detect=False)
    check("单用原则保留常驻、依赖、去重且不切角色", r["role"] is None and r["modules"] == []
          and r["principles"] == ["write", "git"]
          and len(r["sections"]) == len({(s["file"],s["heading"]) for s in r["sections"]})
          and all(x in render(r) for x in ("盲法守门", "外部服务的费用", "c 仍按只读派发")))
    check("dispatch 阶段自动读公共派发", "dispatch" in assemble("a", stages=["dispatch"], skill=skill, detect=False)["principles"])
    check("普通问答不读公共动作正文", not any(s["file"] == COMMON for s in assemble("a", skill=skill, detect=False)["sections"]))
    try:
        assemble("", principles=["unknown"], skill=skill, detect=False)
        check("拒收未知公共原则",False)
    except UsageError:
        check("拒收未知公共原则",True)
    for target, expected in (("s", {"plan", "ideate", "dispatch"}), ("d", {"plan", "dispatch"}),
                             ("c", {"dispatch"}), ("e", {"dispatch"})):
        r = assemble("a", dispatch_to=[target, target], skill=skill, detect=False)
        check("对象依赖 " + target, set(r["stages"]) == expected and r["dispatch_to"] == [target])
    r = assemble("a", stages=["evaluate"], evaluation_actions=["respond"], skill=skill, detect=False)
    check("respond 精确读集", r["stages"] == ["evaluate"] and r["evaluation_parts"] == ["context", "respond"])
    r = assemble("c", evaluation_actions=["check"], skill=skill, detect=False)
    check("c check 不打开 a 阶段", r["stages"] == [] and r["evaluation_parts"] == ["context", "fields", "assess", "check"])
    print("全部通过" if not fails else f"未通过：{fails}")
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="persona-masks 规则按需装配（只读）：按前缀只输出当次要读的规则段落与项目记忆路径。")
    ap.add_argument("prefix", nargs="?", default="", help="调用前缀，如 'a$wid#Demo/Q1'、p#global、'a:kis:kb:'、'wid:'")
    ap.add_argument("--loop", help="循环：asd；s-a-d 或 sad 开启查重子模式")
    ap.add_argument("--stage", action="append", default=[], help="a 阶段（可重复）：" + "/".join(STAGES))
    ap.add_argument("--dispatch-to", action="append", default=[], help="仅 a 派发对象（可重复）：s/d/c/e；不创建代理")
    ap.add_argument("--evaluation-action", action="append", default=[], help="评估动作（可重复）：assess/respond/backfill 仅 a，check 仅 c")
    ap.add_argument("--kb-action", action="append", default=[], help="kb 动作（可重复）：" + "/".join(KB_ACTIONS))
    ap.add_argument("--project-action", action="append", default=[], help="项目动作（可重复）：" + "/".join(PROJECT_ACTIONS))
    ap.add_argument("--principle", action="append", default=[], help="公共动作（可重复）：" + "/".join(PRINCIPLE_ACTIONS))
    ap.add_argument("--cwd", help="项目目录（默认当前目录），用来检测 personas/、MEMORY.md 与 kb/")
    ap.add_argument("--data-dir", help="资料目录（默认 $CODEX_HOME/persona-masks，未设置则 ~/.codex/persona-masks）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--selftest", action="store_true", help="跑内置自检")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        res = assemble(args.prefix, loop=args.loop, cwd=args.cwd, data=args.data_dir, stages=args.stage, kb_actions=args.kb_action, project_actions=args.project_action, principles=args.principle, dispatch_to=args.dispatch_to, evaluation_actions=args.evaluation_action)
    except UsageError as e:
        print(f"无法解析：{e}", file=sys.stderr)
        return 2
    except MissingSection as e:
        print(f"规则文件与脚本不一致：{e}", file=sys.stderr)
        return 3
    if args.json:
        sys.stdout.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
