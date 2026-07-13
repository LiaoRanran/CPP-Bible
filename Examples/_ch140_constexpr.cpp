constexpr int select(bool b){ return b ? 1 : 2; }
int main(){ constexpr int x = select(true); return x; }
