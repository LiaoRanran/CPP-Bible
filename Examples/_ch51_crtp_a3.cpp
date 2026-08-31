template <typename D> struct AnimalCRTP { void speak() { static_cast<D*>(this)->speak_impl(); } };
struct DogCRTP : AnimalCRTP<DogCRTP> { int age; void speak_impl() { age += 1; } };
struct AnimalVirt { int age; virtual void speak() { age += 1; } virtual ~AnimalVirt() = default; };
struct DogFinal final : AnimalVirt { void speak() override { age += 2; } };

void crtp_dispatch(DogCRTP& d) { d.speak(); }    // ① CRTP 静态多态
void virt_dispatch(AnimalVirt* a) { a->speak(); } // ② 虚函数动态多态
void final_call(DogFinal* d) { d->speak(); }        // ③ final 类去虚拟化