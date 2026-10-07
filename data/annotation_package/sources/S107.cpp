#include <vector>
int main(){std::vector<int> v={1,2,3};int*p=&v[0];v.resize(1000);return *p;}
