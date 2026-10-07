#include <vector>
#include <cstdio>
int main(){std::vector<int> v{1,2,3};auto it=v.begin();v.reserve(1024);std::printf("%d\n",*it);}
