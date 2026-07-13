// _ch18_main.cpp —— 调用 compute（定义位于 _ch18_lib.cpp，另一 TU）
int compute(int);

int driver(int a) {
    // 无 LTO：此处为 call compute，compute 内再 call helper。
    // 有 LTO：compute 与 helper 在链接期被内联进 driver，无 call。
    return compute(a) + compute(a + 1);
}

int main() { return driver(1); }
