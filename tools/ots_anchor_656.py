#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ots_anchor_656.py — G9 总闸门：把目录级 Merkle 根台账锚到比特币时间链（OpenTimestamps）。

为什么它是"元验证总闸门"
========================
本仓"什么算通过"最终收敛到两个文件：`tools/.tool_checksums`（代码面）与
`data/supply_chain/merkle_roots.json`（内容面）。前者每批都要重钉（易变），
后者只在受控内容变化时重写。把**后者**的 digest 提交给 OTS（OpenTimestamps）的多个公开比特币聚合日历，
就得到一条"**任何人、任何时间**都能独立复核"的最外层锚点：既不是自写自验，也不依赖本机任何东西。

设计红线（本批坚持四条）
======================
1. **不自己拼 OTS 二进制**。`.ots` 只能由**官方实现**（`ots` CLI 或 `opentimestamps` 库）产出与解析——
   手写序列化再自己"解"一遍属于自写自验，而排队做 G9 就是为了消掉这类洞。
   两者都不可用 ⇒ 走降级，**如实标 `status=pending_anchor`**，绝不产出冒充的 `.ots`。
2. **pending 就是 pending**。日历 submit 成功只表示 digest 已进日历的 Merkle 树；
   拿到比特币区块头证明（bitcoin attestation）才叫 bitcoin_anchored。状态机不许越级叫。
3. **本地时钟不可信**。降级文件里的 `declared_at_local_clock` 标 `clock_trust=none`，
   它不算时间证据，只用来说明"这是什么时候排队待上链的"。
4. **缺依赖不许假红**。可选依赖是 G9 的必要代价，但**没有它也必须能 `--check`**（离线、确定）。

降级产物为什么叫 `.ots.pending.json` 而不是 `.ots`
=================================================
`.ots` 是被 `ots verify` 语义占用的扩展名。没有官方实现时写一个自己编的 `.ots`，
等于把"待办"冒充成"已锚"。所以降级只写 **JSON 登记表 + 上链命令**，让后来的人一条命令补做。

用法
====
    python tools/ots_anchor_656.py --check      # 只读自检（离线确定，门禁用）
    python tools/ots_anchor_656.py --analyze    # 解析现有锚点（判真伪 / 到哪一级）
    python tools/ots_anchor_656.py --stamp      # 真提交到公开日历（联网）⇒ 写 .ots
    python tools/ots_anchor_656.py --upgrade    # 尝试拉 Bitcoin attestation（联网）
    python tools/ots_anchor_656.py --plan       # 降级：只写 .ots.pending.json
    python tools/ots_anchor_656.py --report     # 写 data/656_ots_anchor_report.{md,json}
    python tools/ots_anchor_656.py --json       # 结构化输出到 stdout
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

DEFAULT_TARGET = "data/supply_chain/merkle_roots.json"
OTS_SUFFIX = ".ots"
PENDING_SUFFIX = ".ots.pending.json"
OUT_MD = ROOT / "data" / "656_ots_anchor_report.md"
OUT_JSON = ROOT / "data" / "656_ots_anchor_report.json"

#: 官方 DetachedTimestampFile.HEADER_MAGIC（从 opentimestamps 0.4.5 实测取，
#  作为"本机没装该库时"的兜底期望值——有了它至少能判断"文件头是不是 OTS"，但仍不能解 attestation）
FROZEN_HEADER_MAGIC_HEX = "004f70656e54696d657374616d7073000050726f6f6600bf89e2e884e89294"

#: 冻结的公开聚合日历（与 opentimestamps 库默认聚集器一致；库不可用时用它）
FROZEN_CALENDARS: tuple[str, ...] = (
    "https://alice.btc.calendar.opentimestamps.org",
    "https://bob.btc.calendar.opentimestamps.org",
    "https://a.pool.opentimestamps.org",
    "https://finney.calendar.eternitywall.com",
)

#: verdict → 是否算"已有外部锚"
ANCHORED = {"pending", "bitcoin_anchored"}


# ── 能力探测（决定走"真锚"还是"降级"）──────────────────────────────────────
def have_lib() -> bool:
    try:
        import opentimestamps  # noqa: F401

        return True
    except Exception:  # noqa: BLE001
        return False


def have_cli() -> str | None:
    for name in ("ots", "ots.exe"):
        p = shutil.which(name)
        if p:
            return p
    return None


