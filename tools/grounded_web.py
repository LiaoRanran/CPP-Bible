"""609 C2 · 论证 Web 界面（纯标准库 `http.server`，**只读 + 只绑 127.0.0.1**）。

为什么必须自己写 HTTP 层：引 Flask/FastAPI = 引依赖 = 给供应链多一条要审计的路。
这里只需要"把 W2 结论摆给人看"，标准库够了。

硬约束（三条都是**防越权**的）：
  * **只读**：全部 handler 只读 `grounded_labels_w2.json` + `attack_edges_candidates.jsonl`，
    一个写盘调用都没有（清单里可以 grep 到零 `open(..., "w")`）；
  * **只绑 127.0.0.1**（不对外网卡暴露，`--host` 若传非回环地址 ⇒ **拒绝启动**）；
  * 每一页都带数据源版本与生成时刻 ⇒ 截图/转述时零歧义。

路由 · 6 个页面：
    `/`                 总览（判决分布 + 入口）
    `/nodes`            全部节点（按类型/判决筛选）
    `/node/<id>`        单节点（攻击者/辩护者/证据/卡）
    `/edges`            边列表（攻击/支持 + `?type=`）
    `/mis`              MIS 组（按击败它的命题聚合）
    `/report`           论证报告（summary + 拓扑说明 + 数据血缘）
路由 · 5 个 JSON API（供机器取数）：
    `/api/summary` `/api/nodes` `/api/node/<id>` `/api/edges` `/api/top`

CLI：
    serve [--port N] [--host 127.0.0.1]     常驻（Ctrl-C 退出）
    --check                                 0 数据源齐备且可读 / 1 破
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import html
import http.server
import json
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
DEFAULT_LABELS = ROOT / "data" / "grounded_labels_w2.json"
DEFAULT_EDGES = ROOT / "data" / "attack_edges_candidates.jsonl"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

_LOOPBACK = {"127.0.0.1", "::1", "localhost"}


def load_doc(path: Path | str = DEFAULT_LABELS) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[web] 标注文档不存在：{p}（先跑 weighted_af_solver.py solve）")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise SystemExit(f"[web] 标注文档不是合法 JSON：{exc}") from exc


def load_edges(path: Path | str = DEFAULT_EDGES) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _esc(s: object) -> str:
    return html.escape(str(s))


PAGE = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{title} · 论证 Web</title>
<style>body{{font-family:sans-serif;margin:24px;color:#222}}table{{border-collapse:collapse}}
th,td{{border:1px solid #ddd;padding:4px 8px;font-size:12px;text-align:left}}
a{{color:#1565c0}}.note{{color:#666;font-size:12px}}
code{{background:#f5f5f5;padding:1px 4px}}</style></head><body>
<h1>{title}</h1>{body}
<p class="note">数据源：<code>{src}</code> · 生成于 {ts} ·
tool <code>grounded_web {ver}</code>（只读 · 仅绑 {host}）</p></body></html>"""


def _page(title: str, body: str, src: str, host: str) -> str:
    return PAGE.format(title=_esc(title), body=body, src=_esc(src),
                       ts=datetime.now(timezone(timedelta(hours=8))).replace(
                           microsecond=0).isoformat(),
                       ver=VERSION, host=_esc(host))


def render_overview(doc: dict, host: str) -> str:
    s = doc["summary"]
    rows = "".join(f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in s.items())
    body = (f"<table>{rows}</table>"
            f"<p>轮数 {doc.get('rounds')} · 击败边 {doc.get('defeating_edges')}/{doc.get('edges')}</p>"
            "<ul><li><a href='/nodes'>全部节点</a></li><li><a href='/edges'>边列表</a></li>"
            "<li><a href='/mis'>MIS 组</a></li><li><a href='/report'>论证报告</a></li>"
            "<li><code>/api/summary</code> · <code>/api/nodes</code> · "
            "<code>/api/edges</code> · <code>/api/top</code></li></ul>")
    return _page("论证总览", body, "grounded_labels_w2.json", host)


