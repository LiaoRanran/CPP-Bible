#include <iostream>
consteval int factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }
int main() {
    int x = factorial(5);
    std::cout << x << "\n";
    return 0;
}
