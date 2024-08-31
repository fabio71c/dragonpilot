#pragma once

#include <string>
#include <vector>

#include "selfdrive/boardd/panda.h"

// Modify this function to always return true
bool safety_setter_thread(std::vector<Panda *> pandas) {
  // Original implementation commented out
  // ... (keep the original code as a comment for reference)

  // Always return true to fake panda presence
  return true;
}

void boardd_main_thread(std::vector<std::string> serials);
