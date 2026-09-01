# Effective Modern C++ — 42 条条目化提取

> 源：`docs/references/external/books/effective-modern-cpp.txt`（pypdf 从 PDF 提取，本机 RAG 用，`.gitignore` 忽略）。
> 引用键：`book:effective-modern:itemN`。
> 用法：只取要点与代码片段，**不整本投喂**；「规则」为书中 Item 标题原文，「书中要点」为正文开篇摘录（非全文）。
> ⚠️ 要点是开篇摘录，不可替代原书论证；写入手册前请结合标准/真机验证。

## Item 1，p.9

- **规则**：Understand template type deduction.
- **引用键**：`book:effective-modern-cpp:item1`
- **书中要点**：When users of a complex system are ignorant of how it works, yet happy with what it does, that says a lot about the design of the system. By this measure, template type deduction in C++ is a tremendous success. Millions of programmers have passed arguments to template functions with completely satisfactory results, even though many of those programmers would be hard-pressed to give more than the haziest description of how the types used by those functions were deduced. If that group includes you, I have good news and bad news. …

## Item 2，p.18

- **规则**：Understand auto type deduction.
- **引用键**：`book:effective-modern-cpp:item2`
- **书中要点**：If you’ve read Item 1 on template type deduction, you already know almost every‐ thing you need to know about auto type deduction, because, with only one curious exception, auto type deduction is template type deduction. But how can that be? Template type deduction involves templates and functions and parameters, but auto deals with none of those things. That’s true, but it doesn’t matter. There’s a direct mapping between template type deduction and auto type deduction. There is literally an algorithmic transformation from one to the other. …

## Item 3，p.23

- **规则**：Understand decltype.
- **引用键**：`book:effective-modern-cpp:item3`
- **书中要点**：decltype is an odd creature. Given a name or an expression, decltype tells you the name’s or the expression’s type. Typically, what it tells you is exactly what you’d predict. Occasionally however, it provides results that leave you scratching your head and turning to reference works or online Q&A sites for revelation. We’ll begin with the typical cases—the ones harboring no surprises. …

## Item 4，p.30

- **规则**：Know how to view deduced types.
- **引用键**：`book:effective-modern-cpp:item4`
- **书中要点**：The choice of tools for viewing the results of type deduction is dependent on the phase of the software development process where you want the information. We’ll explore three possibilities: getting type deduction information as you edit your code, getting it during compilation, and getting it at runtime. IDE Editors Code editors in IDEs often show the types of program entities (e.g., variables, param‐ eters, functions, etc.) when you do something like hover your cursor over the entity. …

## Item 5，p.37

- **规则**：Prefer auto to explicit type declarations.
- **引用键**：`book:effective-modern-cpp:item5`
- **书中要点**：Ah, the simple joy of int x; Wait. Damn. I forgot to initialize x, so its value is indeterminate. Maybe. It might actually be initialized to zero. Depends on the context. Sigh. Never mind. Let’s move on to the simple joy of declaring a local variable to be initial‐ ized by dereferencing an iterator: template<typename It> // algorithm to dwim ("do what I mean") void dwim(It b, It e) // for all elements in range from { // b to e while (b != e) { typename std::iterator_traits<It>::value_type currValue = *b; … } } Ugh. …

## Item 6

- **规则**：Use the explicitly typed initializer idiom when auto deduces undesired types.
- **引用键**：`book:effective-modern-cpp:item6`
- **书中要点**：auto deduces undesired types. Item 5 explains that using auto to declare variables offers a number of technical advantages over explicitly specifying types, but sometimes auto’s type deduction zigs when you want it to zag. For example, suppose I have a function that takes a Widget and returns a std::vector<bool>, where each bool indicates whether the Widget offers a particular feature: std::vector<bool> features(const Widget& w); Further suppose that bit 5 indicates whether the Widget has high priority. We can thus write code like this: Widget w; … bool highPriority = features(w)[5]; // is w high priority? …

## Item 7，p.49

