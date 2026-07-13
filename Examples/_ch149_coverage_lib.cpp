// ⑧ 覆盖率取证库：gcov 插桩后统计行覆盖
int classify(int x) {
    if (x > 0) return 1;
    if (x < 0) return -1;
    return 0;
}
