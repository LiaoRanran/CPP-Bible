// 演示：内联函数经 -O2 后在调用点消失（真实汇编证据）
// 文件：Examples/_ch16_inline.cpp
// 行号：8
inline int add_one(int x) { return x + 1; }
int caller(int a) { return add_one(a) * 2; }