def render_nodes(doc: dict, host: str, *, kind: str = "") -> str:
    rows = []
    for nid, v in sorted(doc["nodes"].items()):
        if kind and kind not in (v["type"], v["label"]):
            continue
        rows.append(f"<tr><td><a href='/node/{urllib.parse.quote(str(nid))}'>{_esc(nid)}</a></td>"
                    f"<td>{_esc(v['type'])}</td><td>{_esc(v['label'])}</td>"
                    f"<td>{_esc(v['confidence'])}</td><td>{len(v.get('attackers', ()))}</td>"
                    f"<td>{len(v.get('defenders', ()))}</td></tr>")
    body = ("<table><tr><th>节点</th><th>类型</th><th>判决</th><th>可信度</th>"
            "<th>攻击数</th><th>辩护数</th></tr>" + "".join(rows) + "</table>"
            f"<p class='note'>共 {len(rows)} 行（筛选 kind={kind or '全部'}）</p>")
    return _page("节点一览", body, "grounded_labels_w2.json", host)


def render_node(doc: dict, node_id: str, host: str) -> str:
    v = doc["nodes"].get(node_id)
    if v is None:
        return _page("节点未找到", f"<p>节点 <code>{_esc(node_id)}</code> 不在文档里</p>",
                     "grounded_labels_w2.json", host)
    li = lambda label, items: (          # noqa: E731
        f"<li>{label}：" + "、".join(
            f"<a href='/node/{urllib.parse.quote(str(i))}'>{_esc(i)}</a>" for i in items)
        + "</li>") if items else f"<li>{label}：无</li>"
    body = (f"<ul><li>类型：{_esc(v['type'])}</li><li>判决：<b>{_esc(v['label'])}</b></li>"
            f"<li>可信度：{_esc(v['confidence'])}（credibility {_esc(v['credibility'])}）</li>"
            f"{li('攻击者', v.get('attackers', ()))}"
            f"{li('被它击败的攻击者', v.get('defeated_attackers', ()))}"
            f"{li('辩护者', v.get('defenders', ()))}"
            + (f"<li>卡：{_esc(v.get('card'))}</li>" if v.get("card") else "") + "</ul>"
            "<p><a href='/nodes'>← 回节点一览</a></p>")
    return _page(f"节点 {node_id}", body, "grounded_labels_w2.json", host)


def render_edges(doc: dict, edges: list[dict], host: str, *, etype: str = "") -> str:
    rows: list[str] = []
    nodes = doc["nodes"]
    for a, b in sorted({(str(x), str(nid)) for nid, v in nodes.items()
                        for x in v.get("defeated_attackers", ())}):
        if etype and etype != "attack":
            continue
        rows.append(f"<tr><td>attack</td><td>{_esc(a)}</td><td>{_esc(b)}</td></tr>")
    for a, b in sorted({(str(d), str(nid)) for nid, v in nodes.items()
                        for d in v.get("defenders", ()) if d in nodes}):
        if etype and etype != "support":
            continue
        rows.append(f"<tr><td>support</td><td>{_esc(a)}</td><td>{_esc(b)}</td></tr>")
    cand = len(edges)
    body = ("<table><tr><th>类型</th><th>source</th><th>target</th></tr>" + "".join(rows)
            + f"</table><p class='note'>共 {len(rows)} 条（候选边 {cand} 条，来自 "
              "attack_edges_candidates.jsonl）</p>")
    return _page("边列表", body, "grounded_labels_w2.json + attack_edges_candidates.jsonl", host)


