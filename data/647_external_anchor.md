# 647 A4 · 外部锚接口（**只建接口 + 本地 mock，不真连外部服务**）

## 一、接口契约

```python
publish(hash) -> receipt          # 发布，拿回凭据
verify(hash, receipt) -> bool     # 第三方凭 hash + 凭据独立验证
```

## 二、提供方

| 提供方 | 已实现 | 需要人提供 | 说明 |
|---|---|---|---|
| `mock-local` | ✅ | — | 本地 mock：确定性凭据，篡改必检出（**不是独立锚**） |
| `github-gist` | ⛔ 只留接入点 | token, gist_id | 免费/可公开查；凭据是 gist revision，git 化后天然有时间线 |
| `rfc3161-timestamp` | ⛔ 只留接入点 | tsa_url, 预算确认 | 标准第三方时间戳（TSA 签名）；需要人选 TSA 并确认是否付费 |
| `opentimestamps` | ⛔ 只留接入点 | 是否接受链上成本/延迟 | 去中心化、可自证；确认成本与延迟后接入 |

## 三、把当前透明日志 anchor 发布到本地 mock

- 透明日志：**58** 条，末条 index=57
- anchor（末条 entry_hash）：`2da866b6a16288a095c8b0a32c8fa28410a2b7c5c6dd33f26a4fffcc80913b0f`
- receipt：`{"provider": "mock-local", "hash": "2da866b6a16288a095c8b0a32c8fa28410a2b7c5c6dd33f26a4fffcc80913b0f", "published_at": "2026-09-26T13:46:15Z", "receipt_id": "ea4b736204f5f1c9c1397843731b9cf3f4b1a98a10816e0c3f32eaac2f2568d8", "receipt_digest": "ea2cde5d6f11984a4674b6df7ab6ef852e0130f10a7847360be23ed4fbeb63f1"}`
- **验证可验：True**；改一个字符 ⇒ 检出：True

## 四、独立性的真实状态（不夸大）

| 级别 | 定义 | 本仓库 |
|---|---|---|
| L1 | 同进程自证 | ❌ |
| L2 | 同机独立进程/独立实现 | ✅ 已达（628/629 他验三件套） |
| L3 | 仓库外第三方可验（外部锚/TSA） | ⛔ **未达**（A4 只建接口） |
| L4 | 外部权威机构背书 | ⛔ 未达 |

## 诚实登记

1. **不真连外部服务**：本批没有联网、没有 token、没有 TSA ⇒ **独立性没有实际提升**（§十二.1）；
2. **本地 mock 不是独立锚**：它与日志同机同仓库 ⇒ 改仓库仍能同时改两者；
3. `verify()` 只证明「receipt 与 hash 自洽」，**不能**证明「发布者真在那一刻发布过」；
4. 三个接入点的 `publish/verify` **调用即抛 `AnchorNotImplemented`**（显式拒绝，不会静默退化成 mock）；
5. 用哪个服务是**交人裁决**（GitHub Gist / RFC3161 / OpenTimestamps）。
