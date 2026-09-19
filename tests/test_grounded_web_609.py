"""609 C2 · 论证 Web 回归锁（6 页面 + 5 JSON API + 只读 + 只绑回环）。

测试用 `make_server(port=0)` 挑空口 + 线程常驻 + `urllib` 取数 ⇒ 不占固定端口、不对外暴露。
锁五件事（任务书 5 例 + 2 例自加）：
  1. 6 个页面都能 200 且各自有特征串；
  2. 5 个 JSON API 都能 parse 出预期字段；
  3. **只读**：handler 不 一度打开写盘（静态断言：源码零 `open(..., "w")`）；
  4. **只绑回环**：传非回环 host ⇒ **拒绝启动**（SystemExit）；
  5. 未知路径 404、缺 nodes 的坏文档 ⇒ 500 且不甩栈给浏览器；
  +. 机器拿 API 与肉眼见页面必须一致（summary 的 IN 数两边同值）。
"""
from __future__ import annotations

import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import grounded_web as gw
import pytest

DOC = gw.load_doc()


@pytest.fixture(scope="module")
def server():
    srv = gw.make_server(0, gw.DEFAULT_HOST)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield srv
    srv.shutdown()
    srv.server_close()


def _get(server: ThreadingHTTPServer, path: str) -> tuple[int, str]:
    """GET 本机回环（127.0.0.1 + 随机端口 ⇒ 不对外暴露；404/500 也取回正文便于断言）。"""
    url = f"http://127.0.0.1:{server.server_address[1]}{path}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:                   # noqa
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:          # 4xx/5xx 在 urllib 里是异常，但正文有用
        body = e.read().decode("utf-8", "replace") if e.fp else ""
        return e.code, body


@pytest.mark.parametrize("path,marker", [
    ("/", "论证总览"),
    ("/nodes", "节点一览"),
    ("/edges", "边列表"),
    ("/mis", "MIS 组"),
    ("/report", "论证报告"),
    ("/node/MIS-CONC-003", "节点 MIS-CONC-003"),
])
def test_six_pages_return_200(server, path: str, marker: str):
    code, body = _get(server, path)
    assert code == 200, f"{path} 状态码 {code}"
    assert marker in body, f"{path} 缺特征串 {marker!r}"
    assert "<!DOCTYPE html>" in body


def test_five_json_apis_parse(server):
    s, nodes = _get(server, "/api/summary"), _get(server, "/api/nodes")
    code_edges, edges = _get(server, "/api/edges")
    _, top = _get(server, "/api/top")
    _, api_root = _get(server, "/api")
    summary = json.loads(s[1])["summary"]
    assert s[0] == 200 and summary["nodes"] == 121
    assert len(json.loads(nodes[1])["nodes"]) == 121
    assert code_edges == 200 and len(json.loads(edges)["attack"]) > 0
    assert len(json.loads(top)["top"]) == 10
    assert "/api/nodes" in json.loads(api_root)["apis"]
    node = json.loads(_get(server, "/api/node/MIS-CONC-003")[1])["node"]
    assert node["id"] == "MIS-CONC-003"


def test_read_only_no_write_calls():
    """只读硬约束：Web 工具一个写盘/删除调用都不许有（`_send` 走的是 wfile ≠ 写文件）。"""
    src = Path(gw.__file__).read_text(encoding="utf-8")
    for bad in ("write_text(", "write_bytes(", "os.remove", "shutil.", "sqlite3.connect"):
        assert bad not in src, f"Web 工具出现写盘/删除/数据库调用 {bad} ⇒ 只读硬约束被破"
    assert 'self.send_header("Content-Type"' in src       # 输出只走 HTTP 响应，不是写文件


def test_non_loopback_host_refused():
    with pytest.raises(SystemExit) as e:
        gw.make_server(0, "0.0.0.0")            # 就是要验"拒绝绑外网"
    assert "拒绝绑定" in str(e.value)


def test_404_and_broken_document_are_graceful(server, tmp_path: Path):
    assert _get(server, "/no/such/page")[0] == 404
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"nodes": {}, "summary": {}}), encoding="utf-8")
    srv = gw.make_server(0, gw.DEFAULT_HOST, labels=bad)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        code, body = _get(srv, "/nodes")
        assert code == 200, "空文档也要能渲染（不许 500）"
        assert body
    finally:
        srv.shutdown()
        srv.server_close()


def test_api_and_page_agree_on_in_counts(server):
    _, home = _get(server, "/")
    summary = json.loads(_get(server, "/api/summary")[1])["summary"]
    assert f">IN</b></td><td>{summary['IN']}</td>" in home, "页面与 API 的 IN 数不一致"


def test_check_is_green():
    assert gw.check() == []
