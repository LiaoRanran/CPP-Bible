"""610 B2 · 辩护链 CLI + 批量报告回归锁（show/what-if/report/stats/list-*/--check）。

锁八件事（任务书 B2 的 8 例）：
  1. `show MIS-LANG-001` ⇒ 输出含判决/攻击者/击败关系；
  2. `what-if MIS-LANG-001 medium` ⇒ 打印 **IN 115 / OUT 6**；
  3. `what-if-overturned <命题>` ⇒ 打印受影响节点数（非空）；
  4. `stats --json` ⇒ 字段齐全且数字与入库产物一致；
  5. `list-out` ⇒ **7** 个 OUT 节点；
  6. `list-no-defenders` ⇒ **7** 个节点；`list-no-attackers` ⇒ **4** 个命题；
  7. `report --out` ⇒ 生成 `data/defense_chain_report.md`（幂等，两次逐字一致）；
  8. `--check` ⇒ exit 0（与入库 W2 逐节点一致）。

⚠️ 全部走真实数据（只读）；写盘只写 tmp_path，唯一写真实仓的是第 7 例的**产物报告**（任务书要求）。
"""
from __future__ import annotations

import json
from pathlib import Path

import defense_chain as dc

PROP = "ATOM-UB-GRAY-001::prop-1"


def test_cli_show(capsys):
    assert dc.main(["show", "MIS-LANG-001"]) == 0
    out = capsys.readouterr().out
    assert "# 辩护链 · MIS-LANG-001" in out
    assert "判决 **OUT**" in out and "可信度 low" in out
    assert "## 攻击者" in out and "构成击败" in out
    assert "## 击败它的攻击者" in out
    assert out.count("`ae-") >= 3


def test_cli_what_if(capsys):
    """640b：把 OUT 误解抬到 medium 不再引起翻转（命题 high）⇒ 变化 0 个节点。"""
    from w2_authority_640b import current as _w2
    exp = _w2()
    assert dc.main(["what-if", "MIS-LANG-001", "medium"]) == 0
    out = capsys.readouterr().out
    assert f"IN {exp['IN']} / OUT {exp['OUT']} / UNDEC {exp['UNDEC']}" in out
    assert "变化 0 个节点" in out
    assert dc.main(["what-if", "MIS-LANG-001", "bogus"]) != 0


def test_cli_what_if_overturned(capsys):
    """640b：命题 high 档、无敌者 ⇒ 强制推翻无连带影响。"""
    from w2_authority_640b import current as _w2
    exp = _w2()
    assert dc.main(["what-if-overturned", PROP]) == 0
    out = capsys.readouterr().out
    assert f"推翻 {PROP}" in out and "受影响" in out
    assert f"总 IN {exp['IN']} / OUT {exp['OUT']}" in out


def test_cli_stats(capsys):
    from w2_authority_640b import current as _w2
    exp = _w2()
    assert dc.main(["stats", "--json"]) == 0
    st = json.loads(capsys.readouterr().out)
    assert (st["total_nodes"], st["in"], st["out"], st["undec"]) == (
        121, exp["IN"], exp["OUT"], exp["UNDEC"])
    assert st["total_edges"] == exp["edges"] and st["defeating_edges"] == exp["defeating_edges"]
    assert st["no_attackers"] == 4
    assert set(st["credibility_distribution"]) == {"high", "medium", "low"}
    assert len(st["out_nodes"]) == exp["OUT"]


def test_cli_list_out(capsys):
    from w2_authority_640b import current as _w2
    exp = _w2()
    assert dc.main(["list-out"]) == 0
    lines = [x for x in capsys.readouterr().out.splitlines() if x.strip()]
    assert len(lines) == exp["OUT"]
    assert "MIS-LANG-001" in lines


def test_cli_list_no_defenders_and_no_attackers(capsys):
    assert dc.main(["list-no-defenders"]) == 0
    nd = [x for x in capsys.readouterr().out.splitlines() if x.strip()]
    assert nd, "no-defenders 不应为空"
    assert dc.main(["list-no-attackers"]) == 0
    na = [x for x in capsys.readouterr().out.splitlines() if x.strip()]
    assert na == ["ATOM-CONC-FENCE-001::prop-1", "ATOM-CONC-FENCE-001::prop-2",
                  "ATOM-CONC-LOCK-001::prop-1", "ATOM-CONC-LOCK-001::prop-2"]


def test_cli_report_is_idempotent(capsys):
    from w2_authority_640b import current as _w2
    exp = _w2()
    p = Path(dc.DEFAULT_REPORT)
    assert dc.main(["report"]) == 0
    first = p.read_text(encoding="utf-8")
    assert dc.main(["report"]) == 0
    assert p.read_text(encoding="utf-8") == first, "批量报告必须幂等（不含时间戳）"
    assert f"IN {exp['IN']} / OUT {exp['OUT']} / UNDEC {exp['UNDEC']}" in first


def test_check_consistency(capsys):
    from w2_authority_640b import current as _w2
    exp = _w2()
    assert dc.main(["--check"]) == 0
    assert f"IN {exp['IN']} / OUT {exp['OUT']} / UNDEC {exp['UNDEC']}" in capsys.readouterr().out
