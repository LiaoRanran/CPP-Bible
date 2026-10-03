
int rec(int n){ char pad[16]; pad[0] = (char)n; if (n <= 0) return 0; return 1 + rec(n - 1) + pad[0]; }
int main(){ return rec(5000000) > 0 ? 1 : 0; }
