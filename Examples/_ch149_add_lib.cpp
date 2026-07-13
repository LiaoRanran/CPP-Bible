// ③ 被测库：简单的整数运算，用于覆盖率取证
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }
int divi(int a, int b) { return b == 0 ? 0 : a / b; }
