// [redacted]
// [redacted]
// [redacted]
// [redacted]
// [redacted]
#include <cstddef>
#include <cstdio>
#include <memory>

struct Link {
    std::shared_ptr<Link> next;          // 唯一的边：互指成环
    int tag = 0;
};

__attribute__((noinline)) static void build_cycle() {
    auto a = std::make_shared<Link>();
    auto b = std::make_shared<Link>();
    a->tag = 1;
    b->tag = 2;
    a->next = b;
    b->next = a;                         // 环
}

__attribute__((noinline)) static void scrub_stack() {
    volatile unsigned char buf[8192];
    for (std::size_t i = 0; i < sizeof(buf); ++i) {
        buf[i] = 0;
    }
}

int main() {
    build_cycle();
    scrub_stack();
    std::printf("two-node cycle built, blocks=2\n");
    return 0;                            // [redacted]
}
