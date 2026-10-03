#include <csignal>
#include <cstdio>
static int shared=0;
extern "C" void h(int){ std::printf("x"); shared++; }
int main(){ std::signal(SIGUSR1,h); raise(SIGUSR1); (void)shared; return 0; }
