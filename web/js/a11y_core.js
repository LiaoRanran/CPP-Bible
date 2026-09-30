// 670c4 · 可访问性纯逻辑（无 DOM 依赖，Node 可测）
// 快捷键匹配 / 焦点陷阱索引 / 播报文案 / 帮助清单 —— UI 只负责渲染。

/** 全局 g+ 导航映射。 */
export const NAV_MAP = {
  h: 'index.html',
  c: 'cards.html',
  l: 'learn.html',
  e: 'experiments.html',
  v: 'verdicts.html',
  s: 'starmap.html',
};

/** 页面内快捷键（卡库 / 学习台）。 */
export const LOCAL_KEYS = ['/', 'j', 'k', 'Enter', 'Escape', ' ', 'ArrowLeft', 'ArrowRight', '1', '2', '3', '4'];

/** 快捷键帮助清单（供帮助弹窗渲染）。 */
export const HELP_ITEMS = [
  { keys: ['g', 'h'], desc: '跳到首页' },
  { keys: ['g', 'c'], desc: '跳到卡库' },
  { keys: ['g', 'l'], desc: '跳到学习台' },
  { keys: ['g', 'e'], desc: '跳到实验结果' },
  { keys: ['g', 'v'], desc: '跳到判决历史' },
  { keys: ['g', 's'], desc: '跳到知识星图' },
  { keys: ['/'], desc: '聚焦搜索框' },
  { keys: ['j', 'k'], desc: '下 / 上一张卡' },
  { keys: ['Enter'], desc: '打开卡详情' },
  { keys: ['1', '2', '3', '4'], desc: '学习页评分（SM-2）' },
  { keys: ['?'], desc: '打开本帮助' },
  { keys: ['Esc'], desc: '关闭弹窗 / 取消' },
];

/**
 * 把 keydown 事件归一为单键字符串（忽略带修饰键的普通按键）。
 * @returns {string|null} 'g' | 'Escape' | ... | null（应忽略）
 */
export function normalizeKey(ev) {
  if (ev.ctrlKey || ev.metaKey || ev.altKey) return null;
  const k = ev.key;
  if (k === 'Escape') return 'Escape';
  if (k === 'Enter') return 'Enter';
  if (k === ' ') return ' ';
  if (k === 'ArrowLeft') return 'ArrowLeft';
  if (k === 'ArrowRight') return 'ArrowRight';
  if (k === 'ArrowUp') return 'ArrowUp';
  if (k === 'ArrowDown') return 'ArrowDown';
  if (k.length === 1) return k;   // 字母 / 数字 / 符号（'?' '/' 等）
  return null;
}

/** 该按键是否应被忽略（焦点在输入控件里）。 */
export function isTypingTarget(tagName, isContentEditable) {
  const t = (tagName || '').toUpperCase();
  if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT') return true;
  return Boolean(isContentEditable);
}

/**
 * 处理 g 前缀序列。
 * @param {string|null} pending 上一次的待定键（'g' 或 null）
 * @param {string} key 本次归一化按键
 * @returns {{pending:string|null, nav:string|null}}
 */
export function resolveChord(pending, key) {
  if (pending === 'g') {
    const nav = NAV_MAP[key.toLowerCase()];
    return { pending: null, nav: nav || null };
  }
  if (key === 'g') return { pending: 'g', nav: null };
  return { pending: null, nav: null };
}

/** 焦点陷阱：在 [0,len) 内循环。 */
export function cycleIndex(current, len, shift) {
  if (len <= 0) return -1;
  if (shift) return (current - 1 + len) % len;
  return (current + 1) % len;
}

/** 搜索结果播报文案。 */
export function announceResults(shown, total) {
  if (total === 0) return '没有匹配项';
  if (shown === total) return `显示 ${shown} 条结果，共 ${total} 条`;
  return `筛选后显示 ${shown} 条，共 ${total} 条`;
}

/** 评分播报文案。 */
export function announceRating(grade) {
  const map = { 1: '薄弱', 2: '一般', 3: '良好', 4: '已掌握' };
  return `已标记为${map[grade] || '未知'}`;
}

/** 是否应按 Esc 关闭（有打开的弹窗时）。 */
export function shouldCloseOnEsc(dialogOpen) {
  return Boolean(dialogOpen);
}
