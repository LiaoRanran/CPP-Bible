// ⑦ 极简测试框架：演示"测试门禁"聚合多用例
#include <cstdio>
#include <string>

struct Test {
    const char* name;
    bool (*fn)();
};

static int failures = 0;
void run(const Test* t, int n) {
    for (int i = 0; i < n; ++i) {
        bool ok = t[i].fn();
        std::printf("[%s] %s\n", ok ? "PASS" : "FAIL", t[i].name);
        if (!ok) ++failures;
    }
    std::printf("summary: failures=%d\n", failures);
}

bool t_add()  { return (1 + 1) == 2; }
bool t_sub()  { return (5 - 3) == 2; }
bool t_mul()  { return (4 * 3) == 12; }

int main() {
    Test ts[] = {{"add", t_add}, {"sub", t_sub}, {"mul", t_mul}};
    run(ts, 3);
    return failures == 0 ? 0 : 1;
}
