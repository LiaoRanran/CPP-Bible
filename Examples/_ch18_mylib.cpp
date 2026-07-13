// _ch18_mylib.cpp —— 同一份实现，既编静态库(.a)也编动态库(.dll/.so)
int engine_compute(int x) { return x * x + 1; }

int engine_pipeline(int a, int b) { return engine_compute(a) + engine_compute(b); }
