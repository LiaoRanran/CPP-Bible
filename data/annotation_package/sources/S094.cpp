#include <thread>
#include <cstdio>
int g=0;
void w(){ for(int i=0;i<200000;++i) ++g; }
int main(){ std::thread a(w), b(w); a.join(); b.join(); std::printf("%d\n", g); return 0; }
