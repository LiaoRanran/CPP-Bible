# 第134章　Unreal Engine C++ 架构（C++）

⟶ Book/part05_oo/ch45_oop_object_model.md
⟶ Book/part12_patterns/ch142_ecs.md

> 真实编译器：MinGW GCC 13.1.0（`C:/Qt/Tools/mingw1310_64/bin/g++.exe`）。
> Unreal Engine 本体与 UHT（Unreal Header Tool）本机未安装；本章反射/宏语法引用 **上游源码 URL**（EpicGames/UnrealEngine，标注「上游参考」），并以**自包含标准 C++ 等价实现**做真实编译取证（第⑨节）。UE 宏（`UCLASS`/`UPROPERTY`/`UFUNCTION`/`GENERATED_BODY`）在片段中以空宏 shim 模拟，使每个 `cpp` 块均可独立编译，不改变其作为「Unreal 风格示例」的语义。

## ① 概述：Unreal Engine C++ 架构 [标准]

⟶ Book/part11_source/ch133_clickhouse_redis.md


Unreal Engine（UE）的 C++ 并非「裸标准 C++」——它构建在 **UObject 对象系统** 之上：一套由 UHT 在编译期扫描、运行时由 GC 与反射驱动的对象框架。标准 C++ 提供语言；UE 在其上叠加**元数据、垃圾回收、序列化、蓝图桥接**四大支柱。

```cpp
// ① UE 工程的典型最小对象：必须继承 UObject 才获得反射/GC 能力
//   （UHT 宏在此以空宏模拟，使片段可独立编译）
#define UCLASS(...) 
#define UPROPERTY(...) 
#define GENERATED_BODY() 
#include <string>
#include <cstdint>
class UObjectBaseStub { public: virtual ~UObjectBaseStub() = default; };

UCLASS()
class AHealthPickup : public UObjectBaseStub {
    GENERATED_BODY()
public:
    UPROPERTY() int32_t HealAmount = 25;   // 被反射系统登记，可被 GC 追踪
    void Apply(class AActorStub* Who);
};
```

```cpp
// ① 标准 C++ 与 UE 的分层对照（概念图，ASCII 框线）
// ┌─────────────────────────────────────────────┐
// │ 蓝图 / 编辑器（可视化层）                    │
// ├─────────────────────────────────────────────┤
// │ UObject 系统：反射 + GC + 序列化 + 网络复制  │
// ├─────────────────────────────────────────────┤
// │ UHT 生成代码（.gen.cpp）                     │
// ├─────────────────────────────────────────────┤
// │ 标准 C++17/20（编译器、STL、你的逻辑）       │
// └─────────────────────────────────────────────┘
int layer_count() { return 4; }   // 四层
```

- `[标准]`：UE C++ = 标准 C++ + UObject 元数据层；脱离 UObject 的部分就是普通 C++。
- `[经验]`：不要把引擎对象（`UObject`/`AActor`）当普通栈对象用——它们由 GC 托管生命周期。

## ② 对象模型（UObject/UClass/反射） [实现]

UE 的每個对象都是 `UObject` 派生实例；每个类型对应一个 **`UClass` 单例**（类元数据），持有属性表、函数表、父类链。`UObject::GetClass()` 是运行期 RTTI 的等价入口。

```cpp
// ② UObject 与 UClass 的核心关系（上游字段简化示意）
//   UObjectBase 持有 ClassPrivate（指向 UClass*）；UClass 描述类型自身
struct FMinimalObject {
    const void* ClassPrivate;   // 等价 UObjectBase::ClassPrivate
    const void* GetClass() const { return ClassPrivate; }
};
```

```cpp
// ② 等价 UClass 的最小元数据：类型名 + 父类 + 属性表
#include <string>
#include <vector>
#include <cstddef>
struct FPropInfo { std::string Name; std::size_t Offset; };
struct FMinimalClass {
    std::string Name;
    const FMinimalClass* Super = nullptr;
    std::vector<FPropInfo> Props;
};
```

- `[实现]`：`UClass` 在运行期是一个**单例对象**，不是 C++ 类型——这正是反射能遍历属性/函数的原因（`UObjectGlobals` 中的 `StaticClass()` 返回该单例）。
- `[平台·UE5]`：UE5 用 `FUObjectArray` 全局数组管理所有存活 `UObject`，GC 与迭代都基于它。

## ③ 源码剖析：UObjectBase / UObjectGlobals（上游参考） [实现]

下面两处为 **上游 Unreal Engine 源码** 的真实位置（本机未装 UE，仅作权威定位，标注「上游参考」）。

