#include <algorithm>
#include <vector>

struct Point { int x, y; };

// 自定义比较器：按 x 升序。将观察其是否内联进排序循环。
bool by_x(const Point& a, const Point& b) {
    return a.x < b.x;
}

void sort_points(std::vector<Point>& v) {
    std::sort(v.begin(), v.end(), by_x);
}

int main() {
    std::vector<Point> v{{3,1},{1,9},{2,5},{4,0}};
    sort_points(v);
    return v.front().x;
}
