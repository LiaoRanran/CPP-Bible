#include <thread>
#include <vector>
#include <cstdio>
std::vector<int> v;
void w(){ for(int i=0;i<5000;++i) v.push_back(i); }
int main(){ std::thread a(w), b(w); a.join(); b.join(); std::printf("%zu\n", v.size()); return 0; }
