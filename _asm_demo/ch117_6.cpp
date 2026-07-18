#include <cstdio>
struct Big { long a[8]; Big(){a[0]=1;} Big(const Big& o){std::printf("copy ctor!\n"); a[0]=o.a[0];} };
Big make_forced(const Big& src) {
    Big b = src;     // 必须从实参拷贝构造（不可省略）
    return b;        // 返回 b 可被 NRVO，但 b 本身的构造不能省
}
int main(){ Big x = make_forced(Big{}); (void)x; }
