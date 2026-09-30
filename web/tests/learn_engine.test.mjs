// 670c A1 · Node 真求值：learn_engine 纯逻辑测试（无 DOM / 无依赖，直接 node 跑）
// 覆盖：SM-2 边界 · 错例牌组 · 三阶段路径 · 统计/连续天数 · 掌握度曲线 · 薄弱热力图
//       · 下次复习文案 · 键盘快捷键 · 导入导出校验
import assert from 'node:assert/strict';
import {
  sm2, freshState, isDue, isMastered, isWeak, isTouched,
  buildCardDeck, buildErrorDeck, errorCardCompleteness,
  deckStats, deckStatsEx, dueQueue, DAY,
  STAGES, pathProgress, nextReviewAt, formatNextReview,
  masteryCurve, weakHeatmap, streakDays,
  handleKey, GRADE_KEYS,
  exportPayload, importPayload, isValidState, EXPORT_SCHEMA,
} from '../js/learn_engine.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };

// ══ 1. SM-2 调度与边界 ══
let s = freshState();
s = sm2(s, 5, 0);
ok('首次 q=5 → interval=1, reps=1', s.interval === 1 && s.reps === 1);
ok('首次 q=5 → ease=2.6', Math.abs(s.ease - 2.6) < 1e-9);
ok('history 记录第一条', s.history.length === 1 && s.history[0].q === 5);
ok('due = now + interval*DAY', s.due === DAY);
s = sm2(s, 5, DAY);
ok('二次 q=5 → interval=6, reps=2', s.interval === 6 && s.reps === 2);
const third = sm2(s, 5, 2 * DAY);
ok('三次 q=5 → interval=round(6*ease)', third.interval === Math.round(6 * s.ease));
ok('sm2 不修改入参（纯函数）', s.interval === 6 && s.reps === 2);
const f = sm2(s, 1, 2 * DAY);
ok('失败 q=1 → reps 归零、interval=1、lapses+1', f.reps === 0 && f.interval === 1 && f.lapses === 1);
ok('history 记录质量', f.history.length === 3);
ok('q 上界钳制：q=9 按 5 处理', sm2(freshState(), 9, 0).lastQ === 5);
ok('q 下界钳制：q=-3 按 0 处理', sm2(freshState(), -3, 0).lastQ === 0);
let low = freshState();
for (let i = 0; i < 12; i++) low = sm2(low, 0, i * DAY);
ok('ease 下限 1.3（连续失败不塌缩）', Math.abs(low.ease - 1.3) < 1e-9);
ok('失败不推进 reps', low.reps === 0 && low.lapses === 12);

// ══ 2. 到期 / 掌握 / 薄弱 ══
ok('到期（due<=now）', isDue({ due: 0 }, 100));
ok('未到期（未来）', !isDue({ due: 1000 }, 100));
ok('掌握：interval≥21 且 reps≥2 且 lastQ≥3', isMastered({ interval: 21, reps: 2, lastQ: 4 }));
ok('不掌握：reps 不足', !isMastered({ interval: 30, reps: 1, lastQ: 4 }));
ok('不掌握：末次质量低', !isMastered({ interval: 30, reps: 3, lastQ: 2 }));
ok('薄弱：有 lapse', isWeak({ lapses: 1 }));
ok('薄弱：lastQ 低', isWeak({ lastQ: 2 }));
ok('不薄弱', !isWeak({ lapses: 0, lastQ: 4 }));

// ══ 3. 牌组构建 ══
const deck = buildCardDeck([
  { id: 'A', draft: false, title: 't', domain: 'lang', verdict_state: 'pass', evidence: [1, 2], prereqs: ['Z'] },
  { id: 'B', draft: true },
]);
ok('知识牌组排除草稿', deck.length === 1 && deck[0].id === 'A');
ok('知识牌组保留先修字段', deck[0].prereqs.length === 1 && deck[0].prereqs[0] === 'Z');
ok('知识牌组 domain 透传', deck[0].domain === 'lang');

