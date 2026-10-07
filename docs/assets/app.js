/* Quyi (阙疑) site — shared helpers. Vanilla JS only. */
"use strict";

const ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js";

function el(id) { return document.getElementById(id); }

function fmtPct(x, digits = 2) {
  return (x === null || x === undefined) ? "n/a" : Number(x).toFixed(digits) + "%";
}

/* verdict pill */
function verdictPill(v) {
  const cls = v === "catch" ? "good" : (v === "miss" ? "bad" : "unk");
  return `<span class="pill ${cls}">${v || "n/a"}</span>`;
}

async function loadJSON(path) {
  const r = await fetch(path, { cache: "no-store" });
  if (!r.ok) throw new Error(`fetch ${path} -> ${r.status}`);
  return r.json();
}

/* ECharts loader with graceful offline degradation */
function loadECharts() {
  return new Promise((resolve, reject) => {
    if (window.echarts) return resolve(window.echarts);
    const s = document.createElement("script");
    s.src = ECHARTS_CDN;
    s.onload = () => resolve(window.echarts);
    s.onerror = () => reject(new Error("ECharts CDN 不可达（离线环境）"));
    document.head.appendChild(s);
  });
}

async function mountChart(divId, option, noteId) {
  try {
    const echarts = await loadECharts();
    const node = el(divId);
    const chart = echarts.init(node, null, { renderer: "canvas" });
    chart.setOption(option);
    window.addEventListener("resize", () => chart.resize());
    return chart;
  } catch (e) {
    const node = el(divId);
    if (node) node.innerHTML =
      `<p class="chart-note">图表需要联网加载 ECharts CDN；离线时图表不可用，` +
      `但本页所有数字均以表格给出（可核验）。</p>`;
    if (noteId && el(noteId)) el(noteId).textContent = String(e.message || e);
    return null;
  }
}

/* mark active nav link by filename */
(function markNav() {
  const here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav.links a").forEach(a => {
    const target = a.getAttribute("href");
    if (target === here) a.classList.add("active");
  });
})();

/* simple client-side table filter helper */
function textMatch(row, fields, q) {
  if (!q) return true;
  q = q.toLowerCase();
  return fields.some(f => String(row[f] || "").toLowerCase().includes(q));
}
