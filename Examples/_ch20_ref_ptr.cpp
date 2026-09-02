// Examples/_ch20_ref_ptr.cpp
// ch20 真机证据：引用参数 = 按指针 ABI 传址（GCC 15.3.0 -O2）
void by_ref(int& r) { r++; }
void by_ptr(int* p) { if (p) (*p)++; }
