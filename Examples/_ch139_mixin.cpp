// _ch139_mixin.cpp
// 取证目的：多重继承叠加多个 CRTP mixin，组合能力而不引入虚函数。
#include <iostream>

template <typename Derived>
struct Printable {
    void print_type() const {
        std::cout << static_cast<const Derived*>(this)->type_name() << "\n";
    }
};
template <typename Derived>
struct Serializable {
    void save() const {
        std::cout << "save " << static_cast<const Derived*>(this)->type_name() << "\n";
    }
};

struct Entity : Printable<Entity>, Serializable<Entity> {
    const char* type_name() const { return "Entity"; }
};

int main() {
    Entity e;
    e.print_type();
    e.save();
}