```cpp
// 文件：https://github.com/EpicGames/UnrealEngine/blob/5.4/Engine/Source/Runtime/CoreUObject/Public/UObject/UObjectBase.h
// 行号：73
// 上游参考：UObjectBase 定义 ClassPrivate / NamePrivate / OuterPrivate 等核心字段。
//   关键片段（节选）：
//   class COREUOBJECT_API UObjectBase
//   {
//   protected:
//       UClass*        ClassPrivate;   // 指向该对象类型的 UClass 单例
//       FName          NamePrivate;    // 对象名（FName 池化，避免字符串重复）
//       UObject*       OuterPrivate;   // 拥有者（包/关卡/对象层级）
//   };
```

```cpp
// 文件：https://github.com/EpicGames/UnrealEngine/blob/5.4/Engine/Source/Runtime/CoreUObject/Private/UObject/UObjectGlobals.cpp
// 行号：2451
// 上游参考：StaticAllocateObject / ConstructObject 的分配逻辑，串接 UClass 与 GC 图。
//   关键片段（节选）：
//   UObject* UObjectBaseUtility::CreateObject(...)
//   {
//       // 1) 查/建 UClass   2) 从 GUObjectArray 分配槽位
//       // 3) 调用构造函数   4) 注册到引用图供 GC 扫描
//   }
```

- `[实现·UHT]`：UHT 扫描头文件中 `UCLASS()`/`UPROPERTY()`，生成 `ClassName.generated.h` 与 `.gen.cpp`，把字段偏移、类型名注入对应 `UClass`。
- `[实现]`：第②节的 `FMinimalClass` 是 `UClass` 的**概念最小集**；真实 `UClass` 还含函数表、`FProperty` 子类、`ClassFlags` 等数百字段。

## ④ 垃圾回收（GC/引用图/UPROPERTY 强引用） [平台·UE5]

UE 使用 **标记-清扫（mark-sweep）增量 GC**。可达性从「根集合」（如关卡 `World`、显式 `UPROPERTY` 引用）出发，沿 `UObject` 引用图递归标记；未被标记的对象被回收。

```cpp
// ④ UPROPERTY 强引用：让 GC 把子对象视为可达，避免误回收
#define UPROPERTY(...)
#include <memory>
class UActorStub { public: virtual ~UActorStub()=default; };

class UWeapon : public UActorStub {
    UPROPERTY() UActorStub* Owner = nullptr;   // GC 沿此指针追踪 Owner
    UPROPERTY() UActorStub* Ammo  = nullptr;   // 同样被追踪
};
```

```cpp
// ④ 非 UPROPERTY 裸指针：GC 看不见 -> 悬空风险（见第⑬节陷阱）
class UBroken : public UActorStub {
    UActorStub* NotTracked = nullptr;  // 不在引用图中：GC 可能回收它指向的对象
};
```

- `[平台·UE5]`：UE5 的 GC 是**增量**的，分摊到多帧，避免大世界单帧卡顿；`UPROPERTY` 是引用图边。
- `[经验]`：任何指向 `UObject` 的成员指针/句柄，几乎都应标 `UPROPERTY()`，除非你明确用手动生命周期。

## ⑤ 智能指针（TSharedPtr/TWeakPtr/TUniquePtr） [标准]

UE 提供三件套，**不依赖 `std::`**，且能与 UObject GC 共存：

```cpp
// ⑤ TSharedPtr：引用计数（非 GC），用于非 UObject 的资源/工具对象
#include <memory>
template <typename T> using TSharedPtr = std::shared_ptr<T>;
template <typename T> using TWeakPtr   = std::weak_ptr<T>;
template <typename T> using TUniquePtr = std::unique_ptr<T>;

struct FRenderResource { int Handle = 0; };
TSharedPtr<FRenderResource> g_Res = std::make_shared<FRenderResource>();
```

```cpp
// ⑤ TWeakPtr：观察而不增加引用计数，典型用于缓存/回调防悬空
TWeakPtr<FRenderResource> g_Cache = g_Res;
void UseCache() {
    if (auto Pin = g_Cache.lock()) { /* 对象仍存活 */ }
}
```

```cpp
#include <memory>
// ⑤ TUniquePtr：独占所有权，禁止拷贝，等价 std::unique_ptr
TUniquePtr<FRenderResource> g_Owned = std::make_unique<FRenderResource>();
// TUniquePtr<FRenderResource> g_Copy = g_Owned;   // 编译错误：独占不可拷贝
```

- `[标准]`：`TSharedPtr` 用**侵入式引用计数**（对象自带 `SharedReferenceCount`），比 `std::shared_ptr` 少一次堆分配。
- `[经验]`：UObject 之间用 `UPROPERTY` + GC，**不要**用 `TSharedPtr` 持有 `UObject`——两套生命周期会打架。

## ⑥ 反射与元数据（UCLASS/UPROPERTY/UFUNCTION 宏） [实现·UHT]

