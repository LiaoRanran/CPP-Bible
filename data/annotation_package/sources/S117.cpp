#include <functional>
#include <cstdio>
std::function<int()> g;
void setup(){ int x = 7; g = [&x]{ return x; }; }
int main(){ setup(); std::printf("%d\n", g()); return 0; }
