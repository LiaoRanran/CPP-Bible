int abs_pos(int x) [[pre: x >= 0]] {
    return x;
}
int user(int v) {
    return abs_pos(v);
}
