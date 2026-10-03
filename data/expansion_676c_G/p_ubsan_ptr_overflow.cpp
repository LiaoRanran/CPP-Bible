
#include <cstdio>
int main(){ volatile long off = -2147483647L; const char* p = (const char*)0x1000; const char* q = p + off; printf("%p\n", (void*)q); return 0; }
