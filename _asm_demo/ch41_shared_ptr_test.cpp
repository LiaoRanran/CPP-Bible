// Phase 5 批 A·ASM-41-shared_ptr：shared_ptr 拷贝构造的引用计数原子递增
// 编译: g++ -std=c++26 -O2 -c ch41_shared_ptr_test.cpp -o ch41_shared_ptr_test.o
// 反汇编: objdump -d -M intel -C ch41_shared_ptr_test.o
#include <memory>

struct S { int x; };

// 返回 p 触发 shared_ptr 拷贝构造 → 引用计数原子递增
[[gnu::noinline]] std::shared_ptr<S> clone(const std::shared_ptr<S>& p) { return p; }

[[gnu::noinline]] std::shared_ptr<S> make_one() { return std::make_shared<S>(S{42}); }

int main() {
    auto p = make_one();
    auto q = clone(p);   // 此处引用计数 +1（lock 前缀原子操作）
    return q->x;
}
