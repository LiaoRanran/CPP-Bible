---
id: MIS-PERF-001
name: std::endl 和 \n 是一样的，只是写法不同
level: surface
domain: PERF
trigger_patterns:
  - "endl 就是换行的标准写法"
  - "用 endl 更规范"
refutations:
  - "std::endl 除了写 \n 还强制 flush → 每次都触发系统调用；热路径吞吐差距可达量级"
source: ch158_perf_antipatterns.md ㉒.3 / 附录 I
related_atoms: []
---

# MIS-PERF-001 · std::endl 和 \n 是一样的，只是写法不同

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- endl 就是换行的标准写法
- 用 endl 更规范

## 为什么它不成立
1. std::endl 除了写 \n 还强制 flush → 每次都触发系统调用；热路径吞吐差距可达量级

## 出处与关联

- 出处：ch158_perf_antipatterns.md ㉒.3 / 附录 I
- 关联原子：（暂无，待相关原子锻造后回填）
