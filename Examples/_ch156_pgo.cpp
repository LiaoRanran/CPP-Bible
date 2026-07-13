int g_sink = 0;
int cold(int x) { int s = 0; for (int i = 0; i < 64; ++i) s += x; g_sink += s; return s; }
int process(const int* arr, int n) {
    int sum = 0;
    for (int i = 0; i < n; ++i) {
        if (arr[i] >= 0) sum += arr[i];          // 热路径：占训练数据 ~99%
        else sum += cold(arr[i]);                // 冷路径：含全局副作用，无法被 cmov 合并
    }
    return sum;
}
int main() {
    int buf[2048];
    for (int i = 0; i < 2048; ++i) buf[i] = (i % 97 == 0) ? -i : i;
    return process(buf, 2048);
}
