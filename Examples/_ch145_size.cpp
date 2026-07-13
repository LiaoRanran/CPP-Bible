// _ch145_size.cpp —— Pimpl 的 ABI 稳定性：头文件大小与实现无关（g++ 运行取证）
#include <memory>
#include <cstdio>

struct FatImpl { long a[64]; };          // 实现很"胖"

class PimplWidget {                       // 头文件只露指针
    std::unique_ptr<FatImpl> impl_;
public:
    PimplWidget();
    ~PimplWidget();
};

class FatWidget {                         // 无 Pimpl：实现直接内联进头
    long a[64];
public:
    FatWidget() = default;
};

int main() {
    std::printf("sizeof(PimplWidget)=%zu\n", sizeof(PimplWidget));
    std::printf("sizeof(FatWidget) =%zu\n", sizeof(FatWidget));
    return 0;
}
