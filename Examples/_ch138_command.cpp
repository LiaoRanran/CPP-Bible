// _ch138_command.cpp
// 第138章 ⑥：命令模式——封装操作为对象以支持 undo/redo
#include <iostream>
#include <memory>
#include <vector>

struct Editor {
    int value = 0;
    void add(int d) { value += d; }
    void sub(int d) { value -= d; }
};

struct Command {
    virtual ~Command() = default;
    virtual void do_(Editor& e) = 0;
    virtual void undo(Editor& e) = 0;
};

struct AddCmd : Command {
    int d;
    explicit AddCmd(int d) : d(d) {}
    void do_(Editor& e) override { e.add(d); }
    void undo(Editor& e) override { e.sub(d); }
};

int main() {
    Editor ed;
    std::vector<std::unique_ptr<Command>> hist;
    hist.push_back(std::make_unique<AddCmd>(5));
    hist.back()->do_(ed);
    std::cout << ed.value << '\n';
    hist.back()->undo(ed);
    std::cout << ed.value << '\n';
    return 0;
}
