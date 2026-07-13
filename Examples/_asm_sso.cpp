// SSO 取证：短串不分配堆，长串走堆
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_sso.cpp -o _asm_sso.asm
#include <string>
int use_sso() {
    std::string a = "hi";                 // 短 -> 内联缓冲，无 new
    std::string b = "this is a long string that exceeds the small buffer"; // 长 -> 堆
    return (int)a.size() + (int)b.size();
}
