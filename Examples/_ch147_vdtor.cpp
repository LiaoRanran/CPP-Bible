struct Base { ~Base() {} };            // 析构非 virtual
struct Derived : Base { int* p = new int(0); ~Derived(){ delete p; } };
int main(){ Base* b = new Derived; delete b; }  // 未调用 Derived::~Derived
