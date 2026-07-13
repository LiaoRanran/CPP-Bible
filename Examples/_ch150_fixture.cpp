// ③ 测试夹具：setup/teardown 等价 GoogleTest TestFixture
#include <cstdio>
#include <cstring>
#include <cassert>
struct StackFixture {
    int buf[8];
    int top;
    void SetUp() { top = 0; std::memset(buf, 0, sizeof buf); }
    void TearDown() { top = 0; }
    void push(int v) { buf[top++] = v; }
    int pop() { return buf[--top]; }
};
int main() {
    StackFixture f;
    f.SetUp();
    f.push(42); f.push(7);
    assert(f.pop() == 7);
    assert(f.pop() == 42);
    f.TearDown();
    std::printf("fixture: push/pop order preserved, teardown reset top=%d\n", f.top);
    return 0;
}