const newDeck = buildErrorDeck({ cards: [{
  id: 'IG01', wrong_assertion: '溢出会回绕', counterexample: '溢出是 UB',
  fixture_code: 'int main(){}', sanitizer_output: 'runtime error: signed integer overflow',
  correct_assertion: '溢出是 UB', correct_source: 'counterexample-text/machine-unsigned',
  verdict: 'catch', four_state: 'pass', detector: 'ubsan', refuted: true, needs_review: true,
}] });
ok('错例牌组取 wrong_assertion（不是正确断言）', newDeck.length === 1 && newDeck[0].wrong_assertion === '溢出会回绕');
ok('错例牌组带反例代码', newDeck[0].fixture_code === 'int main(){}');
ok('错例牌组带 sanitizer 输出', newDeck[0].sanitizer_output.includes('signed integer overflow'));
ok('错例牌组登记正确断言来源', newDeck[0].correct_source === 'counterexample-text/machine-unsigned');
ok('错例牌组标未签', newDeck[0].needs_review === true);
ok('四段式完整性判定为 true', errorCardCompleteness(newDeck[0]).complete === true);

const legacy = buildErrorDeck({ cards: [{ id: 'L1', assertion: '旧断言', counterexample: 'x', measured_out: ' out \n' }] });
ok('兼容旧 ig 格式：assertion→wrong_assertion', legacy[0].wrong_assertion === '旧断言');
ok('兼容旧 ig 格式：measured_out→sanitizer_output 且 trim', legacy[0].sanitizer_output === 'out');
ok('旧格式无正确断言 ⇒ 来源标 unavailable', legacy[0].correct_assertion === ''
  && legacy[0].correct_source === 'unavailable/legacy-ig-format');
ok('旧格式四段式不完整', errorCardCompleteness(legacy[0]).complete === false);
ok('空输入不抛异常', buildErrorDeck({}).length === 0 && buildErrorDeck().length === 0);

// ══ 4. 三阶段学习路径 ══
ok('恰好三个阶段', STAGES.length === 3 && STAGES[0].id === 'prereq' && STAGES[2].id === 'quiz');
const deck2 = [{ id: 'A', prereqs: [] }, { id: 'B', prereqs: ['A'] }];
const p0 = pathProgress({}, deck2);
ok('空进度：前置阶段 1/2 就绪', p0.stages[0].done === 1 && p0.stages[0].total === 2);
ok('空进度：当前阶段为前置(0)', p0.currentStage === 0 && p0.stages[0].status === 'current');
ok('空进度：断言/自测阶段为 0 且 pending', p0.stages[1].done === 0 && p0.stages[2].status === 'todo');
const masterA = { interval: 30, reps: 2, lastQ: 4 };
const p1 = pathProgress({ A: masterA }, deck2);
ok('A 掌握后：前置阶段完成', p1.stages[0].done === 2 && p1.stages[0].status === 'done');
ok('A 掌握后：当前阶段推进到断言(1)', p1.currentStage === 1);
const p2 = pathProgress({ A: masterA, B: { interval: 30, reps: 2, lastQ: 5 } }, deck2);
ok('全部掌握：三阶段皆 done', p2.stages.every((x) => x.status === 'done'));
ok('全部掌握：overall=1', Math.abs(p2.overall - 1) < 1e-9);
ok('空牌组不除零', pathProgress({}, []).overall === 0);
ok('牌组外先修被忽略（不阻塞）', pathProgress({}, [{ id: 'X', prereqs: ['NOT_IN_DECK'] }]).stages[0].done === 1);

// ══ 5. 下次复习文案 ══
ok('未学过 → 未开始', formatNextReview(freshState(), 0) === '未开始' && nextReviewAt(freshState()) === null);
ok('已到期 → 该复习了', formatNextReview({ reps: 1, due: 0 }, 100) === '该复习了');
ok('当天内 → 今天', formatNextReview({ reps: 1, due: 0.5 * DAY }, 1) === '今天');
ok('1–2 天 → 明天', formatNextReview({ reps: 1, due: 1.5 * DAY }, 0) === '明天');
ok('远期 → N 天后', formatNextReview({ reps: 1, due: 6 * DAY }, 0) === '6 天后');

