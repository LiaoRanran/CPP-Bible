"""626 C2 · 镜像边审计回归测试（≥4 例）。"""
import sys

ROOT = __import__("os").path.dirname(__import__("os").path.dirname(
    __import__("os").path.abspath(__file__)))
sys.path.insert(0, ROOT + "/tools")
import mirror_edge_audit_626 as M  # noqa: E402


def test_selftest_passes():
    assert M.selftest() == 0


def test_mirror_edge_count():
    a = M.audit()
    assert a["total_candidates"] == 388
    assert a["mirror_edges"] == 194


def test_all_mirror_edges_have_symmetry_proof_id_field():
    """判据 9：所有镜像边都有 symmetry_proof_id 字段（值可为 null）。"""
    a = M.audit()
    assert a["records_have_field"]
    assert len(a["records"]) == a["mirror_edges"]
    assert all("symmetry_proof_id" in r for r in a["records"])


def test_no_verified_symmetry_proof_yet():
    """诚实：当前无已验证的 symmetry proof ⇒ 镜像边不可作为已验证事实。"""
    a = M.audit()
    assert a["with_symmetry_proof"] == 0
    assert a["without_symmetry_proof"] == a["mirror_edges"]
