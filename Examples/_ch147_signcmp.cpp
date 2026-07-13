#include <vector>
#include <cstdio>
void f(const std::vector<int>& v, int n) {
    if (n < v.size())           // int 与 size_t 比较
        std::printf("ok\n");
}
int main(){ std::vector<int> v; f(v, 0); }
