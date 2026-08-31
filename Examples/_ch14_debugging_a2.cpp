// 文件：Examples/_ch14_opt.cpp
// 行号：2
// ⑱ 同一计算，-O0 保留循环，-O2 被识别为可约简的闭式
int sum_to(int n) {
    int s = 0;
    for (int i = 1; i <= n; ++i) s += i;   // 行4：O0 真循环，O2 优化掉
    return s;
}