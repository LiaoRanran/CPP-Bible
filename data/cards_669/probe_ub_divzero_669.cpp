// 669 P0-2 · 记录复算探针（**由 tools/ev_ub_atoms_669.py 从 data/cards_665/index_665.json 生成**，勿手改）
// 作用：把 665 的检测器记录变成**编译器可构建**的一行输出 ⇒ replay 的 run_match 可在任何平台复核
// （记录漂移 ⇒ 本探针输出与卡面 actual.run_* 不一致 ⇒ refute）。检测器**复跑**见卡面 reproduce。
#include <cstdio>
int main() {
    std::puts("EV-UB-DIVZERO-669 rec=index_665/ig-08 detector=ubsan verdict=catch sig=hit:runtime error fixture_file_sha=0981ce1e39152938820b9f37d4bbe0de8a36d71bd544c243d20b55d230764dd5 index_fixture_sha=bf80f5565f55bfdf80244141b2982316460e92b7a2b7dfb729c9feea5652be8d measured_at=2026-09-29T00:18:20");
    return 0;
}
