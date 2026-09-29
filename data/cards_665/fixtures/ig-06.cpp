#include <memory>
struct B; struct A{std::shared_ptr<B> b;}; struct B{std::weak_ptr<A> a;};
int main(){auto x=std::make_shared<A>(); x->b=std::make_shared<B>(); x->b->a=x;}
