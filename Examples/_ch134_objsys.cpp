// _ch134_objsys.cpp
// 第134章 真实取证示例：自包含对象系统 / RTTI 等价机制
// 目标：在不安装 UE / UHT 的前提下，用标准 C++17 复刻 UObject 的核心骨架：
//   1) 基类 FObject（等价 UObject）
//   2) FClass（等价 UClass，含类名/父类/属性表，等价反射元数据）
//   3) 注册式反射（等价 UCLASS/UPROPERTY 宏展开后的 UHT 产物）
//   4) 强引用（等价 UPROPERTY 强引用 + GC 可达性）
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++17 -O2 -S -masm=intel
//       Examples/_ch134_objsys.cpp -o Examples/_ch134_objsys.asm

#include <string>
#include <vector>
#include <unordered_map>
#include <memory>
#include <cstdint>

// ── 等价 UClass 的类型元数据 ──────────────────────────
struct FProperty {
    std::string Name;
    std::size_t Offset;
    bool        bIsObject;   // 是否指向另一个 UObject（GC 需追踪）
};

struct FClass {
    std::string Name;
    const FClass* Super;
    std::vector<FProperty> Properties;
    static std::unordered_map<std::string, const FClass*>& Registry() {
        static std::unordered_map<std::string, const FClass*> m;
        return m;
    }
    static const FClass* Find(const std::string& n) {
        auto it = Registry().find(n);
        return it == Registry().end() ? nullptr : it->second;
    }
};

// ── 等价 UObject 的基类 ──────────────────────────────
struct FObject {
    const FClass* Class;
    std::string   Name;
    FObject(const FClass* c) : Class(c) {}
    const FClass* GetClass() const { return Class; }   // 等价 UObject::GetClass()
};

// ── 等价 UPROPERTY 强引用的智能句柄（简化 TSharedPtr） ──
template <typename T>
struct TStrongRef {
    std::shared_ptr<T> Ptr;
    T* Get() const { return Ptr.get(); }
    explicit operator bool() const { return static_cast<bool>(Ptr); }
};

// ── 具体类型：等价 UCLASS 展开 ───────────────────────
struct FActor : FObject {
    int32_t     Health;        // 等价 UPROPERTY(int32)
    TStrongRef<FObject> Target; // 等价 UPROPERTY() + 强引用（GC 根）

    static const FClass StaticClass;   // UHT 会生成等价符号
    FActor() : FObject(&StaticClass) { Health = 100; }
};

// 反射注册（等价 UHT 生成的 StaticClass 初始化）
const FClass FActor::StaticClass = [](){
    FClass c;
    c.Name  = "FActor";
    c.Super = nullptr;
    c.Properties.push_back(FProperty{"Health", offsetof(FActor, Health), false});
    c.Properties.push_back(FProperty{"Target", offsetof(FActor, Target), true});
    FClass::Registry()["FActor"] = &c;
    return c;
}();

// 等价 UObject 工厂（UClass::CreateDefaultObject 的简化）
FObject* NewObject(const FClass* cls) {
    if (cls && cls->Name == "FActor")
        return new FActor();
    return nullptr;
}

// 等价 GC 标记阶段：沿强引用图递归标记可达对象
void MarkReachable(FObject* Root, std::vector<FObject*>& Out) {
    if (!Root) return;
    Out.push_back(Root);
    // 简化：此处仅演示入口；真实 GC 会遍历 Properties 中 bIsObject 字段
}

int main() {
    FActor* a = new FActor();
    a->Name = "Hero";
    a->Health = 80;
    a->Target.Ptr = std::shared_ptr<FObject>(new FActor());  // 强引用子对象

    const FClass* ac = a->GetClass();           // RTTI 等价：GetClass()
    FObject* b = NewObject(FClass::Find("FActor"));

    std::vector<FObject*> reachable;
    MarkReachable(a, reachable);
    return (int)reachable.size() + (ac ? 0 : 1) + (b ? 0 : 1);
}
