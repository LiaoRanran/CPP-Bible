#include <algorithm>
#include <vector>

struct Point { int x, y; };

// 用无状态 lambda 作为比较器：closure 类型可被 std::sort 内联展开
void sort_points_inline(std::vector<Point>& v) {
    std::sort(v.begin(), v.end(),
              [](const Point& a, const Point& b) { return a.x < b.x; });
}

int main() {
    std::vector<Point> v{{3,1},{1,9},{2,5},{4,0}};
    sort_points_inline(v);
    return v.front().x;
}
