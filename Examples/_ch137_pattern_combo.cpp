// 文件: Examples/_ch137_pattern_combo.cpp
// 模式组合：Composite(文档树) + Decorator(样式) + Flyweight(字体) 协同
#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

struct Font {                                  // Flyweight（内在状态）
    explicit Font(std::string n) : name_(std::move(n)) {}
    std::string name_;
};

struct FontFactory {
    Font* get(const std::string& n) {
        auto it = pool_.find(n);
        if (it != pool_.end()) return it->second.get();
        auto p = std::make_unique<Font>(n);
        auto* raw = p.get();
        pool_[n] = std::move(p);
        return raw;
    }
private:
    std::unordered_map<std::string, std::unique_ptr<Font>> pool_;
};

struct Glyph {                                 // Component（Composite 节点）
    virtual ~Glyph() = default;
    virtual void draw() const = 0;
};

struct Char : Glyph {                          // Leaf，持有 Flyweight 字体
    Char(char c, Font* f) : ch_(c), font_(f) {}
    void draw() const override { std::cout << "'" << ch_ << "'(" << font_->name_ << ")\n"; }
private:
    char ch_; Font* font_;
};

struct Row : Glyph {                           // Composite
    void add(std::unique_ptr<Glyph> g) { kids_.push_back(std::move(g)); }
    void draw() const override { for (auto& k : kids_) k->draw(); }
private:
    std::vector<std::unique_ptr<Glyph>> kids_;
};

struct Bold : Glyph {                          // Decorator
    explicit Bold(std::unique_ptr<Glyph> g) : w_(std::move(g)) {}
    void draw() const override { std::cout << "<b>"; w_->draw(); std::cout << "</b>"; }
private:
    std::unique_ptr<Glyph> w_;
};

int main() {
    FontFactory ff;
    Row line;
    line.add(std::make_unique<Char>('H', ff.get("Arial")));
    line.add(std::make_unique<Bold>(std::make_unique<Char>('i', ff.get("Arial"))));
    line.draw();
}
