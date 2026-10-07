// [redacted]
// [redacted]
// [redacted]
#include <cstdio>

struct Base {
    virtual int f() { return 1; }
    virtual ~Base() = default;
};

int main() {
    Base b;
    // [redacted]
    *reinterpret_cast<void**>(&b) = nullptr;   // [redacted]
    std::printf("calling virtual...\n");
    return b.f();                               // [redacted]
}
