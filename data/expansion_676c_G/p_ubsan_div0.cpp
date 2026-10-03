
#include <cstdio>
int main(){ volatile int z = 0; int x = 100 / z; printf("%d\n", x); return 0; }
