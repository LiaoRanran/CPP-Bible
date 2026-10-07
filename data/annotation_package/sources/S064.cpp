#include <cstdio>
int main(){ int* a = new int[4]; a[0]=1; std::printf("%d\n", a[0]); delete a; return 0; }
