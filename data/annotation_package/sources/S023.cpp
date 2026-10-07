#include <cstdio>
int g(){std::printf("g");return 1;}int h(){std::printf("h");return 2;}
void f(int,int){}
int main(){f(g(),h());}
