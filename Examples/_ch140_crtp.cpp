template <typename Derived> struct Base { void f(){ static_cast<Derived*>(this)->impl(); } };
struct D : Base<D> { void impl(){} };
int main(){ D d; d.f(); return 0; }
