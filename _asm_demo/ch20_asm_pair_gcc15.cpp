void by_ref(int& r) { r++; }
void by_ptr(int* p) { if (p) (*p)++; }
int& first(int& a, int& b) { return a; }
