// _ch11_vtable.cpp : 含虚函数的类，用于观察 vtable / RTTI 段布局
struct Shape {
    virtual ~Shape();
    virtual double area() const;
    virtual int    sides() const;
};

double Shape::area() const { return 0.0; }
int    Shape::sides() const { return 0; }
Shape::~Shape() {}

struct Circle : Shape {
    double r;
    double area() const override { return 3.141592653589793 * r * r; }
    int    sides() const override { return 0; }
};

double total_area(const Shape& s) { return s.area(); }
