// 文件：Examples/_ch99_inner_product.cpp
// 行号：9 (dot) / 14 (axpy_reduce)
#include <numeric>
#include <vector>
#include <iostream>

// 点积：sum_i a[i]*b[i]
double dot(const std::vector<double>& a, const std::vector<double>& b) {
    return std::inner_product(a.begin(), a.end(), b.begin(), 0.0);
}

// 加权累加：init + Σ f(a[i])*b[i]
double axpy_reduce(const std::vector<double>& a, const std::vector<double>& b) {
    return std::inner_product(a.begin(), a.end(), b.begin(), 100.0,
        std::plus<>(),
        [](double x, double y) { return (x - 1.0) * y; });
}

int main() {
    std::vector<double> a{1,2,3}, b{4,5,6};
    std::cout << dot(a,b) << " " << axpy_reduce(a,b) << "\n";
}
