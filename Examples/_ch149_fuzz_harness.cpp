// ⑭ 模糊测试目标骨架：libFuzzer 风格入口（本机无 fuzzer 时仅编译门禁）
#include <cstddef>
#include <cstdio>

// LLVMFuzzerTestOneInput 是 libFuzzer 约定的入口；此处保证可编译
extern "C" int LLVMFuzzerTestOneInput(const unsigned char* data, std::size_t size) {
    if (size >= 2 && data[0] == 'C' && data[1] == 'I') {
        // 触发某个解析分支
        volatile int sink = data[size - 1];
        (void)sink;
    }
    return 0;
}

int main() {
    std::printf("fuzz harness compiled (no libFuzzer linked locally)\n");
    return 0;
}