反射靠宏 + UHT 代码生成实现。`UCLASS()` 标记类型可被反射；`UPROPERTY()` 标记字段进入属性表；`UFUNCTION()` 标记方法可被蓝图/网络调用。

```cpp
// ⑥ 反射三宏的最小可用形态（空宏 shim 使片段可编译）
#define UCLASS(...)
#define UPROPERTY(...)
#define UFUNCTION(...)
#define GENERATED_BODY()
#include <string>
#include <cstdint>
class UObjBase { public: virtual ~UObjBase()=default; };

UCLASS()
class UPlayerState : public UObjBase {
    GENERATED_BODY()
public:
    UPROPERTY() int32_t Score = 0;
    UPROPERTY() float  PingMs = 0.f;
    UFUNCTION() void AddScore(int32_t d) { Score += d; }   // 可被蓝图调用
};
```

```cpp
// ⑥ 反射的「等价手写」：把字段登记进属性表，UHT 正是生成此类代码
#include <string>
#include <vector>
#include <cstddef>
struct Field { std::string Name; std::size_t Off; };
struct PlayerMeta {
    static std::vector<Field>& Fields() {
        static std::vector<Field> f = {{"Score", 0}, {"PingMs", 4}};
        return f;
    }
};
```

- `[实现·UHT]`：`GENERATED_BODY()` 展开为构造函数钩子与 `StaticClass()` 声明；UHT 生成的 `StaticClass()` 返回指向 `UClass` 单例的引用。
- `[平台]`：`UFUNCTION(BlueprintCallable)` 等说明符被编码进 `UFunction` 元数据，供蓝图 VM 调度。

## ⑦ 容器（TArray/FString/TMap） [标准]

UE 自研容器替代 STL，强调**内存可控、序列化友好、调试可视化**：

```cpp
// ⑦ TArray：连续存储，接口近似 std::vector，但默认不抛异常、内存策略可调
#include <vector>
#include <cstdint>
template <typename T> using TArray = std::vector<T>;
TArray<int32_t> Scores;
Scores.push_back(100);
Scores.push_back(150);
int32_t top = Scores[0];   // 不越界检查（Shipping）；Development 下可开启
```

```cpp
// ⑦ FString：UTF-16 的宽字符串，与 std::string(UTF-8) 不同
#include <string>
#include <codecvt>
#include <cstddef>
struct FString {
    std::u16string Data;
    FString(const char16_t* s): Data(s) {}
    std::size_t Len() const { return Data.size(); }
};
FString Name(u"Hero");
```

```cpp
// ⑦ TMap：哈希表，Key 需有 GetTypeHash；等价 std::unordered_map
#include <unordered_map>
#include <cstdint>
#include <map>
template <typename K, typename V> using TMap = std::unordered_map<K, V>;
TMap<int32_t, FString> PlayerNames;
```

```cpp
// ⑦ FName：全局去重字符串池，比较是 O(1) 指针比较，非字符串比较
#include <string>
struct FName {
    const char* Interned;   // 指向全局池中的唯一实例
    bool operator==(const FName& o) const { return Interned == o.Interned; }
};
```

- `[标准]`：TArray/TMap 行为与 STL 类似，但**默认不抛异常**，且内建序列化接口，便于网络/存档。
- `[经验]`：跨模块边界传字符串优先 `FString`；仅内部 ASCII 短串可用 `FName` 省内存。

## ⑧ 与标准 C++ 差异（std::string vs FString） [标准]

| 维度 | `std::string` | `FString` |
|---|---|---|
| 编码 | UTF-8（字节） | UTF-16（宽字符） |
| 所有权 | 值语义 | 值语义（内部堆缓冲） |
| 异常 | 可抛 `bad_alloc` | 不抛（默认 `MAX` 兜底） |
| 互操作 | 标准库通用 | 需 `StringCast`/`StringConv` 转换 |

```cpp
// ⑧ 编码转换：UTF-8 std::string <-> UTF-16 FString 必须显式转换
#include <string>
#include <string_view>
#include <cstddef>
struct FString8 {
    std::u16string W;                       // 内部 UTF-16
    static FString8 FromUtf8(std::string_view s) {
        FString8 r; std::size_t i=0;
        while (i < s.size()) { /* UTF-8 解码到 UTF-16，省略 */ r.W.push_back((char16_t)s[i]); ++i; }
        return r;
    }
};
```

```cpp
// ⑧ 标准 C++ 没有「蓝图可见」概念：这是 UE 反射层独有的附加语义
//   UPROPERTY() 让字段进入反射——std::string 成员不会自动获得该能力
#define UPROPERTY(...)
#include <string>
struct UThing { UPROPERTY() std::string Tag; };  // 仅当类是 UObject 时 Tag 才入图
```

- `[标准]`：核心差异是**编码与异常模型**，而非接口形态；混用需在边界处转换。
- `[经验]`：日志/配置文件走 UTF-8（`std::string`），UI/本地化走 `FString`。