// ══ 6. 掌握度曲线 ══
const curve = masteryCurve(
  { A: { history: [{ q: 5, t: 0 }, { q: 5, t: DAY }, { q: 5, t: 2 * DAY }, { q: 5, t: 3 * DAY }] } },
  [{ id: 'A' }],
);
ok('曲线：四个事件四个点', curve.points.length === 4 && curve.events === 4);
ok('曲线：点按时间递增', curve.points[0].t === 0 && curve.points[3].t === 3 * DAY);
ok('曲线：首点 studied=1', curve.points[0].studied === 1);
// SM-2 真值：第 3 次后 interval=round(6*2.7)=16 <21 未掌握；第 4 次后 interval=round(16*2.8)=45 ≥21 掌握
ok('曲线：第 3 次仍未掌握（interval=16<21）', curve.points[2].mastered === 0);
ok('曲线：第 4 次后掌握（interval=45≥21）', curve.points[3].mastered === 1);
ok('曲线：同刻事件合并为一点', masteryCurve(
  { A: { history: [{ q: 5, t: 7 }] }, B: { history: [{ q: 3, t: 7 }] } }, [{ id: 'A' }, { id: 'B' }],
).points.length === 1);
ok('曲线：无 history 返回空', masteryCurve({}, [{ id: 'A' }]).points.length === 0);

// ══ 7. 薄弱热力图 ══
const hdeck = [
  { id: 'a', domain: 'lang' }, { id: 'b', domain: 'lang' },
  { id: 'c', domain: 'perf' }, { id: 'd', domain: 'perf' },
];
const hm = weakHeatmap({ a: masterA, b: masterA, c: { lapses: 2, reps: 0, lastQ: 1 } }, hdeck);
ok('热力图：按 domain 分桶', hm.length === 2);
const lang = hm.find((x) => x.key === 'lang');
const perf = hm.find((x) => x.key === 'perf');
ok('热力图：lang 2/2 掌握 → level 3', lang.mastered === 2 && lang.level === 3);
ok('热力图：perf 有薄弱 → isWeak', perf.isWeak === true);
ok('热力图：未学桶 level=0', weakHeatmap({}, hdeck).every((x) => x.level === 0));
ok('热力图：薄弱桶排前面', hm[0].key === 'perf');
ok('热力图：自定义分桶键', weakHeatmap({}, [{ id: 'z', kind: 'error' }], (c) => c.kind)[0].key === 'error');
ok('热力图：失败过(reps=0)的卡仍计入 studied/weak', (() => {
  const hh = weakHeatmap({ c: { reps: 0, lapses: 2, lastQ: 1 } }, [{ id: 'c', domain: 'perf' }]);
  return hh[0].studied === 1 && hh[0].weak === 1;
})());

// ══ 7b. 669c 遗留 bug 修正：失败过的卡不能被当成"未学" ══
const failedState = { reps: 0, lapses: 1, lastQ: 1, interval: 1, due: 0, history: [{ q: 1, t: 0 }] };
const dsFail = deckStats({ C: failedState }, [{ id: 'C' }]);
ok('修正：失败过的卡算"已学"而非"未学"', dsFail.studied === 1 && dsFail.untouched === 0);
ok('修正：失败过的卡计入薄弱', dsFail.weak === 1);
ok('修正：isTouched 对空状态为 false', !isTouched(freshState()) && !isTouched(undefined));
ok('修正：isTouched 对仅 reps>0 为 true', isTouched({ reps: 1 }));
ok('修正：失败过但未到期的卡不当作"未学"补位', dueQueue(
  { C: { ...failedState, due: 10 * DAY } }, [{ id: 'C' }], 5, 0).length === 0);

// ══ 8. 连续天数 ══
const sprog = { A: { history: [{ q: 5, t: 0 }, { q: 5, t: DAY }, { q: 5, t: 2 * DAY }] } };
const st1 = streakDays(sprog, 2 * DAY);
ok('连续天数：今天在链上 → current=3', st1.current === 3);
ok('连续天数：longest=3', st1.longest === 3);
ok('连续天数：断档后 current=0', streakDays(sprog, 5 * DAY).current === 0);
ok('连续天数：昨天在链上仍算连续', streakDays(sprog, 3 * DAY).current === 3);
ok('连续天数：空进度为 0', streakDays({}, 0).current === 0 && streakDays({}, 0).longest === 0);
ok('连续天数：同一天多次复习算一天', streakDays(
  { A: { history: [{ q: 5, t: 10 }, { q: 4, t: 20 }, { q: 3, t: 30 }] } }, 30).current === 1);

