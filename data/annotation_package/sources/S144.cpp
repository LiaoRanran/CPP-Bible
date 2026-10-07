#include <cstdio>
int main(){int* p=new int(1);delete p;*p=2;std::printf("%d\n",*p);}