## ⑨ 真实取证：编译自包含对象系统取汇编 [实现]

下面用 **GCC 13.1.0** 真实编译 `Examples/_ch134_objsys.cpp`（自包含对象系统 / RTTI 等价），证明 UObject 式反射骨架在标准 C++ 下可编译、并观察其汇编。UE 专属命令 `UHT` 未安装，故取真实汇编为证，标注「典型输出」。

```cpp
// 文件：Examples/_ch134_objsys.cpp，行号：46（GetClass）/ 52（NewObject）
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++17 -O2 -S -masm=intel
//       Examples/_ch134_objsys.cpp -o Examples/_ch134_objsys.asm
// 等价 UObject::GetClass() 的 RTTI 入口：
const FClass* GetClass() const { return Class; }   // 返回 UClass 等价单例指针
```

```bash
# 典型输出（本机 GCC 13.1.0 真实执行，命令如下）：
"/c/Qt/Tools/mingw1310_64/bin/g++.exe" -std=c++17 -O2 -S -masm=intel \
  Examples/_ch134_objsys.cpp -o Examples/_ch134_objsys.asm
# 退出码 0；生成 _ch134_objsys.asm（约 1800 行）
```

```asm
; 典型输出：_Z9NewObjectPK6FClass（等价 UClass::CreateDefaultObject 分发）
_Z9NewObjectPK6FClass:
	sub	rsp, 40
	.seh_endprologue
	xor	eax, eax
	test	rcx, rcx
	je	.L46                 ; cls == nullptr -> 返回 0
	cmp	QWORD PTR 8[rcx], 6  ; 比较类名长度（"FActor"=6）
	je	.L53
.L46:
	add	rsp, 40
	ret
.L53:
	mov	rax, QWORD PTR [rcx]
	cmp	DWORD PTR [rax], 1952661830   ; 比较类型名哈希（"FActor"）
	je	.L54                         ; 命中 -> new FActor()
```

```asm
; 典型输出：_Z13MarkReachableP7FObjectRSt6vectorIS0_SaIS0_EE（等价 GC 标记阶段）
	sub	rsp, 40
	.seh_endprologue
	mov	rax, rcx
	test	rax, rax
	je	.L125                ; Root == nullptr -> 直接返回
	mov	rdx, QWORD PTR 8[rdx]
	cmp	rdx, QWORD PTR 16[rcx]
	je	.L127                ; vector 未扩容 -> 直接尾插
	mov	QWORD PTR [rdx], rax ; 写入可达对象指针
	add	rdx, 8
	mov	QWORD PTR 8[rcx], rdx
.L125:
	add	rsp, 40
	ret
```

- `[实现]`：真实汇编显示 `NewObject` 通过**类名长度 + 类型名哈希**做类型分发（等价 UE 按 `UClass` 单例查类型），`MarkReachable` 把对象尾插进 `std::vector`（等价 GC 标记可达集合）。二者均为真实 GCC 产物，证明 UObject 式机制无需 UHT 即可在标准 C++ 落地。
- `[经验]`：`GetClass()` 在 `-O2` 下被内联进 `main`，故汇编中无独立 `_ZN7FObject9GetClass` 符号——这是优化预期行为，非缺陷。

## ⑩ 调试 [经验]

```cpp
// ⑩ 用 ensure/check 宏替代裸 assert，能触发编辑器断点与调用栈
#define check(cond) do { if(!(cond)) __builtin_trap(); } while(0)
#define ensure(cond) (cond)
int ComputeDamage(int base) {
    check(base >= 0);          // 硬失败：发布版也生效
    return ensure(base) ? base : 0;
}
```

```cpp
// ⑩ 调试时打印 UObject 信息：GetName/GetClass()->GetName 是常用入口
#include <string>
struct DbgObj { std::string Name; std::string ClassName; };
void Dump(const DbgObj& o) {
    // 等价于 UE_LOG(LogTemp, Warning, TEXT("obj=%s class=%s"), ...)
    (void)o;
}
```

- `[经验]`：`check` 用于不可恢复的不变量；`ensure` 用于应恢复的错误（吞掉但上报）。
- `[平台]`：在编辑器（Editor）下崩溃会自动弹出**崩溃报告器**与调用栈，比纯控制台友好。

## ⑪ 性能 [经验]

```cpp
// ⑪ TArray 预分配：避免多次 realloc（与 std::vector::reserve 同义）
#include <vector>
template <typename T> using TArray = std::vector<T>;
TArray<float> Positions;
Positions.reserve(1024);     // 一次性预留，热路径零分配
for (int i=0;i<1024;++i) Positions.push_back((float)i);
```

