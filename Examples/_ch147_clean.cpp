#include <cstdio>
#include <vector>
int sum(const std::vector<int>& v) {
    int s = 0;
    for (std::size_t i = 0; i < v.size(); ++i) s += v[i];
    return s;
}
int main(){ std::vector<int> v{1,2,3}; std::printf("%d\n", sum(v)); }