def render_mis(doc: dict, host: str) -> str:
    rows = []
    for nid, v in sorted(doc["nodes"].items()):
        if v["type"] != "misconception":
            continue
        rows.append(f"<tr><td><a href='/node/{urllib.parse.quote(str(nid))}'>{_esc(nid)}</a></td>"
                    f"<td>{_esc(v['label'])}</td><td>{len(v.get('attackers', ()))}</td>"
                    f"<td>{len(v.get('defeated_attackers', ()))}</td></tr>")
    body = ("<table><tr><th>MIS</th><th>判决</th><th>攻击者</th><th>被它击败</th></tr>"
            + "".join(rows) + "</table>")
    return _page("MIS 组", body, "grounded_labels_w2.json", host)


def render_report(doc: dict, host: str) -> str:
    lines = [f"<li>{_esc(k)}：{_esc(v)}</li>" for k, v in doc["summary"].items()]
    body = ("<h2>论证摘要</h2><ul>" + "".join(lines) + "</ul>"
            f"<h2>求解参数</h2><ul><li>model：{_esc(doc.get('model'))}</li>"
            f"<li>credibility_levels：{_esc(doc.get('credibility_levels'))}</li>"
            f"<li>轮数：{_esc(doc.get('rounds'))}</li>"
            f"<li>击败边/全部边：{_esc(doc.get('defeating_edges'))}/{_esc(doc.get('edges'))}</li></ul>"
            "<h2>数据血缘</h2><p class='note'>attack_edge_generator（388 候选边）→ "
            "weighted_af_solver（W2 可信度加权 grounded）→ 本页（只读渲染）。"
            "人审介入后请重跑 solver，本页**不会**自动重算。</p>")
    return _page("论证报告", body, "grounded_labels_w2.json", host)


class GroundedHandler(http.server.BaseHTTPRequestHandler):
    """只读 handler；`labels`/`edges` 由 `make_server` 注入（便于测试喂 fixture）。"""

    labels_path = str(DEFAULT_LABELS)
    edges_path = str(DEFAULT_EDGES)
    host_for_page = DEFAULT_HOST

    def log_message(self, fmt: str, *args) -> None:      # 静音默认访问日志
        pass

    def _send(self, body: str | bytes, ctype: str = "text/html; charset=utf-8",
              code: int = 200) -> None:
        raw = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _json(self, obj: object) -> None:
        self._send(json.dumps(obj, ensure_ascii=False, indent=1),
                   "application/json; charset=utf-8")

    def _route(self, path: str, q: dict[str, list[str]]) -> None:
        doc = load_doc(self.labels_path)
        edges = load_edges(self.edges_path)
        seg = [s for s in path.split("/") if s]
        if not seg:
            return self._send(render_overview(doc, self.host_for_page))
        head, rest = seg[0], seg[1:]
        if head == "api":
            if not rest:
                return self._json({"apis": ["/api/summary", "/api/nodes", "/api/edges",
                                            "/api/top", "/api/node/<id>"]})
            name = rest[0]
            if name == "summary":
                return self._json({"summary": doc["summary"], "rounds": doc.get("rounds"),
                                   "defeating_edges": doc.get("defeating_edges"),
                                   "edges": doc.get("edges")})
            if name == "nodes":
                return self._json({"nodes": doc["nodes"]})
            if name == "edges":
                atk = sorted({(str(a), str(n)) for n, v in doc["nodes"].items()
                              for a in v.get("defeated_attackers", ())})
                sup = sorted({(str(d), str(n)) for n, v in doc["nodes"].items()
                              for d in v.get("defenders", ()) if d in doc["nodes"]})
                return self._json({"attack": [list(x) for x in atk],
                                   "support": [list(x) for x in sup],
                                   "candidates": len(edges)})
            if name == "top":
                rows = sorted(({"id": k, "attackers": len(v.get("attackers", ())),
                                "defenders": len(v.get("defenders", ())),
                                "label": v.get("label")} for k, v in doc["nodes"].items()),
                              key=lambda r: -r["attackers"])[:10]
                return self._json({"top": rows})
            if name == "node" and len(rest) > 1:
                nid = urllib.parse.unquote(rest[1])
                node = doc["nodes"].get(nid)
                return self._json({"node": node} if node else {"error": f"no such node: {nid}"})
            return self._json({"error": f"unknown api: {name}"}, )
        if head == "nodes":
            return self._send(render_nodes(doc, self.host_for_page,
                                           kind=(q.get("kind") or [""])[0]))
        if head == "node" and rest:
            return self._send(render_node(doc, urllib.parse.unquote(rest[0]),
                                          self.host_for_page))
        if head == "edges":
            return self._send(render_edges(doc, edges, self.host_for_page,
                                           etype=(q.get("type") or [""])[0]))
        if head == "mis":
            return self._send(render_mis(doc, self.host_for_page))
        if head == "report":
            return self._send(render_report(doc, self.host_for_page))
        self._send("<h1>404</h1><p class='note'>未知路径（见 / 的入口清单）</p>",
                   code=404)

    def do_GET(self) -> None:                     # 只有 GET：**没有 POST/PUT/DELETE**
        parsed = urllib.parse.urlparse(self.path)
        try:
            self._route(parsed.path, urllib.parse.parse_qs(parsed.query))
        except SystemExit as exc:
            self._send(f"<h1>500</h1><p>{_esc(exc)}</p>", code=500)
        except Exception as exc:                  # 一律 fail-loud，但不允许把栈甩给浏览器
            self._send(f"<h1>500</h1><p>{_esc(exc)}</p>", code=500)


