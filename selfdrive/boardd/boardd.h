#pragma once

#include <string>
#include <vector>
#include <cstdlib>
#include <memory>

#include "selfdrive/boardd/panda.h"

// Function to check for mock Panda
inline bool use_mock_panda() {
    const char* mock_panda_env = std::getenv("USE_MOCK_PANDA");
    return mock_panda_env != nullptr && std::string(mock_panda_env) == "1";
}

// Abstract base class for Panda operations
class PandaInterface {
public:
    virtual ~PandaInterface() = default;
    virtual bool safety_setter_thread() = 0;
    virtual void boardd_main_thread(const std::vector<std::string>& serials) = 0;
};

// Real Panda implementation
class RealPanda : public PandaInterface {
public:
    bool safety_setter_thread() override;
    void boardd_main_thread(const std::vector<std::string>& serials) override;
};

// Mock Panda implementation
class MockPanda : public PandaInterface {
public:
    bool safety_setter_thread() override;
    void boardd_main_thread(const std::vector<std::string>& serials) override;
};

// Factory function to create appropriate Panda interface
std::unique_ptr<PandaInterface> create_panda_interface();

// Wrapper functions that use the appropriate implementation
bool safety_setter_thread(std::vector<Panda*> pandas);
void boardd_main_thread(const std::vector<std::string>& serials);