- **规则**：Distinguish between () and {} when creating objects.
- **引用键**：`book:effective-modern-cpp:item7`
- **书中要点**：objects. Depending on your perspective, syntax choices for object initialization in C++11 embody either an embarrassment of riches or a confusing mess. As a general rule, initialization values may be specified with parentheses, an equals sign, or braces: int x(0); // initializer is in parentheses int y = 0; // initializer follows "=" int z{ 0 }; // initializer is in braces In many cases, it’s also possible to use an equals sign and braces together: int z = { 0 }; // initializer uses "=" and braces For the remainder of this Item, I’ll generally ignore the equals-sign-plus-braces syn‐ tax, because C++ usually treat …

## Item 8，p.58

- **规则**：Prefer nullptr to 0 and NULL.
- **引用键**：`book:effective-modern-cpp:item8`
- **书中要点**：So here’s the deal: the literal 0 is an int, not a pointer. If C++ finds itself looking at 0 in a context where only a pointer can be used, it’ll grudgingly interpret 0 as a null pointer, but that’s a fallback position. C++’s primary policy is that 0 is an int, not a pointer. Practically speaking, the same is true of NULL. There is some uncertainty in the details in NULL’s case, because implementations are allowed to give NULL an integral type other than int (e.g., long). …

## Item 9，p.63

- **规则**：Prefer alias declarations to typedefs.
- **引用键**：`book:effective-modern-cpp:item9`
- **书中要点**：I’m confident we can agree that using STL containers is a good idea, and I hope that Item 18 convinces you that using std::unique_ptr is a good idea, but my guess is that neither of us is fond of writing types like “ std::unique_ptr<std::unor dered_map<std::string, std::string>>” more than once. Just thinking about it probably increases the risk of carpal tunnel syndrome. Avoiding such medical tragedies is easy. Introduce a typedef: typedef std::unique_ptr<std::unordered_map<std::string, std::string>> UPtrMapSS; But typedefs are soooo C++98. …

## Item 10，p.67

- **规则**：Prefer scoped enums to unscoped enums.
- **引用键**：`book:effective-modern-cpp:item10`
- **书中要点**：As a general rule, declaring a name inside curly braces limits the visibility of that name to the scope defined by the braces. Not so for the enumerators declared in C++98-style enums. The names of such enumerators belong to the scope containing the enum, and that means that nothing else in that scope may have the same name: enum Color { black, white, red }; // black, white, red are // in same scope as Color auto white = false; // error! …

## Item 11，p.74

- **规则**：Prefer deleted functions to private undefined ones.
- **引用键**：`book:effective-modern-cpp:item11`
- **书中要点**：ones. If you’re providing code to other developers, and you want to prevent them from calling a particular function, you generally just don’t declare the function. No func‐ tion declaration, no function to call. Easy, peasy. But sometimes C++ declares func‐ tions for you, and if you want to prevent clients from calling those functions, the peasy isn’t quite so easy any more. The situation arises only for the “special member functions,” i.e., the member func‐ tions that C++ automatically generates when they’re needed. …

## Item 12，p.79

- **规则**：Declare overriding functions override.
- **引用键**：`book:effective-modern-cpp:item12`
- **书中要点**：The world of object-oriented programming in C++ revolves around classes, inheri‐ tance, and virtual functions. Among the most fundamental ideas in this world is that virtual function implementations in derived classes override the implementations of their base class counterparts. It’s disheartening, then, to realize just how easily virtual function overriding can go wrong. It’s almost as if this part of the language were designed with the idea that Murphy’s Law wasn’t just to be obeyed, it was to be hon‐ ored. …

## Item 13，p.86

- **规则**：Prefer const_iterators to iterators.
- **引用键**：`book:effective-modern-cpp:item13`
- **书中要点**：const_iterators are the STL equivalent of pointers-to- const. They point to values that may not be modified. The standard practice of using const whenever possible dictates that you should use const_iterators any time you need an iterator, yet have no need to modify what the iterator points to. That’s as true for C++98 as for C++11, but in C++98, const_iterators had only halfhearted support. It wasn’t that easy to create them, and once you had one, the ways you could use it were limited. …

## Item 14，p.90

- **规则**：Declare functions noexcept if they won’t emit exceptions.
- **引用键**：`book:effective-modern-cpp:item14`
- **书中要点**：exceptions. In C++98, exception specifications were rather temperamental beasts. You had to summarize the exception types a function might emit, so if the function’s implemen‐ tation was modified, the exception specification might require revision, too. Chang‐ ing an exception specification could break client code, because callers might be dependent on the original exception specification. Compilers typically offered no help in maintaining consistency among function implementations, exception specifi‐ cations, and client code. …

