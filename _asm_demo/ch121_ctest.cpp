int f(int x) [[post: x > 0]] {
    return x + 1;
}
int g(int x) {
    return f(x);
}