def make_server(port: int = 0, host: str = DEFAULT_HOST, *,
                labels: Path | str = DEFAULT_LABELS,
                edges: Path | str = DEFAULT_EDGES) -> http.server.ThreadingHTTPServer:
    """起服务；`port=0` ⇒ 由内核挑空口（**测试必须这么用**，避免抢固定口）。"""
    if host not in _LOOPBACK:
        raise SystemExit(f"[web] 拒绝绑定到非回环地址 {host!r}："
                         f"本工具只读且不得对外暴露（只接受 {sorted(_LOOPBACK)}）")
    cls = type("BoundHandler", (GroundedHandler,),
               {"labels_path": str(labels), "edges_path": str(edges),
                "host_for_page": host})
    return http.server.ThreadingHTTPServer((host, port), cls)


def serve(port: int = DEFAULT_PORT, host: str = DEFAULT_HOST) -> int:
    srv = make_server(port, host)
    print(f"[web] 只读论证 Web 起在 http://{host}:{srv.server_address[1]}/（Ctrl-C 退出）")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[web] 已退出")
    finally:
        srv.server_close()
    return 0


def check() -> list[str]:
    problems: list[str] = []
    for p in (DEFAULT_LABELS, DEFAULT_EDGES):
        if not p.is_file():
            problems.append(f"数据源缺失：{p}")
    if not problems:
        try:
            doc = load_doc(DEFAULT_LABELS)
        except SystemExit as exc:
            return [str(exc)]
        if not isinstance(doc.get("nodes"), dict) or not doc["nodes"]:
            problems.append("nodes 为空（先跑 solver）")
    if set(DEFAULT_HOST.split(".")) and DEFAULT_HOST not in _LOOPBACK:
        problems.append(f"默认 host {DEFAULT_HOST} 不是回环地址")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grounded_web",
                                 description="609 C2 论证 Web 界面（只读 · 只绑回环）")
    ap.add_argument("--version", action="version", version=f"grounded_web {VERSION}")
    ap.add_argument("--check", action="store_true", help="数据源齐备性检查（0 ok / 1 破）")
    ap.add_argument("serve", nargs="?", default=None, help="起服务")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--host", default=DEFAULT_HOST)
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[web] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[web] --check OK：{DEFAULT_LABELS.name} + {DEFAULT_EDGES.name} 齐备可读"
              f"（默认只绑 {DEFAULT_HOST}）")
        return 0

    if a.serve != "serve":
        ap.print_help()
        return 2
    return serve(a.port, a.host)


if __name__ == "__main__":
    sys.exit(main())
