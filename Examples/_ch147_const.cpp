struct Vec { double x=0,y=0; double len() { return x*x+y*y; } }; // 应 const
int main(){ Vec v; (void)v.len(); }
