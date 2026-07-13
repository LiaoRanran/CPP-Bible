#include <cstddef>
template <typename T, typename Storage = int>
struct Counter { T v{}; Storage hits = 0; void inc(){ ++hits; ++v; } };
int main(){ Counter<double> c; c.inc(); return (int)c.hits; }