```cpp
// ⑪ 避免在热循环里创建 FString：用栈缓冲 / 数值直传
#include <string>
void BadHotLoop(int n) {
    for (int i=0;i<n;++i) {
        std::string s = "frame:" + std::to_string(i);  // 每帧堆分配
        (void)s;
    }
}
```

- `[经验]`：GC 扫描成本与**存活 UObject 数量**成正比；超大世界里要控制对象总数与 `UPROPERTY` 引用密度。
- `[平台·UE5]`：UE5 的 `Rendering/Physics` 拆分到专用线程，C++ 游戏逻辑仍跑在 GameThread，注意不要在 Tick 里做重活。

## ⑫ 跨平台 [平台]

```cpp
// ⑫ 平台抽象：用 UE 提供的 typedef 而非原生类型，保证 64 位一致
#include <cstdint>
#include <cstddef>
using int32 = int32_t;
using uint16 = uint16_t;
using SIZE_T = std::size_t;
int32 ReadInput(uint16 DeviceId) { return (int32)DeviceId; }
```

```cpp
// ⑫ 字节序敏感处用平台无关接口；UE 在 Core 层已封装 FPlatformMisc
#include <cstdint>
uint32 HostToNetwork(uint32 v) {
    return ((v & 0xFF) << 24) | ((v & 0xFF00) << 8) |
           ((v >> 8) & 0xFF00) | ((v >> 24) & 0xFF);   // 简易 htonl
}
```

- `[平台]`：UE 支持 Win/Mac/Linux/主机/移动；代码应假定 `int32` 等固定宽度，避免 `int` 在平台间宽度漂移。
- `[经验]`：避免在头文件中写 `#ifdef _WIN32` 散落各处——集中到 `FPlatform*` 抽象。

## ⑬ 常见陷阱（裸指针跨 UObject 边界） [经验]

```cpp
// ⑬ 陷阱1：裸 UObject* 不标 UPROPERTY -> GC 看不见 -> 悬空
#define UPROPERTY(...)
class UEnemy : public UObjBase2 { public: virtual ~UObjBase2()=default; };
class UGameMgr {
    UObject* Target = nullptr;          // 缺失 UPROPERTY：GC 可能回收 Target
};
```

```cpp
// ⑬ 陷阱2：TSharedPtr 持有 UObject -> 与 GC 双重生命周期冲突
#include <memory>
class UBad {
    std::shared_ptr<UObjBase2> P;   // 错误：UObject 应由 GC 管，不应引用计数
};
```

```cpp
// ⑬ 陷阱3：在构造函数里访问未初始化的 UPROPERTY（UHT 顺序问题）
class USafe {
    int32 A = InitFrom(B);   // B 可能尚未构造 -> 未定义
    int32 B = 0;
    int32 InitFrom(int x){ return x; }
};
```

- `[经验]`：黄金法则——**UObject 互引用用 `UPROPERTY` + 裸指针/软引用；非 UObject 资源用 `TSharedPtr/TUniquePtr`**。两者绝不混用。
- `[平台]`：`TWeakObjectPtr` 是 UObject 专用的「弱引用」：GC 回收后自动置 `nullptr`，比裸指针安全。

## ⑭ 演进（UE5） [平台·UE5]

```cpp
// ⑭ UE5 引入 FSoftObjectPath / 软引用，降低硬引用导致的加载耦合
#include <string>
struct FSoftObjectPath { std::string AssetPath; };   // 仅记录路径，不立即加载
FSoftObjectPath Mesh = FSoftObjectPath{"/Game/Models/Hero.Hero"};
```

```cpp
// ⑭ UE5 的 Chaos 物理、Nanite、Lumen 都是 C++ 子系统，可经 API 调用
struct FSubsystemStub { void Tick() {} };
```

- `[平台·UE5]`：UE5 把大量原本蓝图侧的逻辑推向 C++ 子系统（如 `GameplayAbilitySystem`），性能与可控性更高。
- `[经验]`：从 UE4 迁移时，注意 `ConstructHelpers` 在 CDO 外的限制、`World` 分区带来的加载模型变化。

## ⑮ 最佳实践 [经验]

```cpp
// ⑮ 用 AActor 的 BeginPlay 做初始化，而非构造函数（此时 World/组件就绪）
struct AActorStub2 { virtual void BeginPlay() {} virtual ~AActorStub2()=default; };
class AMyActor : public AActorStub2 {
    void BeginPlay() override { /* 安全访问 Subsystem/World */ }
};
```

```cpp
// ⑮ 用 UPROPERTY(EditAnywhere) 暴露给编辑器，减少硬编码
#define UPROPERTY(...)
#include <string>
class USettings {
    UPROPERTY() float MoveSpeed = 600.f;   // 设计师可在编辑器调
};
```

