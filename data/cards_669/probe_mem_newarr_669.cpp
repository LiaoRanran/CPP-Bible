// 669 P0-2 · 记录复算探针（**由 tools/ev_ub_atoms_669.py 从 data/cards_665/index_665.json 生成**，勿手改）
// 作用：把 665 的检测器记录变成**编译器可构建**的一行输出 ⇒ replay 的 run_match 可在任何平台复核
// （记录漂移 ⇒ 本探针输出与卡面 actual.run_* 不一致 ⇒ refute）。检测器**复跑**见卡面 reproduce。
#include <cstdio>
int main() {
    std::puts("EV-MEM-NEWARR-669 rec=index_665/ig-14 detector=asan verdict=catch sig=hit:AddressSanitizer fixture_file_sha=cb38bdb21e113142457c900c00b02712fbba8a5fd65e6caa0cd39cf571bde71d index_fixture_sha=3557ed2c40078bff7c4aa77f858d25513ee08cbbcd7e975dd67e35dd02855c5c measured_at=2026-09-29T00:18:22");
    return 0;
}
