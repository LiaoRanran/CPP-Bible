#ifndef CH144_INCLUDE_GUARD_H
#define CH144_INCLUDE_GUARD_H

struct Widget {
    int id;
    double weight;
};

inline int make_id(Widget& w) { return ++w.id; }

#endif // CH144_INCLUDE_GUARD_H
