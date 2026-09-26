"""644 头部层 · 共享数据模型与基础设施（纯标准库 + PyYAML）。

定义：
- 证据等级 L1–L5 与可信度评分（启发式，阈值可人审调整，见 §十二.2）。
- 证据记录（内容寻址）：`EvidenceID = SHA256(canonical content)`。
- 证据库存储：`data/evidence_store/<hash前2位>/<hash>`（不可变，新证据=新 EvidenceID）。
- 原子卡 / 现有证据解析（只读，绝不修改受控目录）。

铁律（§零.1/§九.1/§九.2）：本模块及所有 644 工具**绝不修改**受控目录
（atoms/evidence/Examples/Book）。头部层只在 `data/evidence_store/` 与
`data/evidence_index.json` 等 644 自有产物上工作。

`--check` 只读幂等：`selftest()` 不写盘、exit 0。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

import yaml  # 仓库依赖 PyYAML（pyproject dependencies）

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

ATOMS_DIR = os.path.join(ROOT, "atoms")
EVIDENCE_DIR = os.path.join(ROOT, "evidence")
STORE_DIR = os.path.join(ROOT, "data", "evidence_store")
INDEX_FILE = os.path.join(ROOT, "data", "evidence_index.json")

GRADES = ("L1", "L2", "L3", "L4", "L5")
GRADE_DESC: dict[str, str] = {
    "L1": "实测：多编译器版本实测、可复现实验",
    "L2": "权威：ISO 标准、标准委员会决议、编译器官方文档",
    "L3": "共识：cppreference、Stack Overflow 高赞、多博客一致",
    "L4": "单点：单篇博客、个人经验、单一来源",
    "L5": "未验证：AI 生成、无来源、无法追溯",
}
#: 等级 → 默认可信度基线（启发式，可人审调整）
GRADE_CREDIBILITY: dict[str, float] = {
    "L1": 0.95, "L2": 0.90, "L3": 0.70, "L4": 0.50, "L5": 0.10,
}


def sha256_text(content: str) -> str:
    """计算规范化证据内容的 SHA256（内容寻址的 EvidenceID）。"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


@dataclass
class EvidenceRecord:
    """一条证据记录（内容寻址、不可变）。

    `evidence_id` 由 `content` 推导；元数据独立于内容，但不参与 hash。
    """

    evidence_id: str
    content: str
    source_type: str
    grade: str
    credibility: float
    acquired_at: str
    acquisition_method: str
    source_url: Optional[str] = None
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "EvidenceRecord":
        return cls(
            evidence_id=str(d["evidence_id"]),
            content=str(d.get("content", "")),
            source_type=str(d.get("source_type", "")),
            grade=str(d.get("grade", "L5")),
            credibility=float(d.get("credibility", 0.0)),
            acquired_at=str(d.get("acquired_at", "")),
            acquisition_method=str(d.get("acquisition_method", "")),
            source_url=d.get("source_url"),
            meta=d.get("meta", {}) or {},
        )

    def is_valid(self) -> bool:
        return (
            self.evidence_id == sha256_text(self.content)
            and self.grade in GRADES
            and 0.0 <= self.credibility <= 1.0
        )