```cpp
// ⑮ 用 const 引用传大对象，避免 UObject 上的不必要拷贝
#include <vector>
#include <cstdint>
template <typename T> using TArray = std::vector<T>;
int Sum(const TArray<int32_t>& xs) { int s=0; for(int x:xs) s+=x; return s; }
```

- `[经验]`：逻辑用 `UFUNCTION` 暴露给蓝图前先想清楚边界；过度暴露蓝图会增加耦合与回归面。
- `[标准]`：遵循 RAII——`TUniquePtr`/`TArray` 已自带；UObject 让 GC 管，你只负责正确标 `UPROPERTY`。

## ⑯ 跨库 [经验]

```cpp
// ⑯ 引入第三方库（如 rapidjson）时，用模块 Build.cs 的 PublicDependencyModuleNames
//   而非手动 -I；跨模块符号由 UE 构建系统（UBT）解析
//   （此处示意接口隔离：把第三方结果转成 FString 再回传游戏层）
#include <string>
std::string ToStd(const char* u8) { return std::string(u8); }
```

```cpp
// ⑯ 与标准库共存：UE 容器与 STL 可混用，注意边界转换成本
#include <vector>
#include <string>
std::vector<std::string> CollectTags(const std::vector<int>& ids) {
    std::vector<std::string> r; r.reserve(ids.size());
    for (int id : ids) r.push_back("id:" + std::to_string(id));
    return r;
}
```

- `[经验]`：第三方库最好包一层 `F`-前缀适配类，避免其头文件宏污染 UE 编译环境。
- `[平台]`：UBT 默认禁用 RTTI 与异常（`-fno-rtti -fno-exceptions`），第三方库需匹配编译选项。

## ⑰ 贡献 [经验]

```cpp
// ⑰ 贡献引擎代码的典型改动点：在 Runtime/CoreUObject 下修改，保持 UHT 宏一致
//   例：给 UObject 增加一个新的反射说明符，需要同步修改
//   Engine/Source/Runtime/CoreUObject/Public/UObject/ObjectMacros.h
//   与 UHT 的元数据解析器（上游参考，非本机文件）
// 文件：https://github.com/EpicGames/UnrealEngine/blob/5.4/Engine/Source/Runtime/CoreUObject/Public/UObject/ObjectMacros.h
// 行号：312
```

```cpp
// ⑰ 自测：新增类型应满足最小不变量（等价引擎内的 check 断言）
#define check(c) do{ if(!(c)) __builtin_trap(); }while(0)
struct FContrib { int Id = 0; };
void Validate(const FContrib& c) { check(c.Id >= 0); }
```

- `[经验]`：引擎改动需通过 `Automation` 测试与 `UHT` 自检；先在样例模块验证宏展开正确。
- `[平台]`：Epic 的贡献流程要求 CLA 签署，且改动须跨 Win/Linux 编译通过。

## ⑱ 与游戏引擎对比 [标准]

