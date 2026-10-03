
#include <cstdlib>
int main(){ char* p = (char*)malloc(10); realloc(p, 20); return p != 0 ? 0 : 1; }
