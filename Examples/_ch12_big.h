#pragma once
#include <vector>
#include <string>
#include <map>
template <typename T, int N> struct Blob { T data[N]; };
template <typename T> T chain(T a, T b, T c, T d) { return a+b+c+d; }
namespace ch12 { inline int tag = 0; }
