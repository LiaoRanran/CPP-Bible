#include "_ch12_big.h"
int tu_3(int x){ return (int)ch12::tag + chain(x,x,x,x) + (int)sizeof(Blob<int,3>); }
