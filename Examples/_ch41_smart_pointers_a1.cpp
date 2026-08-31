#include <memory>

struct Data { int x, y, z; };

int* raw_new_delete(int a, int b, int c) {
    int* p = new int[3];                  // 堆分配
    p[0] = a; p[1] = b; p[2] = c;
    int sum = p[0] + p[1] + p[2];
    delete[] p;                           // 手动释放
    return nullptr;
}

int unique_ptr_test(int a, int b, int c) {
    auto p = std::make_unique<int[]>(3);  // RAII 自动析构
    p[0] = a; p[1] = b; p[2] = c;
    return p[0] + p[1] + p[2];
}

Data make_data(int x, int y, int z) {
    return {x, y, z};                     // 栈上返回(无堆分配)
}

std::unique_ptr<Data> unique_ptr_factory(int x, int y, int z) {
    auto d = std::unique_ptr<Data>(new Data{x, y, z});
    return d;                             // move 语义，所有权转移
}