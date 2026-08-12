// ch97 真实汇编证据源：lower_bound 二分下界（GCC 15.3.0 -O2 -masm=intel）
// 完整产物见 Examples/_ch97_search_lower_bound_idx.asm
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch97_search_lower_bound_idx.cpp -o _ch97_search_lower_bound_idx.asm
int lower_bound_idx(const int* first, int n, int value) __attribute__((used));

int lower_bound_idx(const int* first, int n, int value) {
    const int* base = first;
    while (n > 0) {
        int mid = n / 2;
        if (*(first + mid) < value) {
            first = first + mid + 1;
            n -= mid + 1;
        } else {
            n = mid;
        }
    }
    return int(first - base);
}
