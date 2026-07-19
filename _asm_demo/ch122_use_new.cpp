int* g_a;
int* g_b;
void use_new() {
    g_a = new int[10];
    g_b = new int[10];
    delete[] g_a;
    delete[] g_b;
}
