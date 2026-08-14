#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_path_viz.py - 学习路径可视化生成器
复用 learning_path.py 的 build_graph()，把 147 章依赖 DAG + 3 条路线
渲染为自包含(无外部依赖)的交互式 HTML 知识地图。

输出: docs/learning_path_viz.html

特性:
  - 按 part 分列(x=阶段, y=章序)，体现"知识流"
  - 节点大小∝入度(基础章更大)
  - 16 色按 part 着色
  - 路线切换(全部/嵌入式/后端/408): 高亮选中路线、淡化其余
  - 节点 hover 显示主题+依赖；点击锁定信息卡
  - 章检索框
  - 画布拖拽平移 + 滚轮缩放
"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import learning_path as lp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "learning_path_viz.html")

# part 顺序（与 Book/ 目录名一致）
PART_ORDER = []
for d in sorted(os.listdir(os.path.join(ROOT, "Book"))):
    if d.startswith("part") and os.path.isdir(os.path.join(ROOT, "Book", d)):
        PART_ORDER.append(d)

# 路线解析（取自 learning_paths.md：## 路线 X: 标题下的各阶段 chXX→chXX 序列）
ROUTES = {}
md = open(os.path.join(ROOT, "learning_paths.md"), encoding="utf-8").read()
cur = None
for line in md.splitlines():
    m = re.match(r"^##\s*路线\s*([ABC]):", line)
    if m:
        cur = "路线" + m.group(1)
        ROUTES[cur] = []
        continue
    if cur and re.match(r"^\s*ch\d{2,3}(\s*→\s*ch\d{2,3})+", line):
        seq = re.findall(r"ch(\d{2,3})", line)
        seen = set(ROUTES[cur])
        for s in seq:
            if s not in seen:
                seen.add(s)
                ROUTES[cur].append(s)


PART_LABEL = {
    "part01_history": "历史", "part02_toolchain": "工具链", "part03_language": "语言",
    "part04_memory": "内存", "part05_oo": "OOP", "part06_templates": "模板",
    "part07_stl": "STL", "part08_concurrency": "并发", "part09_modern": "现代特性",
    "part10_perf": "性能", "part11_source": "源码", "part12_libs": "库生态",
    "part13_patterns": "设计模式", "part14_engineering": "工程", "part15_cases": "案例",
    "part16_reading": "阅读",
}


def main():
    g, indeg, chapters = lp.build_graph()
    # 节点
    nodes = []
    part_members = {p: [] for p in PART_ORDER}
    for num, fname in sorted(chapters, key=lambda x: (x[0].zfill(3))):
        # 反查 part
        part = "?"
        for p in PART_ORDER:
            if os.path.exists(os.path.join(ROOT, "Book", p, fname)):
                part = p
                break
        part_members[part].append(num)
    palette = [
        "#4e79a7","#f28e2b","#e15759","#76b7b2","#59a14f","#edc948","#b07aa1",
        "#ff9da7","#9c755f","#bab0ac","#86bcb6","#d37295","#fabfd2","#b6992d",
        "#499894","#79706e",
    ]
    part_color = {p: palette[i % len(palette)] for i, p in enumerate(PART_ORDER)}
    allnums = set(num for num, _ in chapters)
    for p in PART_ORDER:
        for i, num in enumerate(sorted(part_members[p], key=lambda x: x.zfill(3))):
            nodes.append({
                "num": num,
                "label": lp.get_topic(num),
                "part": p,
                "partLabel": PART_LABEL.get(p, p),
                "indeg": indeg.get(num, 0),
                "outdeg": len(g.get(num, set())),
                "y": i,
            })
    # 边（仅同源/目标都在集合内）
    edges = []
    for num, deps in g.items():
        for t in deps:
            if t in allnums and num in allnums:
                edges.append({"from": num, "to": t})
    # 章号→文件（用于检索提示）
    num2file = {num: fname for num, fname in chapters}

    data = {
        "nodes": nodes,
        "edges": edges,
        "routes": ROUTES,
        "partOrder": PART_ORDER,
        "partLabel": PART_LABEL,
        "partColor": part_color,
        "num2file": num2file,
    }
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"[*] 节点={len(nodes)} 边={len(edges)} 路线={list(ROUTES.keys())}")
    print(f"[*] 已写: {OUT}")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>现代 C++ 终极圣经 · 学习路径知识地图</title>
