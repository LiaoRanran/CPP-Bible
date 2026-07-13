# benchmarks/ — 性能基准测试集

> 存放各章 microbenchmark 的可独立编译版本。
> 编译: `g++ -std=c++23 -O2 -o bench_xxx.exe bench_xxx.cpp`

## 已有基准（从章节提取）

| 文件 | 来源章 | 测试内容 |
|---|---|---|
| (待提取) | ch152/154/156 | cache/bandwidth/latency benchmarks |

## 使用

```bash
cd benchmarks
g++ -std=c++23 -O2 -Wall -o bench_xxx.exe bench_xxx.cpp
./bench_xxx.exe
```
