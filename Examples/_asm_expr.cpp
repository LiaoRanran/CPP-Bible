// 表达式模板（Expression Templates）取证：延迟求值 vs 立即求值
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_expr.cpp -o _asm_expr.asm
#include <cstdlib>

// 朴素 Vec：operator+ 立即遍历并分配临时
struct Naive {
    double* p; size_t n;
    Naive(size_t k) : n(k), p(new double[k]) {}
    ~Naive() { delete[] p; }
    Naive operator+(const Naive& o) const {
        Naive r(n);
        for (size_t i = 0; i < n; ++i) r.p[i] = p[i] + o.p[i];  // 立即遍历 + 堆分配
        return r;
    }
};

// 表达式模板 Vec：operator+ 返回代理（不计算）
template <typename E> struct Expr {
    double operator[](size_t i) const { return static_cast<const E&>(*this)[i]; }
    size_t size() const { return static_cast<const E&>(*this).size(); }
};
struct Fast : Expr<Fast> {
    double* p; size_t n;
    Fast(size_t k) : n(k), p(new double[k]) {}
    ~Fast() { delete[] p; }
    double operator[](size_t i) const { return p[i]; }
    size_t size() const { return n; }
    template <typename O> Fast& operator=(const Expr<O>& e) {
        for (size_t i = 0; i < e.size(); ++i) p[i] = e[i];   // 单次遍历完成全部计算
        return *this;
    }
};
template <typename A, typename B>
struct Sum : Expr<Sum<A,B>> {
    const A& a; const B& b;
    Sum(const A& x, const B& y) : a(x), b(y) {}
    double operator[](size_t i) const { return a[i] + b[i]; }
    size_t size() const { return a.size(); }
};
template <typename A, typename B>
Sum<A,B> operator+(const Expr<A>& x, const Expr<B>& y) {
    return Sum<A,B>(static_cast<const A&>(x), static_cast<const B&>(y));  // 仅构造代理，不计算
}

int use_naive(int n) {
    Naive a(n), b(n), c(n);
    for (int i = 0; i < n; ++i) { a.p[i] = i; b.p[i] = i + 1; c.p[i] = i + 2; }
    Naive u = a + b + c;            // 2 次额外 new + 2 次遍历
    return (int)u.p[n - 1];
}
int use_expr(int n) {
    Fast a(n), b(n), c(n);
    for (int i = 0; i < n; ++i) { a.p[i] = i; b.p[i] = i + 1; c.p[i] = i + 2; }
    Fast u(n);
    u = a + b + c;                  // 0 次额外 new + 1 次遍历（压缩为单循环）
    return (int)u.p[n - 1];
}
