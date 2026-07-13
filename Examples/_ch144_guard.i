# 0 "_ch144_guard_main.cpp"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "_ch144_guard_main.cpp"


# 1 "_ch144_guard.h" 1




struct Widget {
    int id;
    int value;
};
# 4 "_ch144_guard_main.cpp" 2


int main() {
    Widget w{42, 7};
    return w.id + w.value;
}
