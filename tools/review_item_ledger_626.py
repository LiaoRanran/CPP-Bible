"""626 B3 · 唯一审查账本（93 unique，**禁止重复计数**）

**根治 P0-B**：624 的「80 新增 + 30 = 110」只是**记录条数**相加，不是唯一复核对象数量。
实测：615 = 30 唯一、624 = 80 唯一、overlap = 17 ⇒ **union = 93**。

规则：
- `review_item_id = RI-<target_type>-<target_id>` **全局唯一**
- 同一 `target_id` 的多次审查 = 不同的 `review_revision`（旧 revision 被 `supersedes`）
- `add()` 遇到已存在且 `status=pending` 的 target：**不新建**，只更新 `last_seen_at`

纯标准库；`--check` 验证账本完整性（唯一性 / 状态机 / 迁移结果）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LEDGER_PATH = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
L615 = os.path.join(ROOT, "data", "human_review_item_by_item_30_615.md")
L624 = os.path.join(ROOT, "data", "human_review_item_by_item_624.md")

STATUSES = ("pending", "in_review", "decided", "superseded", "invalid")
PRIORITIES = ("high", "medium", "low")


@dataclass
class ReviewItem:
    review_item_id: str = ""
    review_revision: int = 1
    target_type: str = "edge"
    target_id: str = ""
    target_revision: str = ""
    first_seen_at: str = ""
    last_seen_at: str = ""
    symmetry_proof_id: str = ""      # 镜像边对称性证明（默认空=未验证；C2 使用）
    supersedes: list = field(default_factory=list)
    status: str = "pending"
    current_decision_id: str = ""
    ambiguity_score: float = 0.5
    priority: str = "medium"
    source_batch: str = ""
    tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "ReviewItem":
        known = set(ReviewItem.__dataclass_fields__)  # type: ignore[attr-defined]
        return ReviewItem(**{k: v for k, v in d.items() if k in known})


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def item_id(target_type: str, target_id: str, revision: int = 1) -> str:
    """`RI-<target_type>-<target_id>`；revision > 1 时追加 `-r<N>` 以保证**全局唯一**。"""
    base = f"RI-{target_type}-{target_id}"
    return base if revision <= 1 else f"{base}-r{revision}"


class ReviewItemLedger:
    def __init__(self) -> None:
        self._items: list[ReviewItem] = []      # 全部记录（含历史 revision）

    # ── 写 ──
    def add(self, item: ReviewItem) -> str:
        """添加或合并；返回生效的 review_item_id。"""
        existing = self.get_by_target(item.target_type, item.target_id)
        now = _now()
        if existing is not None and existing.status == "pending":
            # 同一 target 的重复出现：不新建，只更新 last_seen_at / 合并来源
            existing.last_seen_at = now
            if item.source_batch and item.source_batch not in (existing.source_batch or ""):
                existing.source_batch = "+".join(
                    sorted({*existing.source_batch.split("+"), *item.source_batch.split("+")}
                           - {""}))
            return existing.review_item_id
        if existing is not None:
            # 已 decided/其他状态 ⇒ 新 revision，取代旧的
            item.review_revision = existing.review_revision + 1
            item.supersedes = list(item.supersedes or []) + [existing.review_item_id]
        if not item.review_item_id:
            item.review_item_id = item_id(item.target_type, item.target_id,
                                          item.review_revision)
        if not item.first_seen_at:
            item.first_seen_at = now
        item.last_seen_at = now
        self._items.append(item)
        return item.review_item_id

    # ── 读 ──
    def get(self, review_item_id: str) -> Optional[ReviewItem]:
        for it in self._items:
            if it.review_item_id == review_item_id:
                return it
        return None

    def get_by_target(self, target_type: str, target_id: str) -> Optional[ReviewItem]:
        hits = [it for it in self._items
                if it.target_type == target_type and it.target_id == target_id]
        return hits[-1] if hits else None

    def get_all_pending(self) -> list[ReviewItem]:
        return [it for it in self._items if it.status == "pending"]

    def get_unique_count(self) -> int:
        """唯一审查对象数（按 target 去重）。"""
        return len({(it.target_type, it.target_id) for it in self._items})

    def get_record_count(self) -> int:
        """记录总数（含历史 revision / 重复出现）。"""
        return len(self._items)

    def all_items(self) -> list[ReviewItem]:
        return list(self._items)

    def sorted_by_ambiguity(self, desc: bool = True) -> list[ReviewItem]:
        return sorted(self._items, key=lambda it: it.ambiguity_score, reverse=desc)

    def mark_decided(self, review_item_id: str, decision_event_id: str) -> bool:
        it = self.get(review_item_id)
        if it is None:
            return False
        it.status = "decided"
        it.current_decision_id = decision_event_id
        return True

    # ── 校验 ──
    def verify_uniqueness(self) -> bool:
        """无重复的 pending item（同一 target 只能有一条 pending）。"""
        pend = [(it.target_type, it.target_id) for it in self._items
                if it.status == "pending"]
        return len(pend) == len(set(pend))

    def verify_statuses(self) -> bool:
        return all(it.status in STATUSES for it in self._items)

    # ── IO ──
    def export_jsonl(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for it in self._items:
                fh.write(json.dumps(it.to_dict(), ensure_ascii=False) + "\n")
        return path

    @classmethod
    def import_jsonl(cls, path: str) -> "ReviewItemLedger":
        led = cls()
        if not os.path.exists(path):
            return led
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    led._items.append(ReviewItem.from_dict(json.loads(line)))
        return led


# ── 迁移 ──
def _edge_ids(path: str) -> list[str]:
    if not os.path.exists(path):
        return []
    txt = open(path, encoding="utf-8").read()
    seen: list[str] = []
    for m in re.findall(r"ae-[A-Za-z0-9_:\->.]+", txt):
        if m not in seen:
            seen.append(m)
    return seen


def migrate() -> tuple[ReviewItemLedger, dict]:
    """从 615(30) + 624(80) 清单迁移到唯一审查账本。"""
    led = ReviewItemLedger()
    a, b = set(_edge_ids(L615)), set(_edge_ids(L624))
    records = 0
    now = _now()
    # 先加 615，再加 624（overlap 会在 add() 中被合并，不新建）
    for batch, ids in (("615", sorted(a)), ("624", sorted(b))):
        for eid in ids:
            it = ReviewItem(target_type="edge", target_id=eid,
                            source_batch=batch, priority="high",
                            ambiguity_score=0.8 if batch == "615" else 0.6,
                            tags=["migrated", f"from_{batch}"],
                            first_seen_at=now, last_seen_at=now)
            led.add(it)
            records += 1
    # overlap 的项补标 "615+624"
    overlap = a & b
    for eid in sorted(overlap):
        ov_item: Optional[ReviewItem] = led.get_by_target("edge", eid)
        if ov_item is not None:
            ov_item.source_batch = "615+624"
            ov_item.ambiguity_score = 0.9
            if "overlap" not in ov_item.tags:
                ov_item.tags.append("overlap")
    stats = {"from_615": len(a), "from_624": len(b), "overlap": len(overlap),
             "records": records, "unique": led.get_unique_count(),
             "ledger_records": led.get_record_count()}
    return led, stats


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    led, st = migrate()
    chk("615 唯一 30", st["from_615"] == 30, f"({st['from_615']})")
    chk("624 唯一 80", st["from_624"] == 80, f"({st['from_624']})")
    chk("overlap 17", st["overlap"] == 17, f"({st['overlap']})")
    chk("**唯一 93**", st["unique"] == 93, f"({st['unique']})")
    chk("记录条数 110", st["records"] == 110, f"({st['records']})")
    chk("账本 item 数 = 唯一 93（重复被合并）",
        st["ledger_records"] == 93, f"({st['ledger_records']})")
    chk("唯一性验证通过", led.verify_uniqueness())
    chk("状态合法", led.verify_statuses())
    chk("pending 数 = 93", len(led.get_all_pending()) == 93)

    # 去重行为：重复 add 同 target 不新建
    n0 = led.get_record_count()
    dup = ReviewItem(target_type="edge", target_id=sorted(
        {it.target_id for it in led.all_items()})[0], source_batch="626")
    led.add(dup)
    chk("重复 add 同 target 不新建记录", led.get_record_count() == n0)

    # revision / supersedes
    it0 = led.all_items()[0]
    new = ReviewItem(target_type="edge", target_id=it0.target_id, source_batch="627")
    led.mark_decided(it0.review_item_id, "AE-000001-abcdef12")
    rid = led.add(new)
    it_new = led.get(rid)
    chk("新 revision 递增", it_new is not None and it_new.review_revision == 2)
    chk("新 revision supersedes 旧的",
        it_new is not None and it0.review_item_id in (it_new.supersedes or []))
    chk("mark_decided 生效",
        bool(it0.status == "decided" and it0.current_decision_id))

    # 导出/导入往返
    import tempfile
    led2, st2 = migrate()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "r.jsonl")
        led2.export_jsonl(p)
        led3 = ReviewItemLedger.import_jsonl(p)
    chk("导出/导入条数一致", led3.get_record_count() == led2.get_record_count())
    chk("导入后唯一性成立", led3.verify_uniqueness())
    print(f"B3 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 B3 唯一审查账本")
    ap.add_argument("--check", action="store_true", help="账本完整性自检（只读）")
    ap.add_argument("--run", action="store_true", help="执行迁移并写出账本")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    led, st = migrate()
    if args.run:
        led.export_jsonl(LEDGER_PATH)
        print(f"ledger -> {LEDGER_PATH}")
    print(json.dumps(st, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
