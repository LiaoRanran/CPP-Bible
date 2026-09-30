// 669 P0-2 · 记录复算探针（**由 tools/ev_ub_atoms_669.py 从 data/cards_665/index_665.json 生成**，勿手改）
// 作用：把 665 的检测器记录变成**编译器可构建**的一行输出 ⇒ replay 的 run_match 可在任何平台复核
// （记录漂移 ⇒ 本探针输出与卡面 actual.run_* 不一致 ⇒ refute）。检测器**复跑**见卡面 reproduce。
#include <cstdio>
int main() {
    std::puts("EV-UB-NULLDEREF-669 rec=index_665/ig-07 detector=asan verdict=catch sig=hit:AddressSanitizer fixture_file_sha=f423aeded2974396b404757f6767382cfa9b5c7e15be8a6402e03d5b4b79eb34 index_fixture_sha=36c0ce69c63d19c29c1693394be197fd97d5aef124c0c6cef82f0c90064287e6 measured_at=2026-09-29T00:18:19");
    return 0;
}