def engine() -> str:
    return "opentimestamps-lib" if have_lib() else ("ots-cli" if have_cli() else "none")


def calendar_urls() -> list[str]:
    if have_lib():
        try:
            from opentimestamps.calendar import DEFAULT_AGGREGATORS

            urls = sorted(DEFAULT_AGGREGATORS)
            if urls:
                return urls
        except Exception:  # noqa: BLE001
            pass
    return list(FROZEN_CALENDARS)


# ── 基础 ────────────────────────────────────────────────────────────────────
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def expected_magic() -> str:
    if have_lib():
        try:
            from opentimestamps.core.timestamp import DetachedTimestampFile

            return str(DetachedTimestampFile.HEADER_MAGIC.hex())
        except Exception:  # noqa: BLE001
            pass
    return FROZEN_HEADER_MAGIC_HEX


def _deser_ctx(fd: Any) -> Any:
    """包装成本库需要的反序列化上下文（0.4.x 的 `deserialize` 不吃裸 file 对象）。"""
    from opentimestamps.core.serialize import StreamDeserializationContext

    return StreamDeserializationContext(fd)


def _ser_ctx(fd: Any) -> Any:
    from opentimestamps.core.serialize import StreamSerializationContext

    return StreamSerializationContext(fd)


def attestation_kinds(dts: Any) -> list[dict[str, Any]]:
    """把官方 Timestamp 的 attestation 集合摊平成可序列化清单。"""
    out: list[dict[str, Any]] = []
    try:
        atts = list(dts.timestamp.all_attestations())
    except Exception:  # noqa: BLE001
        return out
    for _ts, att in atts:
        name = type(att).__name__
        kind = {"PendingAttestation": "pending",
                "BitcoinBlockHeaderAttestation": "bitcoin"}.get(name, "unknown")
        detail: dict[str, Any] = {}
        for attr in ("uri", "height"):
            v = getattr(att, attr, None)
            if isinstance(v, (bytes, str, int)):
                detail[attr] = v.hex() if isinstance(v, bytes) else v
        out.append({"kind": kind, "type": name, **detail})
    return out


def analyze(target: str = DEFAULT_TARGET, base: Path | None = None) -> dict[str, Any]:
    """解析现有锚点：有没有 / 是不是真 OTS / 覆盖的 digest 对不对 / 到哪一级。"""
    root = base or ROOT
    t = root / target
    ots = t.with_name(t.name + OTS_SUFFIX)
    pend = t.with_name(t.name + PENDING_SUFFIX)
    rep: dict[str, Any] = {
        "target": target,
        "target_exists": t.is_file(),
        "target_bytes": t.stat().st_size if t.is_file() else None,
        "target_sha256": sha256_file(t) if t.is_file() else None,
        "ots_path": str(ots.name),
        "pending_path": str(pend.name),
        "engine": engine(),
        "magic_expected": expected_magic(),
    }
    if not ots.is_file():
        rep["verdict"] = "missing" if not pend.is_file() else "downgraded_json"
        rep["note"] = "没有 .ots 锚点文件" + ("（有降级登记表）" if pend.is_file() else "")
        if pend.is_file():
            j = _read_json(pend)
            rep["downgrade"] = j
            rep["downgrade_matches_target"] = j.get("sha256") == rep["target_sha256"]
        return rep

    raw = ots.read_bytes()
    magic_exp = rep["magic_expected"]
    found = raw[:len(bytes.fromhex(magic_exp))].hex() if magic_exp else None
    rep.update({
        "ots_bytes": len(raw),
        "magic_found": found,
        "magic_ok": bool(magic_exp and found == magic_exp),
        "hex_head": raw[:40].hex(),
    })
    if have_lib():
        try:
            from opentimestamps.core.timestamp import DetachedTimestampFile

            with ots.open("rb") as g:
                dts = DetachedTimestampFile.deserialize(_deser_ctx(g))
            kinds = attestation_kinds(dts)
            covered = dts.file_digest.hex()
            rep.update({
                "parses_with_official_lib": True,
                "covered_digest": covered,
                "covers_target": covered == rep["target_sha256"],
                "attestations": kinds,
            })
            if not rep["covers_target"]:
                rep["verdict"] = "invalid"
                rep["note"] = "文件能解析，但覆盖的 digest 与目标当前内容不符（挂载错对象或文件已变）"
            elif any(k["kind"] == "bitcoin" for k in kinds):
                rep["verdict"] = "bitcoin_anchored"
                rep["note"] = "已含比特币区块头证明：最外层锚成立"
            elif any(k["kind"] == "pending" for k in kinds):
                rep["verdict"] = "pending"
                rep["note"] = "已提交到日历，尚未拿到比特币区块头证明（需 --upgrade）"
            else:
                rep["verdict"] = "invalid"
                rep["note"] = "可解析但不含任何有效 attestation"
            return rep
        except Exception as e:  # noqa: BLE001
            rep["parses_with_official_lib"] = False
            rep["parse_error"] = f"{type(e).__name__}: {str(e)[:160]}"
    else:
        rep["parses_with_official_lib"] = None  # 无引擎 ⇒ 不做 attestation 级断言
        rep["verdict"] = "unverified" if rep["magic_ok"] else "invalid"
        rep["note"] = ("无官方实现：只能校验文件头"
                       + ("（magic 正确）⇒ 判 `unverified`，**不能**据此说它已锚；建议 `pip install opentimestamps-client` 后重判。"
                          if rep["magic_ok"] else
                          "（magic 不符）⇒ 判 `invalid`：连文件头都不是 OTS。"))
        return rep

    rep["verdict"] = "invalid"
    rep["note"] = ("现有 .ots **不是有效的 OpenTimestamps 文件**（magic 与官方 HEADER_MAGIC 不符 / "
                   "官方库解析失败）——它是占位物，不是锚点。")
    return rep


