// ⑬ 参数化测试：以数据集驱动同一断言（等价 GoogleTest TEST_P）
#include <cstdio>
#include <cassert>
static int abs_val(int x) { return x < 0 ? -x : x; }
int main() {
    int data[] = { 0, 1, -1, 42, -42, 1000, -1000 };
    int n = (int)(sizeof(data)/sizeof(data[0]));
    for (int i = 0; i < n; ++i) {
        int x = data[i];
        assert(abs_val(x) >= 0);
        assert(abs_val(x) == abs_val(-x));
    }
    std::printf("param: abs_val over %d params OK\n", n);
    return 0;
}