// ══ 9. 统计与队列 ══
const prog = { A: { interval: 30, reps: 2, lastQ: 4, due: 0 }, B: freshState() };
const ds = deckStats(prog, [{ id: 'A' }, { id: 'B' }]);
ok('统计：studied=1, mastered=1, untouched=1', ds.studied === 1 && ds.mastered === 1 && ds.untouched === 1);
ok('统计：due 计入到期的 A', ds.due === 1);
const dse = deckStatsEx(prog, [{ id: 'A' }, { id: 'B' }], 0);
ok('增强统计：带 streak 与 path', !!dse.streak && !!dse.path && dse.path.stages.length === 3);
const q = dueQueue(prog, [{ id: 'A' }, { id: 'B' }], 10, 100);
ok('队列：到期 A 优先，B 补位', q[0] === 'A' && q.includes('B'));
ok('队列：limit 生效', dueQueue(prog, [{ id: 'A' }, { id: 'B' }], 1, 100).length === 1);

// ══ 10. 键盘快捷键 ══
const base = { hasCard: true, revealed: false, index: 0, length: 3 };
ok('空格未揭晓 → reveal', handleKey(' ', base).action === 'reveal');
ok('Spacebar 别名 → reveal', handleKey('Spacebar', base).action === 'reveal');
ok('空格已揭晓 → none（不重复揭晓）', handleKey(' ', { ...base, revealed: true }).action === 'none');
ok('← → prev', handleKey('ArrowLeft', base).action === 'prev');
ok('→ → next', handleKey('ArrowRight', base).action === 'next');
ok('只有一张卡时 ←/→ 为 none', handleKey('ArrowLeft', { ...base, length: 1 }).action === 'none');
ok('未揭晓时 1-4 不评分', handleKey('1', base).action === 'none');
ok('1=忘记(q=1)', handleKey('1', { ...base, revealed: true }).q === 1);
ok('2=困难(q=3)', handleKey('2', { ...base, revealed: true }).q === 3);
ok('3=良好(q=4)', handleKey('3', { ...base, revealed: true }).q === 4);
ok('4=完美(q=5)', handleKey('4', { ...base, revealed: true }).q === 5);
ok('评分映射表与键位一致', GRADE_KEYS['1'] === 1 && GRADE_KEYS['4'] === 5);
ok('无卡时一律 none', handleKey(' ', { hasCard: false, length: 0 }).action === 'none'
  && handleKey('ArrowRight', { hasCard: false, length: 0 }).action === 'none');
ok('未知按键 → none', handleKey('F5', { ...base, revealed: true }).action === 'none');

// ══ 11. 导出 / 导入 ══
ok('isValidState：合法', isValidState({ ease: 2.5, interval: 1, reps: 1, lapses: 0, due: 0, history: [] }));
ok('isValidState：非数字 reps 非法', !isValidState({ reps: 'x' }));
ok('isValidState：history 非数组非法', !isValidState({ reps: 1, history: {} }));
ok('isValidState：null/数组非法', !isValidState(null) && !isValidState([]));
const dump = exportPayload({ A: { reps: 1 } }, { note: 'n' }, 0);
const parsedDump = JSON.parse(dump);
ok('导出：带 schema', parsedDump.schema === EXPORT_SCHEMA);
ok('导出：带条数与 meta', parsedDump.count === 1 && parsedDump.meta.note === 'n');
ok('导入：坏 JSON → ok=false 且不动原进度', (() => {
  const r = importPayload('{oops', { A: { reps: 9 } });
  return r.ok === false && r.progress.A.reps === 9 && /JSON/.test(r.error);
})());
ok('导入：合法载荷合并', (() => {
  const r = importPayload(dump, {});
  return r.ok === true && r.imported === 1 && r.progress.A.reps === 1;
})());
ok('导入：坏条目跳过并计数', (() => {
  const r = importPayload(JSON.stringify({ cards: { good: { reps: 2 }, bad: { reps: 'x' } } }), {});
  return r.ok === true && r.imported === 1 && r.skipped === 1 && !('bad' in r.progress);
})());
ok('导入默认保留更靠前的进度（不被旧档案回退）', (() => {
  const r = importPayload(JSON.stringify({ cards: { A: { reps: 1, interval: 1 } } }), { A: { reps: 5, interval: 30 } });
  return r.progress.A.reps === 5;
})());
ok('导入 prefer=imported 时以档案为准', (() => {
  const r = importPayload(JSON.stringify({ cards: { A: { reps: 1, interval: 1 } } }), { A: { reps: 5, interval: 30 } }, { prefer: 'imported' });
  return r.progress.A.reps === 1;
})());
ok('导入：结构不符 → ok=false', importPayload(JSON.stringify([1, 2]), {}).ok === false);

console.log('learn_engine.test: ' + passed + ' assertions passed');
