// [redacted]
// [redacted]
// [redacted]
// [redacted]
// [redacted]
//   wsl.exe -e bash -lc "g++ -std=c++11 -g -fsanitize=address \
// [redacted]
// [redacted]
#include <cstdlib>

struct Holder {
    int* data;
    Holder() : data(new int(42)) {}
    ~Holder() { delete data; }            // [redacted]
};

int main() {
    Holder* a = new Holder();
    Holder b = *a;                        // [redacted]
    delete a;                            // 第一次释放
    return 0;                            // [redacted]
}
