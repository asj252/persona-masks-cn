#!/usr/bin/env python3
"""persona-masks 规则按需装配（只读、可选）。

按调用前缀解析主角色、共用模块、实例、问题与循环，只输出当次要读的规则段落
（当前一个主角色段与「分工的原则」、已启用模块、当次循环）与项目记忆路径，
供宿主或命令行装配提示词。规则以各参考文件原文为准，本脚本只按标题切段。
只用 Python 3.8 以上的标准库；只读文件，不写文件、不联网、不执行别的命令。

用法（在任意目录执行，路径按本文件所在的 skill 目录解析）：
  python3 scripts/load_mask_context.py 'a$wid#Demo/Q1'
  python3 scripts/load_mask_context.py p#global --json
  python3 scripts/load_mask_context.py a --loop s-a-d --cwd <项目目录>
  python3 scripts/load_mask_context.py 'wid:'          # kb 的单次问答快照
  python3 scripts/load_mask_context.py --selftest      # 内置自检
别名：模块 wid -> kb（`wid` 写在开头、前面没有 `$` 时是快照）、t -> smd；循环 s-a-d、sad -> asd（查重子模式）。
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
MODULES = {"kis": "references/kis.md", "smd": "references/smd.md", "kb": "references/kb.md"}
MODULE_ALIASES = {"wid": "kb", "t": "smd"}
LOOPS = {"asd": ("asd", False), "s-a-d": ("asd", True), "sad": ("asd", True)}
LOOPS_FILE = "references/loops.md"
DUP_HEADING = "## 查重子模式"
SNAPSHOT_HEADING = "## 4. `wid`"
NAME_RE = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\Z")
QUESTION_RE = re.compile(r"[A-Za-z0-9]+\Z")
HEADING_RE = re.compile(r"(#{1,6}) ")


class UsageError(Exception):
    """前缀或参数无法解析。"""


class MissingSection(Exception):
    """规则文件里找不到要切的段落。"""


def parse_prefix(prefix):
    """解析 `角色[$模块…][#实例][/问题]:`，也接受冒号连接模块（`a:kis:smd:`）与只用模块（`kb:`、`$kis`、`wid:`）。"""
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
        return {"root": None, "start": str(start), "personas": False, "kb_dir": None}
    kb = next((n for n in ("kb", "lit_kb") if (root / n).is_dir()), None)
    return {"root": str(root), "start": str(start), "personas": (root / "personas").is_dir(), "kb_dir": kb}


def assemble(prefix="", loop=None, cwd=None, data=None, skill=None, detect=True):
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
    project = detect_project(cwd or os.getcwd()) if detect else {"root": None, "start": None, "personas": False, "kb_dir": None}
    if role in ("a", "d", "s") and project["kb_dir"] and "kb" not in modules:
        modules.append("kb")
        notes.append(f"项目根目录有 {project['kb_dir']}/：a、d、s 默认按 kb 联动")
    for alias, name in parsed["aliases"].items():
        notes.append(f"别名 {alias} -> {name}")
    secs = []

    def add(rel, heading=None, without=None):
        text = read(skill, rel)
        if heading:
            title, body = cut(text, heading, rel)
        else:
            title, body = text.split("\n", 1)[0], (drop(text, without, rel) if without else text.strip("\n"))
        secs.append({"file": rel, "heading": title, "text": body})

    if role:
        add(ROLES_FILE, PRINCIPLES)
        add(ROLES_FILE, ROLES[role][1])
        if role in ("s", "d", "c", "e"):
            notes.append("直接用该前缀进入时，首行标签后加一行「直接入口，未经 a 判定」（a／p 派发、任务书拉起、为独立审查另开的上下文不加）")
        if role == "e" and parsed["instance"] == "ops":
            notes.append("e#ops 是只读统计实例：严禁改任何专案的业务代码、实验数据与文稿，见 e 段「专用只读／统计实例」")
    for name in modules:
        add(MODULES[name])
    if parsed["snapshot"]:
        if "kb" not in modules:
            add(MODULES["kb"], SNAPSHOT_HEADING)
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
    return {
        "version": skill_version(skill), "prefix": prefix or "", "role": role, "instance": parsed["instance"],
        "question": parsed["question"], "modules": modules, "aliases": parsed["aliases"], "snapshot": parsed["snapshot"],
        "loop": loop_name, "dup_check": dup, "tag": tag, "data_dir": data_info,
        "project": dict(project, personas_readme=readme, memory=memory), "notes": notes, "sections": secs,
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
    d = res["data_dir"]
    out.append(f"- 资料目录：{d['path']}（PROFILE.md {yes[d['profile_exists']]}）")
    pj = res["project"]
    if pj["root"]:
        line = f"- 项目根：{pj['root']}；personas/README.md {yes[pj['personas_readme']['exists']]}"
        if pj["memory"]:
            line += f"；{pj['memory']['path']} {yes[pj['memory']['exists']]}"
        line += f"；知识库：{pj['kb_dir'] + '/' if pj['kb_dir'] else '无'}"
        out.append(line)
    out += [f"- 提示：{n}" for n in res["notes"]]
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
    check("a$wid#Demo/Q1：a 段＋分工的原则＋kb 全文，别名 wid->kb", r["role"] == "a" and r["modules"] == ["kb"]
          and r["aliases"] == {"wid": "kb"} and r["tag"] == "〔a 建筑师#Demo/Q1〕"
          and any(h.startswith(PRINCIPLES) for h in heads(r)) and any(h.startswith("## a 建筑师") for h in heads(r))
          and not any(h.startswith("## s 思索者") for h in heads(r)) and any(s["file"] == MODULES["kb"] for s in r["sections"]))
    r = assemble("p#global", skill=skill, detect=False)
    check("p#global：只装 p 段", r["role"] == "p" and r["modules"] == [] and any(h.startswith("## p 幕僚长") for h in heads(r))
          and not any(h.startswith("## a 建筑师") for h in heads(r)))
    r = assemble("a:kis:smd:", skill=skill, detect=False)
    check("a:kis:smd:：冒号连接模块", r["modules"] == ["kis", "smd"])
    r = assemble("t:", skill=skill, detect=False)
    check("t:：别名 t->smd，只用模块", r["role"] is None and r["modules"] == ["smd"])
    r = assemble("wid:", skill=skill, detect=False)
    check("wid:：只装 kb 的快照一节", r["snapshot"] and r["modules"] == [] and len(r["sections"]) == 1
          and r["sections"][0]["heading"].startswith(SNAPSHOT_HEADING))
    r = assemble("a", loop="s-a-d", skill=skill, detect=False)
    check("--loop s-a-d：asd 含查重子模式", r["loop"] == "asd" and r["dup_check"] and DUP_HEADING in r["sections"][-1]["text"])
    r = assemble("a", loop="asd", skill=skill, detect=False)
    check("--loop asd：不含查重子模式", r["loop"] == "asd" and not r["dup_check"] and DUP_HEADING not in r["sections"][-1]["text"])
    r = assemble("", loop="sad", skill=skill, detect=False)
    check("只给循环：按 a 装配", r["role"] == "a" and r["dup_check"])
    r = assemble("e#ops", skill=skill, detect=False)
    check("e#ops：e 段含只读统计实例", r["role"] == "e" and "e#ops" in r["sections"][1]["text"])
    r = assemble("a#paper-ideas", skill=skill, detect=False)
    check("实例名可含连字号", r["instance"] == "paper-ideas")
    r = assemble(" a : kis : smd : ", skill=skill, detect=False)
    check("冒号前后可有空格", r["role"] == "a" and r["modules"] == ["kis", "smd"])
    r = assemble("wid : ", skill=skill, detect=False)
    check("wid : 冒号前空格仍是快照", r["snapshot"])
    for bad in ["x$kis", "a$foo", "a#-bad", "a#bad-", "a#a--b", "a$$kis", "a/ ", "a/中文", "a/Q-1", "a$k is", "a $kis"]:
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
    print("全部通过" if not fails else f"未通过：{fails}")
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="persona-masks 规则按需装配（只读）：按前缀只输出当次要读的规则段落与项目记忆路径。")
    ap.add_argument("prefix", nargs="?", default="", help="调用前缀，如 'a$wid#Demo/Q1'、p#global、'a:kis:smd:'、'wid:'")
    ap.add_argument("--loop", help="循环：asd；s-a-d 或 sad 开启查重子模式")
    ap.add_argument("--cwd", help="项目目录（默认当前目录），用来检测 personas/、MEMORY.md 与 kb/")
    ap.add_argument("--data-dir", help="资料目录（默认 $CODEX_HOME/persona-masks，未设置则 ~/.codex/persona-masks）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--selftest", action="store_true", help="跑内置自检")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        res = assemble(args.prefix, loop=args.loop, cwd=args.cwd, data=args.data_dir)
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