def store_evidence(
    content: str,
    *,
    source_type: str,
    grade: str,
    credibility: float,
    acquired_at: str,
    acquisition_method: str,
    source_url: Optional[str] = None,
    meta: Optional[dict[str, Any]] = None,
) -> EvidenceRecord:
    """内容寻址写入（不可变）。已存在同 ID 且同内容则幂等返回。"""
    eid = sha256_text(content)
    rec = EvidenceRecord(
        evidence_id=eid, content=content, source_type=source_type, grade=grade,
        credibility=float(credibility), acquired_at=acquired_at,
        acquisition_method=acquisition_method, source_url=source_url, meta=meta or {},
    )
    path = os.path.join(STORE_DIR, eid[:2], eid)
    if os.path.exists(path):
        existing = load_evidence(eid)
        if existing is not None and existing.content == content:
            return existing
        raise ValueError(f"EvidenceID 冲突但内容不同: {eid}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec.to_dict(), fh, ensure_ascii=False, indent=2, sort_keys=True)
    return rec


def load_evidence(evidence_id: str) -> Optional[EvidenceRecord]:
    path = os.path.join(STORE_DIR, evidence_id[:2], evidence_id)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return EvidenceRecord.from_dict(json.load(fh))


def iter_stored() -> list[EvidenceRecord]:
    out: list[EvidenceRecord] = []
    if not os.path.isdir(STORE_DIR):
        return out
    for hh in os.listdir(STORE_DIR):
        sub = os.path.join(STORE_DIR, hh)
        if not os.path.isdir(sub):
            continue
        for fn in os.listdir(sub):
            if len(fn) == 64:
                rec = load_evidence(fn)
                if rec is not None:
                    out.append(rec)
    return out


def store_path(evidence_id: str) -> str:
    """内容寻址存储路径：`<STORE_DIR>/<前2位>/<hash>`。"""
    return os.path.join(STORE_DIR, evidence_id[:2], evidence_id)


def verify_stored() -> list[tuple[str, str]]:
    """校验所有已存证据：返回 [(evidence_id, 问题)]；空列表=全部自洽（不可变）。"""
    problems: list[tuple[str, str]] = []
    for rec in iter_stored():
        if not rec.is_valid():
            problems.append((rec.evidence_id, "hash/等级/可信度不自洽"))
    return problems


def parse_frontmatter(path: str) -> tuple[dict[str, Any], str]:
    """解析 YAML frontmatter；返回 (meta, body)。缺失 frontmatter 时 meta={}。"""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm = text[3:end].strip("\n")
    body = text[end + 4:]
    try:
        meta = yaml.safe_load(fm) or {}
    except yaml.YAMLError:
        meta = {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, body


def list_atoms() -> list[dict[str, Any]]:
    """列出所有原子卡：{id, rel, path, meta, body, evidence_refs}。只读。"""
    out: list[dict[str, Any]] = []
    for domain in ("conc", "hist", "lang", "mem", "ub"):
        d = os.path.join(ATOMS_DIR, domain)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(d, fn)
            meta, body = parse_frontmatter(p)
            refs = _extract_evidence_refs(meta)
            out.append({
                "id": str(meta.get("id", fn)),
                "rel": os.path.relpath(p, ROOT).replace(os.sep, "/"),
                "path": p, "meta": meta, "body": body,
                "evidence_refs": refs,
            })
    return out


def _extract_evidence_refs(meta: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    cs = meta.get("claim_structured")
    if isinstance(cs, list):
        for item in cs:
            if isinstance(item, dict):
                ev = item.get("evidence")
                if isinstance(ev, list):
                    refs.extend(str(x) for x in ev)
                elif isinstance(ev, str):
                    refs.append(ev)
    return refs


def list_existing_evidence() -> list[dict[str, Any]]:
    """列出现有 evidence/ 下的证据文件（只读，绝不修改）。"""
    out: list[dict[str, Any]] = []
    if not os.path.isdir(EVIDENCE_DIR):
        return out
    for domain in ("conc", "hist", "lang", "mem", "ub"):
        d = os.path.join(EVIDENCE_DIR, domain)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(d, fn)
            meta, body = parse_frontmatter(p)
            out.append({
                "id": str(meta.get("id", fn)),
                "rel": os.path.relpath(p, ROOT).replace(os.sep, "/"),
                "path": p, "meta": meta, "body": body,
                "serves": meta.get("serves") or [],
            })
    return out


def grade_from_source(source_type: str, *, compilers: int = 1,
                      independent_sources: int = 1) -> tuple[str, float]:
    """启发式等级与可信度（详见 _arch_v30/00_synthesis.md 设计输入）。

    映射（原型级，阈值可人审调整，§十二.2）：
    - compiler_run 且多编译器(≥2) → L1；单编译器 → L2（实测但缺交叉）
    - iso_standard / committee / official_doc → L2
    - cppreference / so_high / multi_blog → L3
    - single_blog / personal → L4
    - ai_generated / none → L5
    可信度 = 等级基线 × 多源/多编译器微调（封顶 1.0）。
    """
    st = (source_type or "").lower()
    if st == "compiler_run":
        grade = "L1" if compilers >= 2 else "L2"
    elif st in ("iso_standard", "committee", "official_doc"):
        grade = "L2"
    elif st in ("cppreference", "so_high", "multi_blog"):
        grade = "L3"
    elif st in ("single_blog", "personal"):
        grade = "L4"
    else:
        grade = "L5"
    base = GRADE_CREDIBILITY[grade]
    bonus = min(0.05 * (independent_sources - 1), 0.1)
    if st == "compiler_run" and compilers >= 2:
        bonus = max(bonus, 0.03 * (compilers - 1))
    cred = min(1.0, round(base + bonus, 4))
    return grade, cred


def source_type_from_ev(kind: str, compilers: int = 1) -> str:
    """把现有证据 kind 映到 source_type（供 grade_from_source 使用）。"""
    k = (kind or "").lower()
    if k in ("run", "asm", "layout", "abi", "symbol", "bench", "sanitizer", "godbolt"):
        return "compiler_run"
    if k == "traceable_argument":
        return "multi_blog"
    return "single_blog"


def grade_evidence_record(source_type: str, *, compilers: int = 1,
                          independent_sources: int = 1) -> tuple[str, float]:
    """对外暴露的等级判定（直接复用 grade_from_source 启发式）。"""
    return grade_from_source(source_type, compilers=compilers,
                             independent_sources=independent_sources)


def grade_existing_evidence() -> list[dict[str, Any]]:
    """对现有 evidence/ 下每条证据分级（只读）。"""
    out: list[dict[str, Any]] = []
    for e in list_existing_evidence():
        meta = e["meta"]
        compilers = len(meta.get("matrix", {}).get("compiler", [])) or 1
        st = source_type_from_ev(meta.get("kind", ""), compilers)
        indep = 2 if st == "multi_blog" else 1
        grade, cred = grade_evidence_record(st, compilers=compilers, independent_sources=indep)
        out.append({
            "id": e["id"], "kind": meta.get("kind", ""), "source_type": st,
            "compilers": compilers, "grade": grade, "credibility": cred,
            "verdict": str(meta.get("verdict", "")),
            "artifact_sha256_present": bool(meta.get("artifact_sha256")),
            "serves": meta.get("serves") or [],
        })
    return out


def card_evidence_map() -> dict[str, list[dict[str, Any]]]:
    """构建 卡 → 证据列表（含分级）的多对多映射（只读）。

    来源：现有 evidence/ 文件的 `serves` 字段 + 原子卡 `claim_structured[].evidence`。
    返回 {card_id: [graded_ev_dict, ...]}。
    """
    ev_by_id = {e["id"]: e for e in grade_existing_evidence()}
    # 先以 evidence 的 serves 为主
    m: dict[str, list[dict[str, Any]]] = {}
    for eid, e in ev_by_id.items():
        for card in e["serves"]:
            m.setdefault(str(card), []).append(e)
    # 再以原子卡引用补全（避免 serves 缺失导致漏关联）
    for a in list_atoms():
        cid = a["id"]
        for ref in a["evidence_refs"]:
            ev = ev_by_id.get(ref)
            if ev is not None and ev not in m.get(cid, []):
                m.setdefault(cid, []).append(ev)
    return m


def selftest() -> int:
    """只读幂等自检（不写盘）。返回 0 表示通过。"""
    assert sha256_text("abc") == sha256_text("abc")
    assert len(sha256_text("x")) == 64
    g, c = grade_from_source("compiler_run", compilers=2)
    assert g == "L1" and c > 0.9
    g2, _ = grade_from_source("ai_generated")
    assert g2 == "L5"
    assert GRADES == ("L1", "L2", "L3", "L4", "L5")
    assert source_type_from_ev("run", 1) == "compiler_run"
    recs = grade_existing_evidence()
    assert len(recs) > 0 and all(r["grade"] in GRADES for r in recs)
    assert isinstance(card_evidence_map(), dict)
    return 0


if __name__ == "__main__":
    sys.exit(selftest())
