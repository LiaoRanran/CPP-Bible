// 669 P0-2 · 记录复算探针（**由 tools/ev_ub_atoms_669.py 从 data/cards_665/index_665.json 生成**，勿手改）
// 作用：把 665 的检测器记录变成**编译器可构建**的一行输出 ⇒ replay 的 run_match 可在任何平台复核
// （记录漂移 ⇒ 本探针输出与卡面 actual.run_* 不一致 ⇒ refute）。检测器**复跑**见卡面 reproduce。
#include <cstdio>
int main() {
    std::puts("EV-UB-OOB-669 rec=index_665/ig-02 detector=asan verdict=catch sig=hit:AddressSanitizer fixture_file_sha=31294d437366433bf14d909fbc8b40b5ab58951c1788ee81bd830118b5236b65 index_fixture_sha=e2f9abdb484ef6d8a81bb34f14a01ea947ae449c5f4c6086c92f7764522de400 measured_at=2026-09-29T00:18:16");
    return 0;
}
