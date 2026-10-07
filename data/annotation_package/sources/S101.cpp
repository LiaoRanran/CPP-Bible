#include <memory>
int main(){std::auto_ptr<int> a(new int(1));std::auto_ptr<int> b(a);return *b;}
