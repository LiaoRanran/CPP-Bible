// 655 D · 星图的**纯几何/统计核心**（无 DOM、无 canvas ⇒ 可在 Node 里真跑）
//   starmap.js 用它做：卡片摘要里的攻防计数、边 hover 的"最近边"判定。

/** 某节点的攻/防/被击败计数（只数与该节点相连的边）。 */
export function statsOf(links, id) {
  let attacks = 0, defends = 0, defeated = 0;
  for (const l of links) {
    if (l.source !== id && l.target !== id) continue;
    if (l.kind === 'attack') { attacks++; if (l.defeated) defeated++; }
    else if (l.kind === 'defend') defends++;
  }
  return { attacks, defends, defeated };
}

/** 点 (px,py) 到线段 AB 的距离（t clamped 到 [0,1]，即"最近点在线段上"）。 */
export function pointSegDist(px, py, ax, ay, bx, by) {
  const vx = bx - ax, vy = by - ay;
  const len2 = vx * vx + vy * vy;
  if (len2 < 1e-9) return Math.hypot(px - ax, py - ay);
  let t = ((px - ax) * vx + (py - ay) * vy) / len2;
  t = Math.max(0, Math.min(1, t));
  return Math.hypot(px - (ax + t * vx), py - (ay + t * vy));
}

/** 在可见边里挑"离鼠标最近且在阈值内"的边下标（找不到 ⇒ -1）。 */
export function pickEdgeIndex({ links, nodes, pos, toScreen, visible, passLink, sx, sy, maxPx }) {
  let best = -1, bd = maxPx;
  for (let i = 0; i < links.length; i++) {
    const l = links[i];
    if (!passLink(l)) continue;
    const a = l._ai, b = l._bi;
    if (a == null || b == null || !visible(nodes[a]) || !visible(nodes[b])) continue;
    const A = toScreen(pos[a]), B = toScreen(pos[b]);
    const d = pointSegDist(sx, sy, A.x, A.y, B.x, B.y);
    if (d < bd) { bd = d; best = i; }
  }
  return best;
}
