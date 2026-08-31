// 【程序 11】数组求和：无 restrict
void sum_norestrict(double* dest, const double* src, int n) {
    for (int i = 0; i < n; ++i) dest[i] += src[i];
}

// 【程序 12】数组求和：加 __restrict
void sum_restrict(double* __restrict dest, const double* __restrict src, int n) {
    for (int i = 0; i < n; ++i) dest[i] += src[i];
}