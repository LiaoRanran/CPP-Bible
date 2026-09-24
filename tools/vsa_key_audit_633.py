"""633 C1 · vsa_secret.key 备份 + 影响评估（**默认不轮换**）

任务书 §六.C1 / §零.14：**先评估影响，再决定是否轮换**；无论是否轮换都**先备份**；
**默认不轮换**（只有显式 `--rotate` 才换，且换前自动备份）。

- 影响评估：扫全仓找出引用 `data/vsa_secret.key` 的工具；统计 `data/vsa/` 下已签发的
  VSA 凭证数（轮换后旧凭证需用**备份旧钥**验证）。
- 备份：`data/vsa/vsa_secret.key.backup_20260924`，校验 sha256 与原文件一致。
- **gitignore 加固**（632 G1 发现 ignore 过窄）：覆盖 `data/vsa_secret.key*` 与 `data/vsa/*.key*`。

**密钥内容绝不打印**：只输出 sha256 前 12 位（用于一致性核对）。
**只读契约**：`--check` 只读、exit 0、不写盘；`--backup`/`--rotate`/`--report` 才写盘。
纯标准库；≥5 例单测（tests/test_vsa_key_audit_633.py）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

KEY = os.path.join(ROOT, "data", "vsa_secret.key")
VSA_DIR = os.path.join(ROOT, "data", "vsa")
BACKUP = os.path.join(VSA_DIR, "vsa_secret.key.backup_20260924")
GITIGNORE = os.path.join(ROOT, ".gitignore")
OUT_MD = os.path.join(ROOT, "data", "vsa_key_audit_633.md")

REQUIRED_IGNORES = ("data/vsa_secret.key*", "data/vsa/*.key*")


def sha256_head(path: str, n: int = 12) -> str:
    if not os.path.exists(path):
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:n]


def find_references() -> list[tuple[str, int, str]]:
    """扫全仓（tools/ + data/）找出引用 vsa_secret.key 的位置。"""
    out: list[tuple[str, int, str]] = []
    for base in ("tools", "data"):
        for r, dirs, files in os.walk(os.path.join(ROOT, base)):
            dirs[:] = [d for d in dirs if d not in (".pytest_tmp", "__pycache__")]
            for f in files:
                if not f.endswith((".py", ".md", ".json", ".txt")):
                    continue
                p = os.path.join(r, f)
                try:
                    for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                        if "vsa_secret.key" in line and "backup" not in line:
                            out.append((os.path.relpath(p, ROOT).replace(os.sep, "/"), i,
                                        line.strip()[:90]))
                except OSError:
                    continue
    return out


def count_vsa_creds() -> int:
    if not os.path.isdir(VSA_DIR):
        return 0
    return sum(1 for f in os.listdir(VSA_DIR)
               if f.startswith("attestation_") and f.endswith(".json"))


def gitignore_coverage() -> dict[str, Any]:
    txt = open(GITIGNORE, encoding="utf-8", errors="replace").read() if os.path.exists(GITIGNORE) else ""
    lines = [ln.strip() for ln in txt.splitlines()]
    cov = {pat: (pat in lines) for pat in REQUIRED_IGNORES}
    return {"patterns": cov, "covered": all(cov.values()),
            "note": "data/vsa_secret.key 原来已忽略（窄）；需加宽到 key* 与 data/vsa/*.key*"}


def backup(dry: bool = False) -> dict[str, Any]:
    if not os.path.exists(KEY):
        return {"ok": False, "reason": "密钥不存在"}
    src_hash = sha256_head(KEY)
    if not dry:
        os.makedirs(VSA_DIR, exist_ok=True)
        shutil.copy2(KEY, BACKUP)
    bk_hash = sha256_head(BACKUP)
    return {"ok": (bk_hash == src_hash), "backup": os.path.relpath(BACKUP, ROOT).replace(os.sep, "/"),
            "src_sha12": src_hash, "backup_sha12": bk_hash, "consistent": bk_hash == src_hash}


def rotate(force: bool = False) -> dict[str, Any]:
    """**默认不轮换**：只有显式调用（--rotate）才生成新钥；换前自动备份。"""
    if not force:
        return {"rotated": False, "reason": "默认不轮换（需显式 --rotate，§零.14）"}
    r = backup()
    if not r.get("ok"):
        return {"rotated": False, "reason": "备份未成功，拒绝轮换"}
    with open(KEY, "wb") as fh:
        fh.write(os.urandom(32))
    return {"rotated": True, "new_key_sha12": sha256_head(KEY), "backup": r["backup"]}


def write_report() -> str:
    refs = find_references()
    b = backup(dry=True)
    g = gitignore_coverage()
    creds = count_vsa_creds()
    lines = [
        "# 633 C1 · vsa_secret.key 备份 + 影响评估（默认不轮换）", "",
        "## 一、影响评估：谁在用这把钥", "",
        f"- 引用 `vsa_secret.key` 的位置：**{len(refs)}** 处", "",
        "| 文件 | 行 | 片段 |", "|---|---|---|"]
    for f, i, s in refs[:30]:
        lines.append(f"| `{f}` | {i} | `{s}` |")
    lines += ["",
              "## 二、轮换影响", "",
              f"- `data/vsa/` 下已签发 VSA 凭证：**{creds}** 张（`attestation_*.json`）。",
              "- **若轮换**：这些旧凭证的 HMAC 用旧钥签发，换钥后**新钥验证会失败**；"
              "旧钥保留在备份中即可用于**历史凭证验证**——但需验证端支持指定旧钥（当前工具"
              "硬编码路径 `data/vsa_secret.key`，不自动读备份）。",
              "- 结论：**轮换会导致历史凭证默认不可验**（需人工把备份钥放回或改验证端支持 key_id）"
              "⇒ 影响评估判定为**较高**，**默认不轮换**（交人裁决）。", "",
              "## 三、备份状态", "",
              f"- 密钥存在：**{os.path.exists(KEY)}**；sha256 前 12 位：`{b.get('src_sha12', '')}`",
              f"- 备份目标：`{b.get('backup', '')}`（本次为只读评估，未写）",
              "- 备份动作由 `--backup` 执行（复制 + sha256 一致性校验）。", "",
              "## 四、gitignore 加固（632 G1 发现过窄）", "",
              "| 需覆盖模式 | 当前是否存在 |", "|---|---|"]
    for pat, ok in g["patterns"].items():
        lines.append(f"| `{pat}` | {'✅' if ok else '❌（需加）'} |")
    lines += ["",
              "## 五、轮换决策", "",
              "- **默认不轮换**（§零.14）。`--rotate` 才会执行：先备份 → 再写 32 字节新钥。",
              "- 是否轮换交人裁决（见 §交人项）。", "",
              "## 六、诚实登记", "",
              "1. **未轮换密钥**（默认关闭，符合 §零.14）；",
              "2. **密钥内容全程未打印**，只输出 sha256 前 12 位用于一致性核对；",
              "3. 影响评估为**静态**（按文件引用 + 凭证计数），未实跑「换钥后旧凭证验证失败」"
              "的端到端复现；",
              "4. gitignore 加宽后需复核 `git check-ignore` 对真实密钥生效。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("密钥文件存在", os.path.exists(KEY))
    chk("备份评估结构", set(backup(dry=True)) >= {"ok", "backup", "consistent"})
    chk("默认不轮换（force=False）", rotate(force=False)["rotated"] is False)
    chk("引用扫描非空", len(find_references()) >= 1)
    chk("gitignore 覆盖结构", set(gitignore_coverage()) >= {"patterns", "covered"})
    chk("VSA 凭证计数为整数", isinstance(count_vsa_creds(), int))
    chk("报告路径在 data 下（--check 不写）", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="633 C1 vsa_secret.key 备份+影响评估")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--backup", action="store_true", help="执行备份（复制 + sha256 校验）")
    ap.add_argument("--rotate", action="store_true", help="显式轮换（默认不做）")
    ap.add_argument("--report", action="store_true", help="写 data/vsa_key_audit_633.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.rotate:
        r = rotate(force=True)
        print(json.dumps(r, ensure_ascii=False))
        return 0 if r.get("rotated") else 1
    if args.backup:
        r = backup()
        print(json.dumps(r, ensure_ascii=False))
        return 0 if r.get("ok") else 1
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps({"refs": len(find_references()), "creds": count_vsa_creds(),
                          "gitignore": gitignore_coverage()}, ensure_ascii=False, indent=2))
        return 0
    print(f"refs={len(find_references())} creds={count_vsa_creds()} "
          f"gitignore_covered={gitignore_coverage()['covered']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
