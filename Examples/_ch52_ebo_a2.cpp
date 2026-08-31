#include <cstddef>
struct Empty {};
struct Derived : Empty { int x; };
struct AsMember { Empty e; int x; };
static_assert(sizeof(Derived) == sizeof(int));
static_assert(sizeof(AsMember) == 2 * sizeof(int));
int read_derived(Derived* p) { return p->x; }
int read_member(AsMember* p) { return p->x; }