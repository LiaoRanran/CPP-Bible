// 656 C2 · 组件出口：一次性注册全部 QueYi Web Component
// 页面只需：`import './components/index.js';`（或 `<script type="module" src="components/index.js">`）
//
// 673m 修复：672b 减法批次删掉了 qy-card / qy-panel / qy-tag / qy-status 四个组件文件，
//   但漏改本文件 ⇒ 这里仍 re-export 已删模块 ⇒ import 本文件时抛 ERR_MODULE_NOT_FOUND。
//   后果不是"少几个组件"，而是**整条 export 链断掉**：7 个页面（index / cards / card /
//   learn / starmap / experiments / verify）的 module 脚本全部加载失败，连存活的 QyNav
//   也注册不上 —— 导航条全站失效。收敛为实际存在的两个组件，恢复全站脚本可加载。
export { QyNav } from './qy-nav.js';
export { QyButton } from './qy-button.js';

export const COMPONENTS = ['qy-nav', 'qy-button'];
