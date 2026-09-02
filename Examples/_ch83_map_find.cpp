// Examples/_ch83_map_find.cpp
// ch83 真机证据：std::map::find 树下降（GCC 15.3.0 -O2 -masm=intel）
#include <map>

int lookup(const std::map<int, int>& m, int k) {
    auto it = m.find(k);
    return it == m.end() ? -1 : it->second;
}
