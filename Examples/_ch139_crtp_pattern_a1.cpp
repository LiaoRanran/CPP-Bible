struct ShapeV { virtual double area() const = 0; virtual ~ShapeV() = default; };
struct CircleV : ShapeV {
    double r;
    CircleV(double r_) : r(r_) {}
    double area() const override { return 3.141592653589793 * r * r; }
};

template <typename Derived>
struct ShapeC { double area() const { return static_cast<const Derived*>(this)->area_impl(); } };
struct CircleC : ShapeC<CircleC> {
    double r;
    CircleC(double r_) : r(r_) {}
    double area_impl() const { return 3.141592653589793 * r * r; }
};

double process_v(const ShapeV& s)      { return s.area() * 2.0; }
double process_c(const ShapeC<CircleC>& s) { return s.area() * 2.0; }