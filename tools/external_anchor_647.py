"""647 A4 · **外部锚接口**（只建接口 + 本地 mock；**不真连任何外部服务**）。

为什么（647 §一 / 642 B1「独立性四级 L1–L4」）：本仓库锚定仍是 **L2** —— RSA 密钥在本地、
透明日志 anchor 也在本地 ⇒ **改仓库就能同时改日志和 anchor**。真正独立需要把 anchor
**发布到仓库之外**（第三方可查）。647 只做**接口 + 本地 mock**，不选服务（交人裁决）。

接口（§三 A4）：
```python
publish(hash) -> receipt          # 把 hash 发布给锚服务，拿回凭据
verify(hash, receipt) -> bool     # 第三方凭 hash + receipt 独立验证
```

三种**预留接入点**（**只登记，不实现**，各自 `publish/verify` 抛 `AnchorNotImplemented`）：

| 提供方 | 为什么是候选 | 需要人提供 |
|---|---|---|
| GitHub Gist | 免费、有公开时间戳、可 git 化 | token + gist id/scope |
| RFC 3161 时间戳服务 | 标准时间戳（第三方 TSA 签名） | TSA URL + 是否付费 |
| OpenTimestamps（比特币） | 去中心化、可自证 | 是否接受链上成本/延迟 |

**本地 mock（本批实现）**：`MockAnchor` —— 确定性凭据（`receipt_id` + `receipt_digest` 可重算），
`verify()` 对**改 hash / 换 receipt / 改凭据字段** 全部检出（不联网、纯标准库）。

**诚实登记（§十二.1）**：
1. **本批不真连外部服务** ⇒ 独立性**没有实际提升**，只把"能不能接"变成"接得上"的结构就绪；
2. 本地 mock **不是**独立锚 —— 它和日志在**同一台机器、同一个仓库**里，
   真正的 L3/L4 必须由**仓库外**的第三方持有（交人裁决用哪个服务）；
3. `verify()` 只能证明"这份 receipt 与这个 hash 自洽"，
   **不能**证明"发布者真的在那一刻发布过"（那是 TSA/区块链的职责）。

CLI：`--check`（只读自检）/ `--report`（写 `data/647_external_anchor.md` + 发布示例凭据）/
`--publish`（把当前透明日志 anchor 发布到本地 mock 并验证）/ `--json`。纯标准库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import transparency_log_628 as tlog  # noqa: E402  （透明日志单一真源，不复制）

OUT_MD = os.path.join(ROOT, "data", "647_external_anchor.md")
OUT_JSON = os.path.join(ROOT, "data", "647_external_anchor_receipts.json")

MOCK_PROVIDER = "mock-local"

#: 预留接入点（**只登记不实现**；`implemented=False`）
RESERVED_PROVIDERS: tuple[dict[str, Any], ...] = (
    {"name": "github-gist", "implemented": False,
     "requires": ["token", "gist_id"], "public_verifiable": True,
     "note": "免费/可公开查；凭据是 gist revision，git 化后天然有时间线"},
    {"name": "rfc3161-timestamp", "implemented": False,
     "requires": ["tsa_url", "预算确认"], "public_verifiable": True,
     "note": "标准第三方时间戳（TSA 签名）；需要人选 TSA 并确认是否付费"},
    {"name": "opentimestamps", "implemented": False,
     "requires": ["是否接受链上成本/延迟"], "public_verifiable": True,
     "note": "去中心化、可自证；确认成本与延迟后接入"},
)


class AnchorNotImplemented(NotImplementedError):
    """647 A4：预留接入点**未实现**（显式拒绝，不静默降级成 mock）。"""


def _canonical(d: dict[str, Any]) -> str:
    return json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class AnchorProvider:
    """锚服务接口（所有提供方共用）。"""

    name = "abstract"
    implemented = False

    def publish(self, h: str) -> dict[str, Any]:
        raise AnchorNotImplemented(f"{self.name}：本批只建接口，未实现")

    def verify(self, h: str, receipt: dict[str, Any]) -> bool:
        raise AnchorNotImplemented(f"{self.name}：本批只建接口，未实现")


class ReservedAnchor(AnchorProvider):
    """预留接入点：**能构造、能自述、调用即抛**（不假装能用）。"""

    def __init__(self, spec: dict[str, Any]) -> None:
        self.name = str(spec["name"])
        self.requires = list(spec.get("requires", []))
        self.note = str(spec.get("note", ""))
        self.implemented = False

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "implemented": False,
                "requires": self.requires, "note": self.note}


class MockAnchor(AnchorProvider):
    """本地 mock 锚（**离线、确定性**）：凭据可重算 ⇒ 篡改必被检出。

    `publish()` 是**纯函数**（同一 (hash, published_at) ⇒ 同一凭据），便于单测与复算。
    """

    name = MOCK_PROVIDER
    implemented = True

    def publish(self, h: str, published_at: Optional[str] = None) -> dict[str, Any]:
        if not isinstance(h, str) or len(h) < 16:
            raise ValueError(f"hash 形态可疑（要求 ≥16 位字符串）：{h!r}")
        ts = published_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        core: dict[str, Any] = {"provider": self.name, "hash": h, "published_at": ts}
        receipt: dict[str, Any] = dict(core)
        receipt["receipt_id"] = _sha256_text(_canonical(core))    # 全 64 位（不截断，避免自比不对称）
        receipt["receipt_digest"] = _sha256_text(_canonical(receipt))
        return receipt

    def verify(self, h: str, receipt: dict[str, Any]) -> bool:
        if not isinstance(receipt, dict) or not isinstance(h, str):
            return False
        if receipt.get("provider") != self.name or receipt.get("hash") != h:
            return False
        body: dict[str, Any] = dict(receipt)
        digest = body.pop("receipt_digest", None)
        rid = body.get("receipt_id")
        if not isinstance(digest, str) or not isinstance(rid, str) or not digest or not rid:
            return False
        core: dict[str, Any] = {k: body[k] for k in ("provider", "hash", "published_at")
                                if k in body}
        if _sha256_text(_canonical(core)) != rid:
            return False
        # `receipt_digest` 覆盖**除它自己之外**的全部字段（含 receipt_id）⇒ 改任一字段即失配
        return _sha256_text(_canonical(body)) == digest


def providers() -> list[AnchorProvider]:
    """全部提供方：本地 mock（已实现）+ 3 个预留接入点（调用即抛）。"""
    return [MockAnchor()] + [ReservedAnchor(dict(s)) for s in RESERVED_PROVIDERS]


def get_provider(name: str) -> AnchorProvider:
    for p in providers():
        if p.name == name:
            return p
    raise KeyError(f"未知锚提供方：{name}（可选：{[p.name for p in providers()]}）")


# ── 契约级接口（模块函数，§三 A4 要求的两条）────────────────────────────────────
def publish(h: str, provider: str = MOCK_PROVIDER,
            published_at: Optional[str] = None) -> dict[str, Any]:
    """把 `hash` 发布给锚提供方，返回 receipt。非 mock 提供方 ⇒ `AnchorNotImplemented`。"""
    p = get_provider(provider)
    if isinstance(p, MockAnchor):
        return p.publish(h, published_at=published_at)
    return p.publish(h)


def verify(h: str, receipt: dict[str, Any]) -> bool:
    """凭 hash + receipt 独立验证（fail-closed）。

    返回 `False` 的四种情形：receipt 不是 dict / 提供方未知 / **提供方未实现**（无法验证 ⇒ 不认）/
    凭据与 hash 不自洽。**直接调用未实现提供方的 `provider.verify()`** 才抛 `AnchorNotImplemented`
    （`verify()` 是门面，不把"验不了"伪装成"验过了"，也不让调用方因未实现而崩溃）。
    """
    if not isinstance(receipt, dict):
        return False
    name = str(receipt.get("provider", ""))
    try:
        p = get_provider(name)
    except KeyError:
        return False
    if not getattr(p, "implemented", False):
        return False
    return p.verify(h, receipt)


def transparency_anchor() -> dict[str, Any]:
    """当前透明日志的 anchor（= 末条 `entry_hash`；空日志 ⇒ GENESIS）。"""
    entries = tlog._read_log()
    if not entries:
        return {"anchor": "", "n_entries": 0, "log_index": None}
    last = entries[-1]
    return {"anchor": str(last.get("entry_hash", "")), "n_entries": len(entries),
            "log_index": last.get("log_index")}


def publish_current_anchor(published_at: Optional[str] = None) -> dict[str, Any]:
    """把**当前透明日志 anchor** 发布到本地 mock，并当场验证可验（A4 的落地动作）。"""
    a = transparency_anchor()
    if not a["anchor"]:
        return {"anchor": None, "published": False, "verified": False,
                "reason": "透明日志为空 ⇒ 无可发布 anchor（不编造）"}
    receipt = publish(a["anchor"], MOCK_PROVIDER, published_at=published_at)
    return {"anchor": a, "receipt": receipt, "published": True,
            "verified": verify(a["anchor"], receipt),
            "tamper_detected": (not verify(a["anchor"] + "0", receipt))}


def interface_spec() -> dict[str, Any]:
    return {"contract": {"publish": "publish(hash: str) -> receipt: dict",
                         "verify": "verify(hash: str, receipt: dict) -> bool"},
            "implemented": [MOCK_PROVIDER],
            "reserved": [dict(s) for s in RESERVED_PROVIDERS],
            "real_external_service_connected": False}


def write_report(published_at: Optional[str] = None) -> str:
    spec = interface_spec()
    cur = publish_current_anchor(published_at=published_at)
    lines = [
        "# 647 A4 · 外部锚接口（**只建接口 + 本地 mock，不真连外部服务**）", "",
        "## 一、接口契约", "",
        "```python",
        "publish(hash) -> receipt          # 发布，拿回凭据",
        "verify(hash, receipt) -> bool     # 第三方凭 hash + 凭据独立验证",
        "```", "",
        "## 二、提供方", "",
        "| 提供方 | 已实现 | 需要人提供 | 说明 |", "|---|---|---|---|",
        f"| `{MOCK_PROVIDER}` | ✅ | — | 本地 mock：确定性凭据，篡改必检出（**不是独立锚**） |",
    ]
    for s in spec["reserved"]:
        lines.append(f"| `{s['name']}` | ⛔ 只留接入点 | {', '.join(s['requires'])} | {s['note']} |")
    lines += ["", "## 三、把当前透明日志 anchor 发布到本地 mock", ""]
    if cur["published"]:
        a = cur["anchor"]
        lines += [f"- 透明日志：**{a['n_entries']}** 条，末条 index={a['log_index']}",
                  f"- anchor（末条 entry_hash）：`{a['anchor']}`",
                  f"- receipt：`{json.dumps(cur['receipt'], ensure_ascii=False)}`",
                  f"- **验证可验：{cur['verified']}**；改一个字符 ⇒ 检出：{cur['tamper_detected']}"]
    else:
        lines.append(f"- {cur['reason']}")
    lines += ["", "## 四、独立性的真实状态（不夸大）", "",
              "| 级别 | 定义 | 本仓库 |", "|---|---|---|",
              "| L1 | 同进程自证 | ❌ |",
              "| L2 | 同机独立进程/独立实现 | ✅ 已达（628/629 他验三件套） |",
              "| L3 | 仓库外第三方可验（外部锚/TSA） | ⛔ **未达**（A4 只建接口） |",
              "| L4 | 外部权威机构背书 | ⛔ 未达 |", "",
              "## 诚实登记", "",
              "1. **不真连外部服务**：本批没有联网、没有 token、没有 TSA ⇒ "
              "**独立性没有实际提升**（§十二.1）；",
              "2. **本地 mock 不是独立锚**：它与日志同机同仓库 ⇒ 改仓库仍能同时改两者；",
              "3. `verify()` 只证明「receipt 与 hash 自洽」，**不能**证明「发布者真在那一刻发布过」；",
              "4. 三个接入点的 `publish/verify` **调用即抛 `AnchorNotImplemented`**"
              "（显式拒绝，不会静默退化成 mock）；",
              "5. 用哪个服务是**交人裁决**（GitHub Gist / RFC3161 / OpenTimestamps）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"spec": spec, "current": cur}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    h = "a" * 64
    r = publish(h, published_at="2026-09-26T00:00:00Z")
    chk("publish 返回 receipt", r.get("provider") == MOCK_PROVIDER and r.get("hash") == h)
    chk("receipt 含 id + digest（均 64 位）", len(str(r.get("receipt_id"))) == 64
        and len(str(r.get("receipt_digest"))) == 64)
    chk("verify(hash, receipt) = True", verify(h, r) is True)
    chk("确定性：同参 ⇒ 同凭据", publish(h, published_at="2026-09-26T00:00:00Z") == r)
    chk("换 hash ⇒ 检出", verify("b" * 64, r) is False)

    # 篡改凭据的每种字段 ⇒ 都必须检出
    for field, bad in (("receipt_id", "0" * 64), ("receipt_digest", "0" * 64),
                       ("published_at", "1999-01-01T00:00:00Z"),
                       ("provider", "github-gist"), ("hash", "c" * 64)):
        t = dict(r)
        t[field] = bad
        chk(f"篡改 {field} ⇒ 检出", verify(h, t) is False)
    not_a_dict: Any = None
    chk("空 dict / 非 dict ⇒ False", verify(h, {}) is False and verify(h, not_a_dict) is False)

    # 预留接入点：调用即抛（不静默降级）
    for s in RESERVED_PROVIDERS:
        p = get_provider(str(s["name"]))
        chk(f"预留点 {s['name']} 未实现", p.implemented is False)
        try:
            p.publish(h)
            chk(f"预留点 {s['name']} 调用即抛", False)
        except AnchorNotImplemented:
            chk(f"预留点 {s['name']} 调用即抛", True)
    chk("契约两条在（publish/verify）", callable(publish) and callable(verify))

    a = transparency_anchor()
    chk("透明日志 anchor 可读", a["n_entries"] >= 1 and len(a["anchor"]) == 64)
    cur = publish_current_anchor(published_at="2026-09-26T00:00:00Z")
    chk("当前 anchor 发布后可验", cur["published"] is True and cur["verified"] is True)
    chk("当前 anchor 篡改可检出", cur["tamper_detected"] is True)
    chk("未连外部服务（诚实）", interface_spec()["real_external_service_connected"] is False)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"A4 anchor selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 A4 外部锚接口（mock + 预留接入点）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + 发布示例凭据")
    ap.add_argument("--publish", action="store_true", help="把当前透明日志 anchor 发布到本地 mock")
    ap.add_argument("--json", action="store_true", help="打印当前 anchor 的发布结果")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    cur = publish_current_anchor()
    if a.json or a.publish:
        print(json.dumps(cur, ensure_ascii=False, indent=2))
        return 0 if cur.get("verified") else 1
    spec = interface_spec()
    print(f"[external-anchor] 已实现 {spec['implemented']}；预留 "
          f"{[s['name'] for s in spec['reserved']]}；真连外部服务="
          f"{spec['real_external_service_connected']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
