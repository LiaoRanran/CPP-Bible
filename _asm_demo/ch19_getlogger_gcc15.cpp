#include <string>

struct Logger {
    std::string name;
};

Logger& getLogger() {
    static Logger instance{"logger"};   // __cxa_guard 保证只构造一次
    return instance;
}
