#pragma once

#include <string>
#include <vector>
#include <cstdlib>

#include "selfdrive/boardd/panda.h"

// Add this function declaration to check for mock Panda
inline bool use_mock_panda() {
    const char* mock_panda_env = std::getenv("USE_MOCK_PANDA");
    return mock_panda_env != nullptr && std::string(mock_panda_env) == "1";
}

// Modify these function declarations to handle mock Panda
bool safety_setter_thread(std::vector<Panda *> pandas);
void boardd_main_thread(std::vector<std::string> serials);

// Add these mock function declarations
void mock_safety_setter_thread();
void mock_boardd_main_thread(std::vector<std::string> serials);
