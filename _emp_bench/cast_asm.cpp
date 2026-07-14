#include <typeinfo>
struct Base { virtual ~Base()=default; virtual int f(){return 1;} };
struct Right { virtual ~Right()=default; virtual int g(){return 2;} int r=0; };
struct Most : Base, Right { int m=0; };
int use_static(Most* p){ Right* q=static_cast<Right*>(p); return q->g()+q->r; }
int use_dynamic(Base* p){ Right* q=dynamic_cast<Right*>(p); return q? q->g():0; }
int main(){ Most m; return use_static(&m)+use_dynamic(&m); }
