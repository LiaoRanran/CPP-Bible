// 【程序 8】优化武器化：int* 与 float* 被假定不 alias
void f(int* p, float* q, int n) {
    for (int i = 0; i < n; ++i) {
        *p += 1;
        *q += 1.0f;
    }
}