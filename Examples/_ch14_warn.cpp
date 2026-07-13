// _ch14_warn.cpp — 触发编译器诊断（真实警告取证）
int maybe_uninit() {
    int x;            // 从未初始化
    return x;         // -Wall -Wextra 会报“可能未初始化”
}

int main() {
    return maybe_uninit();
}
