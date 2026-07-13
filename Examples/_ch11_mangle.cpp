// _ch11_mangle.cpp : 不同签名 -> Itanium mangling 对照（均给出定义，符号真实存在）
int         g(int, double)          { return 0; }
void        h(char)                 { }
long        k(short, int*, long)    { return 0; }
double      area_of_circle(double r){ return 3.141592653589793 * r * r; }
namespace ns { int q(int x)         { return x; } }
template<typename T> T id(T x)      { return x; }
template int id<int>(int);
