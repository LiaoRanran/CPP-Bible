#include <cstdio>
int main(){int* a=new int[4]{0};a[4]=1;std::printf("%d\n",a[4]);delete[] a;}
