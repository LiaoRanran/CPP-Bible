// ⑤ 跨平台 ABI 门禁：用 static_assert 锁定类型宽度
#include <cstdio>
#include <cstdint>

static_assert(sizeof(std::int32_t) == 4, "int32 must be 4 bytes");
static_assert(alignof(double) <= 8, "double alignment portable");

int main() {
    std::printf("abi: int32=%zu double_align=%zu\n",
                sizeof(std::int32_t), alignof(double));
    return 0;
}
