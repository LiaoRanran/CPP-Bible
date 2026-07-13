# 0 "_ch144_include_guard.cpp"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "_ch144_include_guard.cpp"



struct Widget {
    int id;
    double weight;
};

inline int make_id(Widget& w) { return ++w.id; }
