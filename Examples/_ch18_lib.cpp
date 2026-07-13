// _ch18_lib.cpp —— 被 LTO 跨 TU 内联的库实现（无 static / 可外部链接）
int helper(int x) { return x * 2 + 1; }

int compute(int a) { return helper(a) + helper(a); }
