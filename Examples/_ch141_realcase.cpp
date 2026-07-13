// Examples/_ch141_realcase.cpp
// 真实案例：交易网关（TradingGateway）注入行情源与风控，单测可换 fake，生产可换真实实现。
#include <cassert>
#include <iostream>
#include <memory>
#include <string>

struct IMarketData { virtual ~IMarketData() = default; virtual double price(const std::string&) = 0; };
struct LiveMarket  : IMarketData { double price(const std::string&) override { return 100.0; } };
struct FakeMarket  : IMarketData { double price(const std::string&) override { return 1.0; } };

struct IRisk { virtual ~IRisk() = default; virtual bool allow(double) = 0; };
struct SimpleRisk : IRisk { bool allow(double p) override { return p < 1000.0; } };

class TradingGateway {
    std::unique_ptr<IMarketData> md_;
    std::unique_ptr<IRisk> risk_;
public:
    TradingGateway(std::unique_ptr<IMarketData> md, std::unique_ptr<IRisk> rk)
        : md_(std::move(md)), risk_(std::move(rk)) {}
    bool submit(const std::string& sym) {
        double p = md_->price(sym);
        return risk_->allow(p);
    }
};

int main() {
    TradingGateway prod(std::make_unique<LiveMarket>(), std::make_unique<SimpleRisk>());
    TradingGateway test(std::make_unique<FakeMarket>(), std::make_unique<SimpleRisk>());
    std::cout << "prod=" << prod.submit("AAPL") << " test=" << test.submit("AAPL") << "\n";
    assert(test.submit("AAPL") == true);
}
