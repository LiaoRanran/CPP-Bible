// ch158 perf_antipatterns —— 真实反汇编证据源：虚函数间接调用（§⑤）
// 动态类型在编译期未知，s.area() 必须走 vtable 间接调用，无法内联/去虚拟化。
struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };
struct Circle : Shape { double r; double area() const override; };
double Circle::area() const { return 3.141592653589793 * r * r; }

double compute_area(const Shape& s) __attribute__((used));
double compute_area(const Shape& s) { return s.area(); }   // 间接调用：call [vtable+offset]
