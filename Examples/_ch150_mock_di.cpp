// ④ 依赖注入：通过接口替换真实实现为测试替身（test double）
#include <cstdio>
#include <cstring>
#include <cassert>
struct IEmail { virtual ~IEmail() = default; virtual bool send(const char*) = 0; };
struct RealEmail : IEmail { bool send(const char*) override { return true; } };
struct FakeEmail : IEmail {
    int calls = 0; bool next = true;
    bool send(const char*) override { ++calls; return next; }
};
struct Service { IEmail& e; explicit Service(IEmail& e_) : e(e_) {} bool notify() { return e.send("hi"); } };
int main() {
    FakeEmail fake;
    Service s(fake);
    assert(s.notify() == true);
    fake.next = false;
    assert(s.notify() == false);
    std::printf("mock-di: fake.send called=%d times\n", fake.calls);
    return 0;
}