## Item 15

- **规则**：Use constexpr whenever possible.                                                              97 vii === PAGE 10 ===
- **引用键**：`book:effective-modern-cpp:item15`
- **书中要点**：If there were an award for the most confusing new word in C++11, constexpr would probably win it. When applied to objects, it’s essentially a beefed-up form of const, but when applied to functions, it has a quite different meaning. Cutting through the confusion is worth the trouble, because when constexpr corresponds to what you want to express, you definitely want to use it. Conceptually, constexpr indicates a value that’s not only constant, it’s known dur‐ ing compilation. The concept is only part of the story, though, because when con stexpr is applied to functions, things are more nuanced than this suggests. …

## Item 16，p.103

- **规则**：Make const member functions thread safe.
- **引用键**：`book:effective-modern-cpp:item16`
- **书中要点**：If we’re working in a mathematical domain, we might find it convenient to have a class representing polynomials. Within this class, it would probably be useful to have a function to compute the root(s) of a polynomial, i.e., values where the polynomial evaluates to zero. Such a function would not modify the polynomial, so it’d be natural to declare it const: class Polynomial { public: using RootsType = // data structure holding values std::vector<double>; // where polynomial evals to zero … // (see Item 9 for info on "using") RootsType roots() const; … }; Computing the roots of a polynomial can be expensive, so w …

## Item 17，p.109

- **规则**：Understand special member function generation.
- **引用键**：`book:effective-modern-cpp:item17`
- **书中要点**：generation. In official C++ parlance, the special member functions are the ones that C++ is willing to generate on its own. C++98 has four such functions: the default constructor, the destructor, the copy constructor, and the copy assignment operator. There’s fine print, of course. These functions are generated only if they’re needed, i.e., if some code uses them without their being expressly declared in the class. A default con‐ structor is generated only if the class declares no constructors at all. …

## Item 18

- **规则**：Use std::unique_ptr for exclusive-ownership resource management.
- **引用键**：`book:effective-modern-cpp:item18`
- **书中要点**：resource management. When you reach for a smart pointer, std::unique_ptr should generally be the one closest at hand. It’s reasonable to assume that, by default, std::unique_ptrs are the same size as raw pointers, and for most operations (including dereferencing), they execute exactly the same instructions. This means you can use them even in situa‐ 118 | Item 17 class Investment { … }; class Stock: public Investment { … }; class Bond: public Investment { … }; class RealEstate: public Investment { … }; Investment Bond Stock RealEstate tions where memory and cycles are tight. …

## Item 19

- **规则**：Use std::shared_ptr for shared-ownership resource management.
- **引用键**：`book:effective-modern-cpp:item19`
- **书中要点**：resource management. Programmers using languages with garbage collection point and laugh at what C++ programmers go through to prevent resource leaks. “How primitive!” they jeer. “Didn’t you get the memo from Lisp in the 1960s? Machines should manage resource lifetimes, not humans.” C++ developers roll their eyes. “You mean the memo where the only resource is memory and the timing of resource reclamation is nondetermin‐ istic? We prefer the generality and predictability of destructors, thank you.” But our bravado is part bluster. …

## Item 20

- **规则**：Use std::weak_ptr for std::shared_ptr-like pointers that can dangle.
- **引用键**：`book:effective-modern-cpp:item20`
- **书中要点**：like pointers that can dangle. Paradoxically, it can be convenient to have a smart pointer that acts like a std::shared_ptr (see Item 19), but that doesn’t participate in the shared ownership of the pointed-to resource. In other words, a pointer like std::shared_ptr that doesn’t affect an object’s reference count. This kind of smart pointer has to contend with a problem unknown to std::shared_ptrs: the possibility that what it points to has been destroyed. A truly smart pointer would deal with this problem by tracking when it dangles, i.e., when the object it is supposed to point to no longer exists. …

## Item 21

- **规则**：Prefer std::make_unique and std::make_shared to direct use of new.
- **引用键**：`book:effective-modern-cpp:item21`
- **书中要点**：std::make_shared to direct use of new. Let’s begin by leveling the playing field for std::make_unique and std:: make_shared. std::make_shared is part of C++11, but, sadly, std::make_ unique isn’t. It joined the Standard Library as of C++14. If you’re using C++11, never fear, because a basic version of std::make_unique is easy to write yourself. Here, look: template<typename T, typename... Ts> std::unique_ptr<T> make_unique(Ts&&... …

## Item 22

- **规则**：When using the Pimpl Idiom, define special member functions in the implementation file.
- **引用键**：`book:effective-modern-cpp:item22`
- **书中要点**：member functions in the implementation file. If you’ve ever had to combat excessive build times, you’re familiar with the Pimpl (“pointer to implementation”) Idiom. That’s the technique whereby you replace the data members of a class with a pointer to an implementation class (or struct), put the data members that used to be in the primary class into the implementation class, and access those data members indirectly through the pointer. …

## Item 23，p.158

- **规则**：Understand std::move and std::forward.
- **引用键**：`book:effective-modern-cpp:item23`
- **书中要点**：It’s useful to approach std::move and std::forward in terms of what they don’t do. std::move doesn’t move anything. std::forward doesn’t forward anything. At run‐ time, neither does anything at all. They generate no executable code. Not a single byte. std::move and std::forward are merely functions (actually function templates) that perform casts. std::move unconditionally casts its argument to an rvalue, while std::forward performs this cast only if a particular condition is fulfilled. That’s it. The explanation leads to a new set of questions, but, fundamentally, that’s the com‐ plete story. …

## Item 24，p.164

- **规则**：Distinguish universal references from rvalue references.
- **引用键**：`book:effective-modern-cpp:item24`
- **书中要点**：references. It’s been said that the truth shall set you free, but under the right circumstances, a well-chosen lie can be equally liberating. This Item is such a lie. Because we’re dealing with software, however, let’s eschew the word “lie” and instead say that this Item comprises an “abstraction.” To declare an rvalue reference to some type T, you write T&&. It thus seems reason‐ able to assume that if you see “T&&” in source code, you’re looking at an rvalue refer‐ ence. …

## Item 25

- **规则**：Use std::move on rvalue references, std::forward on universal references.
- **引用键**：`book:effective-modern-cpp:item25`
- **书中要点**：std::forward on universal references. Rvalue references bind only to objects that are candidates for moving. If you have an rvalue reference parameter, you know that the object it’s bound to may be moved: class Widget { Widget(Widget&& rhs); // rhs definitely refers to an 168 | Item 24 … // object eligible for moving }; That being the case, you’ll want to pass such objects to other functions in a way that permits those functions to take advantage of the object’s rvalueness. The way to do that is to cast parameters bound to such objects to rvalues. …

## Item 26，p.177

- **规则**：Avoid overloading on universal references.
- **引用键**：`book:effective-modern-cpp:item26`
- **书中要点**：Suppose you need to write a function that takes a name as a parameter, logs the cur‐ rent date and time, then adds the name to a global data structure. You might come up with a function that looks something like this: std::multiset<std::string> names; // global data structure void logAndAdd(const std::string& name) { auto now = // get current time std::chrono::system_clock::now(); log(now, "logAndAdd"); // make log entry names.emplace(name); // add name to global data } // structure; see Item 42 // for info on emplace This isn’t unreasonable code, but it’s not as efficient as it could be. …

## Item 27

- **规则**：Familiarize yourself with alternatives to overloading on universal references.
- **引用键**：`book:effective-modern-cpp:item27`
- **书中要点**：overloading on universal references. Item 26 explains that overloading on universal references can lead to a variety of problems, both for freestanding and for member functions (especially constructors). Yet it also gives examples where such overloading could be useful. If only it would behave the way we’d like! This Item explores ways to achieve the desired behavior, either through designs that avoid overloading on universal references or by employ‐ ing them in ways that constrain the types of arguments they can match. The discussion that follows builds on the examples introduced in Item 26 . …

## Item 28，p.197

- **规则**：Understand reference collapsing.
- **引用键**：`book:effective-modern-cpp:item28`
- **书中要点**：Item 23 remarks that when an argument is passed to a template function, the type deduced for the template parameter encodes whether the argument is an lvalue or an rvalue. The Item fails to mention that this happens only when the argument is used to initialize a parameter that’s a universal reference, but there’s a good reason for the omission: universal references aren’t introduced until Item 24. …

## Item 29

- **规则**：Assume that move operations are not present, not cheap, and not used.
- **引用键**：`book:effective-modern-cpp:item29`
- **书中要点**：not cheap, and not used. Move semantics is arguably the premier feature of C++11. “Moving containers is now as cheap as copying pointers!” you’re likely to hear, and “Copying temporary objects is now so efficient, coding to avoid it is tantamount to premature optimization!” Such sentiments are easy to understand. Move semantics is truly an important feature. It doesn’t just allow compilers to replace expensive copy operations with comparatively cheap moves, it actually requires that they do so (when the proper conditions are ful‐ filled). …

## Item 30，p.207

- **规则**：Familiarize yourself with perfect forwarding failure cases.
- **引用键**：`book:effective-modern-cpp:item30`
- **书中要点**：failure cases. One of the features most prominently emblazoned on the C++11 box is perfect for‐ warding. Perfect forwarding. It’s perfect! Alas, tear the box open, and you’ll find that there’s “perfect” (the ideal), and then there’s “perfect” (the reality). C++11’s perfect forwarding is very good, but it achieves true perfection only if you’re willing to over‐ look an epsilon or two. This Item is devoted to familiarizing you with the epsilons. …

## Item 31，p.216

- **规则**：Avoid default capture modes.
- **引用键**：`book:effective-modern-cpp:item31`
- **书中要点**：There are two default capture modes in C++11: by-reference and by-value. Default by-reference capture can lead to dangling references. Default by-value capture lures you into thinking you’re immune to that problem (you’re not), and it lulls you into thinking your closures are self-contained (they may not be). That’s the executive summary for this Item. If you’re more engineer than executive, you’ll want some meat on those bones, so let’s start with the danger of default by- reference capture. …

## Item 32，p.224

- **规则**：Use init capture to move objects into closures.
- **引用键**：`book:effective-modern-cpp:item32`
- **书中要点**：Sometimes neither by-value capture nor by-reference capture is what you want. If you have a move-only object (e.g., a std::unique_ptr or a std::future) that you want to get into a closure, C++11 offers no way to do it. If you have an object that’s expensive to copy but cheap to move (e.g., most containers in the Standard Library), and you’d like to get that object into a closure, you’d much rather move it than copy it. Again, however, C++11 gives you no way to accomplish that. But that’s C++11. C++14 is a different story. It offers direct support for moving objects into closures. …

## Item 33，p.229

- **规则**：Use decltype on auto&& parameters to std::forward them.
- **引用键**：`book:effective-modern-cpp:item33`
- **书中要点**：std::forward them. One of the most exciting features of C++14 is generic lambdas —lambdas that use auto in their parameter specifications. The implementation of this feature is straight‐ forward: operator() in the lambda’s closure class is a template. Given this lambda, for example, `auto f = [](auto x){ return func(normalize(x)); };` the closure class’s function call operator looks like this: class SomeCompilerGeneratedClassName { public: template<typename T> // see Item 3 for auto operator()(T x) const // auto return type { return func(normalize(x)); } … // other closure class }; // functionality In this example, …

## Item 34，p.232

- **规则**：Prefer lambdas to std::bind.
- **引用键**：`book:effective-modern-cpp:item34`
- **书中要点**：std::bind is the C++11 successor to C++98’s std::bind1st and std::bind2nd, but, informally, it’s been part of the Standard Library since 2005. That’s when the Standardization Committee adopted a document known as TR1, which included bind’s specification. (In TR1, bind was in a different namespace, so it was std::tr1::bind, not std::bind, and a few interface details were different.) This history means that some programmers have a decade or more of experience using std::bind. If you’re one of them, you may be reluctant to abandon a tool that’s served you well. …

## Item 35，p.241

- **规则**：Prefer task-based programming to thread-based.
- **引用键**：`book:effective-modern-cpp:item35`
- **书中要点**：based. If you want to run a function doAsyncWork asynchronously, you have two basic choices. You can create a std::thread and run doAsyncWork on it, thus employing a thread-based approach: int doAsyncWork(); std::thread t(doAsyncWork); Or you can pass doAsyncWork to std::async, a strategy known as task-based: 1 Assuming you have one. Some embedded systems don’t. auto fut = std::async(doAsyncWork); // "fut" for "future" In such calls, the function object passed to std::async (e.g., doAsyncWork) is con‐ sidered a task. …

## Item 36，p.245

- **规则**：Specify std::launch::async if asynchronicity is essential.
- **引用键**：`book:effective-modern-cpp:item36`
- **书中要点**：asynchronicity is essential. When you call std::async to execute a function (or other callable object), you’re generally intending to run the function asynchronously. But that’s not necessarily what you’re asking std::async to do. You’re really requesting that the function be run in accord with a std::async launch policy. There are two standard policies, each 2 This is a simplification. What matters isn’t the future on which get or wait is invoked, it’s the shared state to which the future refers. …

## Item 37，p.250

- **规则**：Make std::threads unjoinable on all paths.
- **引用键**：`book:effective-modern-cpp:item37`
- **书中要点**：Every std::thread object is in one of two states: joinable or unjoinable. A joinable std::thread corresponds to an underlying asynchronous thread of execution that is or could be running. A std::thread corresponding to an underlying thread that’s blocked or waiting to be scheduled is joinable, for example. std::thread objects cor‐ responding to underlying threads that have run to completion are also considered joinable. An unjoinable std::thread is what you’d expect: a std::thread that’s not joinable. Unjoinable std::thread objects include: • Default-constructed std::threads. …

## Item 38，p.258

- **规则**：Be aware of varying thread handle destructor behavior.
- **引用键**：`book:effective-modern-cpp:item38`
- **书中要点**：behavior. Item 37 explains that a joinable std::thread corresponds to an underlying system thread of execution. A future for a non-deferred task (see Item 36) has a similar rela‐ tionship to a system thread. As such, both std::thread objects and future objects can be thought of as handles to system threads. From this perspective, it’s interesting that std::threads and futures have such dif‐ ferent behaviors in their destructors. …

## Item 39

- **规则**：Consider void futures for one-shot event communication.                  262 viii | Table of Contents === PAGE 11 ===
- **引用键**：`book:effective-modern-cpp:item39`
- **书中要点**：communication. Sometimes it’s useful for a task to tell a second, asynchronously running task that a particular event has occurred, because the second task can’t proceed until the event has taken place. Perhaps a data structure has been initialized, a stage of computation has been completed, or a significant sensor value has been detected. When that’s the case, what’s the best way for this kind of inter-thread communication to take place? An obvious approach is to use a condition variable ( condvar). …

## Item 40，p.271

- **规则**：Use std::atomic for concurrency, volatile for special memory.
- **引用键**：`book:effective-modern-cpp:item40`
- **书中要点**：for special memory. Poor volatile. So misunderstood. It shouldn’t even be in this chapter, because it has nothing to do with concurrent programming. But in other programming languages (e.g., Java and C#), it is useful for such programming, and even in C++, some compil‐ ers have imbued volatile with semantics that render it applicable to concurrent software (but only when compiled with those compilers). It’s thus worthwhile to dis‐ cuss volatile in a chapter on concurrency if for no other reason than to dispel the confusion surrounding it. …

## Item 41

- **规则**：Consider pass by value for copyable parameters that are cheap to move and always copied.
- **引用键**：`book:effective-modern-cpp:item41`
- **书中要点**：that are cheap to move and always copied. Some function parameters are intended to be copied. 1 For example, a member func‐ tion addName might copy its parameter into a private container. For efficiency, such a function should copy lvalue arguments, but move rvalue arguments: class Widget { public: void addName(const std::string& newName) // take lvalue; { names.push_back(newName); } // copy it void addName(std::string&& newName) // take rvalue; { names.push_back(std::move(newName)); } // move it; see … // Item 25 for use // of std::move private: std::vector<std::string> names; }; This works, but it requires writ …

## Item 42

- **规则**：Consider emplacement instead of insertion.                                            292 Index. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- **引用键**：`book:effective-modern-cpp:item42`
- **书中要点**：If you have a container holding, say, std::strings, it seems logical that when you add a new element via an insertion function (i.e., insert, push_front, push_back, or, for std::forward_list, insert_after), the type of element you’ll pass to the function will be std::string. After all, that’s what the container has in it. Logical though this may be, it’s not always true. …
