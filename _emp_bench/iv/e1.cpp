#include <cstddef>
#include <array>
#include <new>
#include <utility>
template <class T, std::size_t N>
class StaticVector {
    alignas(T) unsigned char buf_[N * sizeof(T)];
    std::size_t size_ = 0;
public:
    bool push_back(const T& v) {
        if (size_ >= N) return false;
        ::new (&buf_[size_ * sizeof(T)]) T(v);
        ++size_; return true;
    }
    T& operator[](std::size_t i) {
        return *std::launder(reinterpret_cast<T*>(&buf_[i * sizeof(T)]));
    }
    std::size_t size() const noexcept { return size_; }
    ~StaticVector() { for (std::size_t i=0;i<size_;++i) (*this)[i].~T(); }
};
int main(){ StaticVector<int,4> v; v.push_back(1); v.push_back(2); return v[0]+v[1]+(int)v.size(); }