<style>
  :root { --bg:#0f1117; --panel:#171a23; --ink:#e6e9ef; --muted:#9aa3b2;
          --line:#2a2f3a; --accent:#5aa9ff; }
  * { box-sizing: border-box; }
  html,body { margin:0; height:100%; background:var(--bg); color:var(--ink);
              font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif; }
  #app { display:flex; height:100vh; overflow:hidden; }
  #side { width:320px; min-width:320px; background:var(--panel); border-right:1px solid var(--line);
          padding:16px; overflow-y:auto; }
  #canvas-wrap { flex:1; position:relative; overflow:hidden; }
  svg { width:100%; height:100%; display:block; cursor:grab; }
  svg.drag { cursor:grabbing; }
  h1 { font-size:17px; margin:0 0 4px; }
  .sub { color:var(--muted); font-size:12px; margin-bottom:14px; }
  .routes button { display:block; width:100%; text-align:left; margin:4px 0; padding:8px 10px;
        background:#1f2430; color:var(--ink); border:1px solid var(--line); border-radius:6px;
        cursor:pointer; font-size:13px; }
  .routes button:hover { border-color:var(--accent); }
  .routes button.active { background:#243044; border-color:var(--accent); }
  .rt-desc { font-size:11px; color:var(--muted); margin:2px 0 10px; line-height:1.5; }
  #search { width:100%; padding:7px 9px; background:#11141c; border:1px solid var(--line);
            border-radius:6px; color:var(--ink); font-size:13px; margin-bottom:10px; }
  .legend { margin-top:14px; font-size:11px; color:var(--muted); }
  .legend .row { display:flex; align-items:center; gap:6px; margin:3px 0; }
  .legend .sw { width:12px; height:12px; border-radius:3px; }
  #info { margin-top:14px; background:#11141c; border:1px solid var(--line); border-radius:6px;
          padding:10px; font-size:12px; min-height:80px; }
  #info b { color:var(--accent); }
  .edge { stroke:#3a4150; stroke-width:1; opacity:.5; }
  .edge.hot { stroke:var(--accent); stroke-width:2.2; opacity:.95; }
  .node circle { stroke:#0f1117; stroke-width:1.5; cursor:pointer; transition:opacity .15s; }
  .node text { fill:var(--muted); font-size:10px; pointer-events:none; user-select:none; }
  .dim { opacity:.12 !important; }
  .hint { position:absolute; left:12px; bottom:10px; font-size:11px; color:var(--muted);
          background:rgba(15,17,23,.7); padding:4px 8px; border-radius:5px; }
  .stat { font-size:11px; color:var(--muted); margin-top:8px; }
  a { color:var(--accent); }
</style>
</head>
<body>
<div id="app">
  <div id="side">
    <h1>学习路径知识地图</h1>
    <div class="sub">147 章 · 547 依赖边 · 按 part 分列（左→右=学习阶段）</div>
    <input id="search" placeholder="检索章号/主题，如 vector / ch77">
    <div class="routes" id="routes"></div>
    <div id="info">点击节点查看详情；选择上方路线高亮学习顺序。</div>
    <div class="legend" id="legend"></div>
    <div class="stat" id="stat"></div>
  </div>
  <div id="canvas-wrap">
    <svg id="svg"><g id="viewport"></g></svg>
    <div class="hint">滚轮缩放 · 拖拽平移 · 节点点击锁定</div>
  </div>
</div>
<script>
const DATA = __DATA__;
const COLW = 230, ROWH = 64, PADX = 70, PADY = 50;
const svg = document.getElementById('svg');
const vp = document.getElementById('viewport');
const NS = 'http://www.w3.org/2000/svg';

// 布局：x = part 列, y = part 内序号
const partIndex = {};
DATA.partOrder.forEach((p,i)=>partIndex[p]=i);
const pos = {};
let maxRows = 0;
DATA.nodes.forEach(n=>{
  const x = PADX + partIndex[n.part]*COLW;
  const y = PADY + n.y*ROWH;
  pos[n.num] = {x, y, n};
  maxRows = Math.max(maxRows, n.y+1);
});
const W = PADX*2 + (DATA.partOrder.length-1)*COLW + 120;
const H = PADY*2 + maxRows*ROWH;
svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
svg.setAttribute('width', W); svg.setAttribute('height', H);

// 边
const edgeEls = [];
DATA.edges.forEach(e=>{
  const a = pos[e.from], b = pos[e.to];
  if(!a||!b) return;
  const line = document.createElementNS(NS,'line');
  // 跨列曲线
  const mx = (a.x+b.x)/2;
  line.setAttribute('x1',a.x); line.setAttribute('y1',a.y);
  line.setAttribute('x2',b.x); line.setAttribute('y2',b.y);
  line.setAttribute('class','edge');
  line.dataset.from = e.from; line.dataset.to = e.to;
  vp.appendChild(line); edgeEls.push(line);
});

// 节点
const nodeEls = {};
DATA.nodes.forEach(n=>{
  const p = pos[n.num];
  const g = document.createElementNS(NS,'g');
  g.setAttribute('class','node'); g.setAttribute('transform',`translate(${p.x},${p.y})`);
  const r = 8 + Math.min(n.indeg,26)*0.5;
  const c = document.createElementNS(NS,'circle');
  c.setAttribute('r', r);
  c.setAttribute('fill', DATA.partColor[n.part]);
  const t = document.createElementNS(NS,'text');
  t.setAttribute('x', r+4); t.setAttribute('y', 3);
  t.textContent = `ch${n.num} ${n.label}`;
  g.appendChild(c); g.appendChild(t);
  g.addEventListener('click', ev=>{ ev.stopPropagation(); showInfo(n); lock=n.num; });
  g.addEventListener('mouseenter', ()=>{ if(!lock) showInfo(n); });
  vp.appendChild(g);
  nodeEls[n.num]=g;
});

// 信息卡
let lock = null;
const info = document.getElementById('info');
function showInfo(n){
  const file = DATA.num2file[n.num]||'';
  let deps = DATA.edges.filter(e=>e.from===n.num).map(e=>'ch'+e.to);
  let used = DATA.edges.filter(e=>e.to===n.num).map(e=>'ch'+e.from);
  info.innerHTML = `<b>ch${n.num} · ${n.label}</b><br>`+
    `part: ${n.partLabel} · 入度 ${n.indeg} / 出度 ${n.outdeg}<br>`+
    `文件: <code>${file}</code><br>`+
    (deps.length?`依赖: ${deps.join(', ')}<br>`:'')+
    (used.length?`被依赖: ${used.slice(0,8).join(', ')}${used.length>8?' …':''}`:'');
}

// 路线按钮
const routesBox = document.getElementById('routes');
const routeDesc = {
  '路线A':'嵌入式系统工程师（6 个月）',
  '路线B':'C++ 后端开发（6 个月）',
  '路线C':'考研 408 备考（3 个月）',
};
let activeRoute = null;
function mkBtn(key){
  const b = document.createElement('button');
  b.textContent = key + ' — ' + (routeDesc[key]||'自定义路线');
  b.onclick = ()=>toggleRoute(key, b);
  routesBox.appendChild(b);
}
Object.keys(DATA.routes).forEach(mkBtn);
const allBtn = document.createElement('button');
allBtn.textContent = '全部（依赖全图）';
allBtn.className='active';
allBtn.onclick = ()=>toggleRoute(null, allBtn);
routesBox.appendChild(allBtn);
const descEl = document.createElement('div');
descEl.className='rt-desc';
routesBox.appendChild(descEl);

function toggleRoute(key, btn){
  document.querySelectorAll('#routes button').forEach(x=>x.classList.remove('active'));
  btn.classList.add('active');
  activeRoute = key;
  if(!key){
    descEl.textContent='';
    Object.values(nodeEls).forEach(g=>g.classList.remove('dim'));
    edgeEls.forEach(e=>e.classList.remove('dim','hot'));
    return;
  }
  const seq = DATA.routes[key]||[];
  const set = new Set(seq);
  Object.entries(nodeEls).forEach(([num,g])=>{
    g.classList.toggle('dim', !set.has(num));
  });
  edgeEls.forEach(e=>{
    const hot = set.has(e.dataset.from) && set.has(e.dataset.to) &&
                Math.abs(seq.indexOf(e.dataset.from)-seq.indexOf(e.dataset.to))===1;
    e.classList.toggle('dim', !set.has(e.dataset.from)&&!set.has(e.dataset.to));
    e.classList.toggle('hot', hot);
  });
  descEl.innerHTML = '顺序: ' + seq.map(s=>'ch'+s).join(' → ');
}

// 检索
document.getElementById('search').addEventListener('input', e=>{
  const q = e.target.value.trim().toLowerCase();
  if(!q){ Object.values(nodeEls).forEach(g=>g.classList.remove('dim')); return; }
  Object.entries(nodeEls).forEach(([num,g])=>{
    const n = pos[num].n;
    const hit = ('ch'+num).includes(q) || n.label.toLowerCase().includes(q);
    g.classList.toggle('dim', !hit);
  });
});

// 图例
const legend = document.getElementById('legend');
legend.innerHTML = '<div style="margin-bottom:6px;color:var(--ink)">part 着色</div>'+
  DATA.partOrder.map(p=>`<div class="row"><span class="sw" style="background:${DATA.partColor[p]}"></span>${DATA.partLabel[p]||p}</div>`).join('')+
  '<div style="margin-top:8px">节点大小 ∝ 被依赖次数（基础章更大）</div>';
document.getElementById('stat').textContent =
  `节点 ${DATA.nodes.length} · 边 ${DATA.edges.length} · 路线 ${Object.keys(DATA.routes).length} 条`;

// 平移/缩放
let scale=1, tx=0, ty=0;
function apply(){ vp.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`); }
svg.addEventListener('wheel', e=>{
  e.preventDefault();
  const f = e.deltaY<0?1.1:0.9;
  scale = Math.min(3, Math.max(0.3, scale*f));
  apply();
}, {passive:false});
let drag=false, lx=0, ly=0;
svg.addEventListener('mousedown', e=>{ drag=true; lx=e.clientX; ly=e.clientY; svg.classList.add('drag'); });
window.addEventListener('mouseup', ()=>{ drag=false; svg.classList.remove('drag'); });
window.addEventListener('mousemove', e=>{
  if(!drag) return;
  tx += e.clientX-lx; ty += e.clientY-ly; lx=e.clientX; ly=e.clientY; apply();
});
svg.addEventListener('click', ()=>{ lock=null; });
apply();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
