int may_throw_div(int a, int b) {
    if (b == 0) throw "div by zero";
    return a / b;
}
int noexcept_add(int a, int b) noexcept { return a + b; }
int call_may_throw(int x, int y) { return may_throw_div(x, y); }
int call_noexcept(int x, int y) { return noexcept_add(x, y); }