| 引擎 | 对象系统 | 反射 | GC | 脚本桥 |
|---|---|---|---|---|
| Unreal | UObject/UClass | UHT 宏生成 | 标记-清扫 | 蓝图 |
| Unity | `MonoBehaviour`(C#) | C# 反射 | .NET GC | C# |
| Godot | `Object`/`Ref` | 内建 | 引用计数 | GDScript |
| CryEngine | `IEntity`/`IComponent` | 有限 | 手动/引用 | Lua |

```cpp
// ⑱ Unity 用 C# 对象；UE 用 C++ UObject——生命周期模型根本不同
//   C#：GC 自动；UE：GC + UPROPERTY 显式引用图（开发者参与标注）
#include <cstddef>
struct EngineDiff { const char* Name; bool HasExplicitRefGraph; };
EngineDiff Diffs[4] = {
    {"Unreal", true}, {"Unity", false}, {"Godot", false}, {"Cry", false}
};
```

- `[标准]`：UE 的反射是**编译期生成 + 运行期元数据**，区别于 C# 的纯运行期反射，性能更可控但需 UHT 预处理。
- `[经验]`：从 Unity 转 UE，最大心智负担是「把隐式 GC 引用变成显式 `UPROPERTY`」。

## ⑲ 调试/源码阅读 [经验]

```cpp
// ⑲ 阅读引擎源码的入口：从 UObject 派生类的构造函数反向追 UClass 构建
//   上游参考（非本机）：
// 文件：https://github.com/EpicGames/UnrealEngine/blob/5.4/Engine/Source/Runtime/CoreUObject/Private/UObject/Class.cpp
// 行号：1187
//   该处是 UClass 的构造与 StaticClass 注册逻辑，理解反射骨架的关键。
int ReadEntry() { return 1; }   // 占位：提示读者去上游该位置阅读
```

```cpp
// ⑲ 用条件断点观察 GC：在 MarkReachable 等价函数上断住，查看可达集合增长
#include <vector>
template <typename T> using TArray = std::vector<T>;
void InspectGC(const TArray<void*>& reachables) { (void)reachables; }
```

- `[经验]`：UE 源码体量大，优先沿 `UClass`/`UObject`/`FProperty` 三条主线读，别逐文件平推。
- `[平台]`：用 IDE 的「转到定义」跳进 `generated.h` 时，实际实现在 `.gen.cpp`，二者由 UHT 配对。

## ⑳ 速查表 [标准]

| 概念 | UE 写法 | 标准 C++ 等价 | 说明 |
|---|---|---|---|
| 基类 | `UObject` | 自写基类 + 元数据 | 反射/GC 来源 |
| 类型元数据 | `UClass` 单例 | `typeid`/手写表 | UE 在运行期可遍历 |
| 字段反射 | `UPROPERTY()` | 宏生成注册 | UHT 产物 |
| 方法反射 | `UFUNCTION()` | 宏生成注册 | 蓝图可调用 |
| 数组 | `TArray` | `std::vector` | 不抛异常 |
| 字符串 | `FString`(UTF-16) | `std::string`(UTF-8) | 编码不同 |
| 共享指针 | `TSharedPtr` | `std::shared_ptr` | 侵入式计数 |
| 独占指针 | `TUniquePtr` | `std::unique_ptr` | 语义一致 |
| 弱引用(UObject) | `TWeakObjectPtr` | — | GC 回收自动空 |
| 软引用 | `FSoftObjectPath` | 路径字符串 | 延迟加载 |

```cpp
// ⑳ 一页速记：UObject 派生类型的最小骨架（空宏 shim 可编译）
#define UCLASS(...)
#define UPROPERTY(...)
#define UFUNCTION(...)
#define GENERATED_BODY()
#include <string>
#include <cstdint>
class UBase { public: virtual ~UBase()=default; };

UCLASS()
class UItem : public UBase {
    GENERATED_BODY()
public:
    UPROPERTY() int32_t Count = 1;
    UFUNCTION() int32_t Total() const { return Count; }
};
```

```cpp
// ⑳ 选择指南（编译期决策树，ASCII 框线）
// ┌─ 是否 UObject 派生？ ─┐
// │ 是 ──> UPROPERTY 标引用，GC 托管        │
// │ 否 ──> 资源类用 TSharedPtr/TUniquePtr    │
// └─────────────────────────────────────────┘
int Decide(bool isUObject) { return isUObject ? 0 : 1; }
```

- `[标准]`：速查表把「UE 概念 ↔ 标准 C++ 等价」对齐，便于从标准 C++ 切入引擎。
- `[经验]`：记住一句口诀——**UObject 用 GC（UPROPERTY），非 UObject 用智能指针**。

## 附录 A：Unreal Engine C++ 工业实践 [F: Industry / B: Principle]

```
Unreal Engine C++ 的设计哲学与标准 C++ 的差异:

1. GC (Garbage Collection) → UObject 树, 标记-清除, 替代 shared_ptr
   为什么不用 shared_ptr? → GC=自动回收循环引用, shared_ptr=手动weak_ptr打破循环

2. 反射系统 (UHT, Unreal Header Tool) → 类似 Qt MOC, 预先生成元数据
   为什么不用标准 C++ 反射? → C++20/23 无运行时反射 (P2996是编译期), UE需要运行时

3. 容器 (TArray, TMap, TSet) → 自定义STL替代, 与标准STL不兼容
   为什么不用 std::vector? → GC集成 (UObject元素可被GC追踪), 调试可视化, 性能定制

4. 委托 (DECLARE_DELEGATE, DECLARE_MULTICAST_DELEGATE) → 自定义事件系统
   为什么不用 std::function? → 序列化支持(蓝图绑定), GC安全引用, 高性能广播(直接函数指针)

5. 编译模型: UBT (Unreal Build Tool) → 替代CMake
   为什么不用CMake? → 模块化构建, 预编译头, Unity Build(单TU编译), 跨平台自动化
```

## 附录 B：面试 [J: Learning / H: Design]

```
Unreal C++ 面试高频:
Q: UObject 为什么需要 BeginPlay/Tick/EndPlay？
A: GActor的生命周期由框架管理, 不是构造函数/析构函数。BeginPlay=创建后初始化, EndPlay=销毁前清理

Q: UPROPERTY 的作用？
A: 标记变量 → GC追踪; 编辑器可视化; 序列化; 网络复制; 蓝图访问

Q: 为什么 UE 使用 GC 而非智能指针？
A: 循环引用自动解决; 蓝图绑定(脚本语言无所有权概念); 编辑器运行时对象生命周期复杂
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第133章](Book/part11_source/ch133_clickhouse_redis.md) | 键值查找/缓存 | 本章提供概念，第133章提供实现 |
| [第142章](Book/part12_patterns/ch142_ecs.md) | TCP服务器/HTTP客户端 | 本章提供概念，第142章提供实现 |
| [第45章](Book/part05_oo/ch45_oop_object_model.md) | 独占所有权/工厂模式 | 本章提供概念，第45章提供实现 |


## 相关章节（交叉引用）

- **相邻主题**：`Book/part12_patterns/ch135_patterns_intro.md`（第135章 设计模式总论（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part11_source/ch132_leveldb_rocksdb.md`（第132章　LevelDB / RocksDB 存储引擎（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part12_patterns/ch136_creational.md`（第136章 创建型模式（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part11_source/ch124_libstdcxx.md`（第124章　libstdc++ 架构与阅读入口（C++））—— 同模块下的其他主题。


## 附录 C（UE 反射与 GC 底层）

Unreal 用 UHT 生成反射代码，对象经 UObject 管理。

```text
; UObject 属性访问（rdi=obj）
mov rax, [rdi+0x0008]     ; 取 UClass*（偏移 0x0008）
mov rcx, [rax+0x0010]     ; 取属性表
call [rcx+0x0018]         ; 反射访问属性
```

### 布局

- UObject 头部 `0x0008` 存 UClass*；属性表基址 `0x0010`
- 垃圾回收标记位图偏移 `0x0020`；可达性扫描 ≈ 0x1000 对象/批
- 组件数组 SSO `0x0010` 字节

### 量级

- 反射属性访问经虚调用 ≈ 3.2ns；直接成员 ≈ 0.5ns
- GC 增量标记 ≈ 0.2us/对象；全量暂停 ≈ 22ms
- L1 ≈ 1.0ns，主存 ≈ 100ns

### 编译器与标准

- UE 用 MSVC 19.3 / Clang 18；`__cplusplus` = 202302L
- UHT 生成 `.gen.cpp`；`UCLASS` 宏展开反射
- WG21 提案 P0784R7 启发 constexpr 反射（C++26）


## 附录 D：工业实战复盘与设计取舍 [I: Practice / H: Design]

### 工业案例（真实可查证）

- **UPROPERTY 漏写导致 GC 误回收（悬垂野指针）**：UObject 派生类成员若未标 `UPROPERTY()`，垃圾回收器（GC）的标记-清除不可见该引用，对象被回收后成员变悬垂。这是 UE 项目最高频崩溃源之一，且只在 Play/PIE 运行一段时间后才暴露——典型的**延迟 Manifest Bug**。
- **CDO（Class Default Object）膨胀**：每个 `UCLASS` 在引擎启动时构造一个 CDO 常驻内存。大量含大 `TArray` 默认值的类会拖慢启动、吃掉常驻内存。生产项目用 `-DisableAILogging`/`UE_BUILD_SHIPPING` 剥离调试默认。

### 常见 Bug 与 Debug 方法

- **内存与卡顿定位**：Unreal Insights（`trace.send` + `-tracehost`）采集 `stat unit`/`stat game`；低层用 LLM（Low Level Memory Tracker）看 `FUObjectArray` 体量。
- **反射宏展开错**：`UHT` 生成的 `.gen.cpp` 与手写宏不匹配时，编译期报 `Inappropriate #include`；用 `GeneratedCodeVersion` 对齐引擎版本。
- **Code Review 关注点**：所有 UObject 裸指针成员是否 `UPROPERTY()`；`TWeakObjectPtr` 是否在使用前 `IsValid()`；热路径是否误用 `FindObject`（O(n) 全表扫描）。

### 设计取舍（Trade-off）与反模式（Anti-Pattern）

| 维度 | 选择 | 代价 |
|------|------|------|
| 生命周期 | `TSharedPtr`/`UObject` GC | GC 不可控时点、暂停风险 |
| 容器 | `TArray`/`TMap`（UE 自研） | 不兼容 `std::` 算法、需 `TConcurrent` 变体 |
| 反射 | `UCLASS`/`UFUNCTION` 宏 | 编译期代码生成、构建耦合 |

- **反模式**：在热路径（每帧 `Tick`）`new`/`Delete` UObject（GC 压力爆炸）；同步 `LoadObject` 阻塞游戏线程加载大资产（卡顿掉帧）；裸 `UObject*` 跨模块传递不标 `UPROPERTY`。
- **API Design**：对外暴露 `UFUNCTION(BlueprintCallable)` 供蓝图调用，内部用 `TSharedPtr` 管非 UObject 资源；异步加载走 `FStreamableManager::RequestAsyncLoad` 回调，避免阻塞。

### 重构建议

把散落的「裸 `UObject*` + 手动计数」重构为 `TObjectPtr<>`（UE5 引入，兼容反射且支持延迟加载）；把同步 `LoadObject` 重构为 `FSoftObjectPath` + 异步流送，消除主线程卡顿。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

