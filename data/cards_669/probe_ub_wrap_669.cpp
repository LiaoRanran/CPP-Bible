// 669 P0-2 · 记录复算探针（**由 tools/ev_ub_atoms_669.py 从 data/cards_665/index_665.json 生成**，勿手改）
// 作用：把 665 的检测器记录变成**编译器可构建**的一行输出 ⇒ replay 的 run_match 可在任何平台复核
// （记录漂移 ⇒ 本探针输出与卡面 actual.run_* 不一致 ⇒ refute）。检测器**复跑**见卡面 reproduce。
#include <cstdio>
int main() {
    std::puts("EV-UB-WRAP-669 rec=index_665/ig-01 detector=ubsan verdict=catch sig=hit:runtime error fixture_file_sha=a6e43581ac0874820048fa276a405e0382968bb6161584944be43530bc47d847 index_fixture_sha=dda4a791a7d627098a6d82955fb5a1ec512ab6c29285464ab07926b86b0847bd measured_at=2026-09-29T00:18:15");
    return 0;
}
