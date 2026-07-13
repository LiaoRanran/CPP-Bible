// 文件: Examples/_ch137_flyweight.cpp
// Flyweight：共享内在状态，外部状态由调用方按次传入
#include <iostream>
#include <memory>
#include <unordered_map>

struct Glyph {                     // 内在状态 intrinsic
    explicit Glyph(char c) : ch_(c) {}
    void draw(int x, int y) const {     // x,y 为外部状态 extrinsic
        std::cout << ch_ << "@(" << x << ',' << y << ")\n";
    }
private:
    char ch_;
};

struct GlyphFactory {              // 享元工厂（带缓存）
    std::shared_ptr<Glyph> get(char c) {
        auto& p = pool_[c];
        if (!p) p = std::make_shared<Glyph>(c);
        return p;
    }
private:
    std::unordered_map<char, std::shared_ptr<Glyph>> pool_;
};

int main() {
    GlyphFactory f;
    auto a1 = f.get('a');
    auto a2 = f.get('a');          // 相同字符复用同一对象
    a1->draw(0, 0);
    a2->draw(5, 5);
}
