#pragma once

#include <string>
#include <vector>
#include <cstdlib>
#include <iostream>
#include <thread>
#include <chrono>

// Always use mock panda
inline bool use_mock_panda() {
    return true;
}

// Mock implementations
inline void mock_safety_setter_thread() {
    std::cout << "Mock safety setter thread running (doing nothing)" << std::endl;
}

inline void mock_boardd_main_thread(const std::vector<std::string>& serials) {
    std::cout << "Mock boardd main thread running" << std::endl;
    while (true) {
        std::cout << "Mock boardd still running..." << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }
}

// Wrapper functions that now always use mock implementations
inline void safety_setter_thread() {
    mock_safety_setter_thread();
}

inline void boardd_main_thread(const std::vector<std::string>& serials) {
    mock_boardd_main_thread(serials);
}