def _read_json(p: Path) -> dict[str, Any]:
    try:
        payload: Any = json.loads(p.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {"_parse_error": f"不是 dict：{type(payload).__name__}"}
    except Exception as e:  # noqa: BLE001
        return {"_parse_error": f"{type(e).__name__}: {str(e)[:120]}"}


def pending_payload(t: Path, target: str, reason: str) -> dict[str, Any]:
    return {
        "ots_anchor_version": "656.1",
        "target": target,
        "bytes": t.stat().st_size if t.is_file() else None,
        "sha256": sha256_file(t) if t.is_file() else None,
        "declared_at_local_clock": dt.datetime.now().isoformat(timespec="seconds"),
        "clock_trust": "none",
        "status": "pending_anchor",
        "reason": reason,
        "calendars": calendar_urls(),
        "how_to_anchor": [
            "python tools/ots_anchor_656.py --stamp    # 提交到公开日历 ⇒ 写真正的 .ots",
            "python tools/ots_anchor_656.py --upgrade  # 等日历入块后拉 Bitcoin attestation",
        ],
        "how_to_verify": [
            "python tools/ots_anchor_656.py --analyze",
            "ots verify <target>.ots -f <target>       # 需要 ots CLI",
        ],
        "note": "本文件**不是** OTS 证明，只是待上链登记表；声称上链必须先产出真正的 .ots。",
    }


def write_pending(target: str, reason: str, base: Path | None = None) -> dict[str, Any]:
    """降级：写"待上链"登记表（**不是** .ots），内含可复制的上链命令。"""
    root = base or ROOT
    t = root / target
    payload = pending_payload(t, target, reason)
    p = t.with_name(t.name + PENDING_SUFFIX)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8", newline="\n")
    return payload


# ── 真锚：stamp / upgrade（联网，非默认路径）────────────────────────────────
def stamp(target: str = DEFAULT_TARGET, calendars: list[str] | None = None) -> dict[str, Any]:
    """用**官方实现**生成 .ots：算文件 digest + 提交到多个日历 ⇒ pending attestation。"""
    t = ROOT / target
    res: dict[str, Any] = {"target": target, "engine": engine(), "calendars": [], "errors": []}
    cli = have_cli()
    if not have_lib() and cli:
        # 官方 CLI 路径：一次 stamp 用默认日历（多日历合并依赖 CLI 自身行为，诚实标注）
        r = subprocess.run([cli, "stamp", str(t)], cwd=str(ROOT),
                           capture_output=True, text=True, check=False)
        ots = t.with_name(t.name + OTS_SUFFIX)
        res["cli_stdout"] = (r.stdout or r.stderr or "")[-400:]
        res["ots_path"] = str(ots.name)
        res.update(analyze(target))
        return res
    if not have_lib():
        res["verdict"] = "no_engine"
        res["errors"].append("既无 ots CLI 也无 opentimestamps 库 ⇒ 拒绝产出 .ots（改用 --plan 降级）")
        return res

    from opentimestamps.calendar import RemoteCalendar
    from opentimestamps.core.op import OpSHA256
    from opentimestamps.core.timestamp import DetachedTimestampFile

    with t.open("rb") as f:
        dts = DetachedTimestampFile.from_fd(OpSHA256(), f)
    digest = dts.file_digest
    res["covered_digest"] = digest.hex()
    urls = calendars or calendar_urls()
    ok = 0
    for url in urls:
        try:
            remote = RemoteCalendar(url).submit(digest)
            if remote is None:
                res["errors"].append(f"{url}: submit 返回 None")
                continue
            dts.timestamp.merge(remote)
            ok += 1
            res["calendars"].append(url)
        except Exception as e:  # noqa: BLE001
            res["errors"].append(f"{url}: {type(e).__name__}: {str(e)[:120]}")
    if not ok:
        res["verdict"] = "submit_failed"
        res["errors"].append("全部日历提交失败 ⇒ 不写 .ots（宁缺勿假）")
        return res
    ots = t.with_name(t.name + OTS_SUFFIX)
    with ots.open("wb") as g:
        dts.serialize(_ser_ctx(g))
    res["ots_path"] = str(ots.name)
    res["ots_bytes"] = ots.stat().st_size
    res.update(analyze(target))  # 用同一套口径复核刚产出的文件
    return res


def upgrade(target: str = DEFAULT_TARGET) -> dict[str, Any]:
    """把 pending 升级为 bitcoin attestation（需日历已把 commitment 打包进区块）。"""
    t = ROOT / target
    ots = t.with_name(t.name + OTS_SUFFIX)
    res: dict[str, Any] = {"target": target, "ots_path": str(ots.name), "upgraded": 0, "errors": []}
    cli = have_cli()
    if not have_lib() and cli:
        r = subprocess.run([cli, "--btc-wallet-disabled", "upgrade", str(ots)],
                           cwd=str(ROOT), capture_output=True, text=True, check=False)
        res["cli_stdout"] = (r.stdout or r.stderr or "")[-400:]
        res.update(analyze(target))
        return res
    if not have_lib():
        res["verdict"] = "no_engine"
        return res

    from opentimestamps.calendar import RemoteCalendar
    from opentimestamps.core.timestamp import DetachedTimestampFile

    with ots.open("rb") as g:
        dts = DetachedTimestampFile.deserialize(_deser_ctx(g))
    # 官方客户端同一套路：对每个 PendingAttestation 回日历 `get/timestamp/<commitment>`，
    # 拿到后 `remote.merge(旧)` 换根；**日历还没打包进区块**时会抛 CommitmentNotFoundError/KeyError
    # ⇒ 那是"还没好"，不是错误（记为 not_ready）。
    ts_root = dts.timestamp
    ok = 0
    not_ready = 0
    try_again = True
    while try_again:
        try_again = False
        for msg, att in list(ts_root.all_attestations()):        # 注意：返回 (msg_bytes, attestation)
            if type(att).__name__ != "PendingAttestation":
                continue
            uri = getattr(att, "uri", None)
            if not uri:
                continue
            try:
                remote = RemoteCalendar(uri).get_timestamp(msg)
            except KeyError:
                not_ready += 1
                continue
            except Exception as e:  # noqa: BLE001
                res["errors"].append(f"{uri}: {type(e).__name__}: {str(e)[:120]}")
                continue
            if remote is None:
                not_ready += 1
                continue
            remote.merge(ts_root)
            ts_root = remote
            ok += 1
            try_again = True
            break
    res["not_ready"] = not_ready
    res["upgraded"] = ok
    dts.timestamp = ts_root
    with ots.open("wb") as g:
        dts.serialize(_ser_ctx(g))
    res.update(analyze(target))
    return res


# ── 自检（门禁）：离线、确定、不联网 ─────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    rep = analyze(DEFAULT_TARGET)
    print(f"  引擎={rep['engine']}｜verdict={rep['verdict']}")
    chk("目标台账存在且 sha256 可算", bool(rep["target_sha256"]), str(rep.get("target_bytes")))
    chk("verdict 不属于 bad 集合（invalid/submit_failed/no_engine 均判 FAIL）",
        rep["verdict"] in ANCHORED | {"downgraded_json", "missing", "unverified"}, rep["verdict"])

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        fake = tmp / "fake.json"
        fake.write_bytes(b'{"a":1}\n')
        # ① 造一个"长得像但不是"的占位物（沿用旧 .ots 的形态）⇒ 必须判 invalid
        magic_hex = expected_magic()
        magic_bytes = bytes.fromhex(magic_hex) if magic_hex else b"\x00OpenTimestamps\x00\x00proof\x00"
        bad = magic_bytes + b"\x64\x08" + hashlib.sha256(fake.read_bytes()).digest() * 2 + b"\x00\x08" + b"\x00" * 40
        (tmp / "fake.json.ots").write_bytes(bad)
        rep2 = analyze("fake.json", base=tmp)
        chk("伪造/占位 .ots 必须判 invalid", rep2["verdict"] == "invalid",
            f"verdict={rep2['verdict']} magic_ok={rep2.get('magic_ok')}")
        (tmp / "fake.json.ots").unlink()          # 清掉占位物，单独验证降级路径
        # ② 降级登记表：写得到、读得回、sha256 与目标一致；改 1 字节 ⇒ 失配
        pay = write_pending("fake.json", reason="selftest", base=tmp)
        chk("降级登记表 sha256 == 目标文件", pay["sha256"] == hashlib.sha256(fake.read_bytes()).hexdigest())
        chk("降级登记表明确标 clock_trust=none", pay.get("clock_trust") == "none")
        chk("降级登记表自称 status=pending_anchor（不冒充已锚）", pay.get("status") == "pending_anchor")
        rep3 = analyze("fake.json", base=tmp)
        chk("只有登记表时 verdict=downgraded_json", rep3["verdict"] == "downgraded_json", rep3["verdict"])
        chk("登记表 sha256 漂移可被检出", bool(rep3.get("downgrade_matches_target")))
        fake.write_bytes(b'{"a":2}\n')
        rep4 = analyze("fake.json", base=tmp)
        chk("目标文件改 1 字节 ⇒ 登记表失配被检出", rep4.get("downgrade_matches_target") is False)

    if rep["verdict"] in ANCHORED:
        chk("真实 .ots 覆盖的 digest = 目标台账当前内容", bool(rep.get("covers_target")),
            str(rep.get("covered_digest"))[:16])
        chk("至少 1 条 attestation", bool(rep.get("attestations")),
            ",".join(sorted({a["kind"] for a in rep.get("attestations", [])})))
    print(f"ots_anchor_656 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


# ── 报告 ────────────────────────────────────────────────────────────────────
def report() -> dict[str, Any]:
    ana = analyze(DEFAULT_TARGET)
    roots_doc = json.loads((ROOT / DEFAULT_TARGET).read_text(encoding="utf-8"))
    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "engine": ana["engine"],
        "calendars": calendar_urls(),
        "target": DEFAULT_TARGET,
        "analyze": ana,
        "note": ("OTS 是**最外层锚**：内层 = tool_integrity（代码面）+ merkle_roots（内容面）；"
                 "OTS 只证明「某个 digest 在某一时刻之前已存在」，pending ≠ 已入块。"),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")
    a = ana
    lines = [
        "# 656 A · OTS 外部锚（G9 总闸门）报告",
        "",
        f"> 生成：{payload['generated_at']}　引擎：`{payload['engine']}`　目标：`{DEFAULT_TARGET}`",
        "",
        "## 一、锚了什么",
        "",
        f"- 目标文件：`{a['target']}`（{a['target_bytes']} 字节）",
        f"- 其 sha256：`{a['target_sha256']}`",
        f"- 该文件内含 {len(roots_doc.get('dirs', {}))} 个受控目录的 Merkle 根"
        f"（{', '.join(sorted(roots_doc.get('dirs', {})))}）",
        "",
        "## 二、当前判定",
        "",
        f"- verdict：**{a['verdict']}**",
        f"- 说明：{a.get('note', '')}",
        f"- 官方实现能否解析：`{a.get('parses_with_official_lib')}`"
        + (f"（{a.get('parse_error')}）" if a.get("parse_error") else ""),
        f"- magic 是否等于官方 HEADER_MAGIC：`{a.get('magic_ok')}`",
        f"- 覆盖的 digest：`{a.get('covered_digest')}`",
        f"- attestations：`{json.dumps(a.get('attestations'), ensure_ascii=False)}`",
        "",
        "## 三、日历与依赖",
        "",
        "- 提交目标（公开 BTC 聚合日历）：",
    ]
    lines += [f"  - `{u}`" for u in payload["calendars"]]
    lines += [
        "",
        "## 四、状态机（不许越级叫）",
        "",
        "| verdict | 含义 | 说明 |",
        "|---|---|---|",
        "| `missing` | 没有 .ots | 尚无任何外部锚 |",
        "| `invalid` | 文件不是有效 OTS | magic 不符 / 官方实现解析失败 / 无 attestation / 挂载对象错 |",
        "| `pending` | 已提交日历、未入块 | digest 已进日历 Merkle 树；比特币证明待 `--upgrade` |",
        "| `bitcoin_anchored` | 已含比特币区块头证明 | 最外层锚成立 |",
        "| `downgraded_json` | 无引擎时的登记表 | **不是**锚点；内含上链命令 |",
        "",
        "## 五、怎么复核（任何人、任何时间）",
        "",
        "```bash",
        "python tools/ots_anchor_656.py --analyze",
        "ots verify data/supply_chain/merkle_roots.json.ots -f data/supply_chain/merkle_roots.json",
        "python tools/ots_anchor_656.py --upgrade     # 联网：拉 Bitcoin attestation",
        "```",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return payload


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="656 A：OTS 比特币时间戳锚（G9 总闸门）")
    ap.add_argument("--target", default=DEFAULT_TARGET)
    ap.add_argument("--analyze", action="store_true", help="解析现有锚点并判定级别")
    ap.add_argument("--stamp", action="store_true", help="真提交到公开日历（联网）")
    ap.add_argument("--upgrade", action="store_true", help="尝试升级为 Bitcoin attestation（联网）")
    ap.add_argument("--plan", action="store_true", help="降级：写 .ots.pending.json")
    ap.add_argument("--check", action="store_true", help="离线自检（门禁）")
    ap.add_argument("--report", action="store_true", help="写 Markdown/JSON 报告")
    ap.add_argument("--json", action="store_true", help="结构化输出到 stdout")
    a = ap.parse_args(argv)

    if a.check:
        return selftest()
    if a.analyze:
        rep = analyze(a.target)
        if a.json:
            print(json.dumps(rep, ensure_ascii=False, indent=2))
        else:
            print(f"[ots656] verdict={rep['verdict']}｜{rep.get('note','')}")
            print(f"         target_sha256={rep.get('target_sha256')}")
            print(f"         engine={rep['engine']}")
        return 0 if rep["verdict"] in ANCHORED else 1
    if a.stamp:
        rep = stamp(a.target)
        if a.json:
            print(json.dumps(rep, ensure_ascii=False, indent=2))
        else:
            print(f"[ots656] stamp ⇒ verdict={rep.get('verdict')}　覆盖={str(rep.get('covered_digest'))[:16]}　"
                  f"提交成功日历 {len(rep.get('calendars', []))} 个　错误 {len(rep.get('errors', []))} 条")
            for e in rep.get("errors", [])[:6]:
                print(f"         ! {e}")
        return 0 if rep.get("verdict") in ANCHORED else 1
    if a.upgrade:
        rep = upgrade(a.target)
        if a.json:
            print(json.dumps(rep, ensure_ascii=False, indent=2))
        else:
            print(f"[ots656] upgrade ⇒ verdict={rep.get('verdict')}　升级 {rep.get('upgraded')} 条"
                  f"　错误 {len(rep.get('errors', []))} 条")
        return 0
    if a.plan:
        write_pending(a.target, reason="人工降级：--plan 显式请求（无引擎或不想联网）")
        print(f"[ots656] 已写 {a.target}{PENDING_SUFFIX}（**不是**锚点，只是待上链登记表）")
        return 0
    if a.report:
        pay = report()
        print(f"[ots656] 报告已写：{OUT_MD.name} / {OUT_JSON.name}"
              f"（verdict={pay['analyze']['verdict']}）")
        return 0
    rep = analyze(a.target)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(f"[ots656] verdict={rep['verdict']}"
              f"（加 --analyze/--stamp/--upgrade/--plan/--check/--report 之一）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
