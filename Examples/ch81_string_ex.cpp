// ① 最简形态：值语义，拷贝即独立副本
#include <string>
std::string a = "hello";
std::string b = a;          // 深拷贝，b 与 a 相互独立
b[0] = 'H';                 // 修改 b 不影响 a