int compute_ec(int x, int& out){ if(x==0) return -1; out=x*2; return 0; }
int compute_ex(int x){ if(x==0) throw 1; return x*2; }
