# 651 H7 · 外部变更订阅清单（证据时效）

> 证据会因**外部世界变化**而过期。以下清单供人工定期核对（本工具不抓网，只列清单）。

## 一、标准 issue log（条款可能改）
| 来源 | 地址 | 频率 |
|---|---|---|
| WG21（C++）邮件/issue | https://wg21.link/ / https://github.com/cplusplus/papers | 季度 |
| WG14（C）文档 | https://www.open-std.org/jtc1/sc22/wg14/www/docs/ | 季度 |
| cppreference 变更 | https://en.cppreference.com/w/ | 季度 |

## 二、编译器状态页（实测结论可能失效）
| 来源 | 地址 | 关注 |
|---|---|---|
| GCC release notes | https://gcc.gnu.org/gcc-15/changes.html | 语义/优化变更 |
| Clang release notes | https://releases.llvm.org/ | 语义/优化变更 |
| MSVC 更新 | https://learn.microsoft.com/en-us/cpp/ | 语义变更 |

## 三、触发口径
当上游发布新版本/新条款 ⇒ 相关卡 `recheck_after` 提前，重跑 L1 实测（648 探针模板）。
