// ⑮  unity build：把多个 TU 合并成一个翻译单元，减少头文件重解析
#include "ch149_u_a.cpp"
#include "ch149_u_b.cpp"

int main() {
    std::printf("unity: %d %d\n", module_a(), module_b());
    return 0;
}
