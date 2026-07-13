// 文件：Examples/_ch160_valloc.cpp
// 行号：1
// 平台差异取证：Windows VirtualAlloc 按页申请/释放（本机 MinGW g++ -O2 实测通过）
#include <windows.h>
#include <cstdio>

int main() {
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    std::printf("page size = %u bytes\n", static_cast<unsigned>(si.dwPageSize));
    void* mem = VirtualAlloc(nullptr, si.dwPageSize * 64,
                             MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    std::printf("VirtualAlloc -> %p\n", mem);
    VirtualFree(mem, 0, MEM_RELEASE);
    std::printf("VirtualFree OK\n");
    return 0;
}
