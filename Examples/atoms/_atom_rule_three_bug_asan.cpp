// Examples/_atom_rule_three_bug_asan.cpp
// 服务 ATOM-MEM-RAII-002 / EV-MEM-024 的第二证据腿（WSL ASan 人工复现口径）。
// 与 _atom_rule_three_bug.cpp 的 Buggy 同型：只写析构、不写拷贝 → 隐式浅拷贝；
// 差异仅在于析构**真释放**（观测型析构不释放，见主夹具），从而使 double free 真实发生、
// 可被 AddressSanitizer 捕获。复现命令（Ubuntu g++ 13.3.0，与 CI 同版）：
//   wsl.exe -e bash -lc "g++ -std=c++11 -g -fsanitize=address \
//     Examples/_atom_rule_three_bug_asan.cpp -o build/_rtb_asan && ./build/_rtb_asan"
// 预期输出首行：ERROR: AddressSanitizer: attempting double-free ... in Buggy::~Buggy()
#include <cstdlib>

struct Buggy {
    int* data;
    Buggy() : data(new int(42)) {}
    ~Buggy() { delete data; }            // 与主夹具的唯一差异：真释放（double free 的成因）
};

int main() {
    Buggy* a = new Buggy();
    Buggy b = *a;                        // 隐式浅拷贝：b.data == a->data
    delete a;                            // 第一次释放
    return 0;                            // b 析构 → 第二次释放同一块 → double free
}
