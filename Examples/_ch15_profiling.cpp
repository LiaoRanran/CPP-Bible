#include <chrono>
long long f(){ auto t=std::chrono::steady_clock::now(); return (long long)t.time_since_epoch().count(); }
