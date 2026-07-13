// ⑬ 汇编取证片段：Ring::push 的 tail=(tail+1)%16 在 -O2 下的真实产物
// 见 _ch164_framework_rb.asm（g++ -O2 -masm=intel）
#include <cstddef>
struct Ring {
    char buf[16]; int head = 0, tail = 0;
    void push(char c);
};
// 定义放在 TU 内，避免被整体常量折叠，迫使编译器生成取模序列
void Ring::push(char c) {
    buf[tail] = c;
    tail = (tail + 1) % 16;
}
int demo(Ring& r, char c) { r.push(c); return r.tail; }
