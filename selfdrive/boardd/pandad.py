#!/usr/bin/env python3
# simple boardd wrapper that updates the panda first
import os
import usb1
import time
import json
import subprocess
from typing import List, NoReturn
from functools import cmp_to_key

from panda import Panda, PandaDFU, PandaProtocolMismatch, FW_PATH
from openpilot.common.basedir import BASEDIR
from openpilot.common.params import Params
from openpilot.selfdrive.boardd.set_time import set_time
from openpilot.system.hardware import HARDWARE
from openpilot.system.swaglog import cloudlog

# MockPanda class to simulate a connected and healthy Panda
class MockPanda:
    def __init__(self, serial="MOCK_SERIAL"):
        self.serial = serial

    def get_signature(self):
        return b"mock_signature"

    def get_usb_serial(self):
        return "mock_serial"

    def health(self):
        # Simulated health status
        return {
            "uptime": 1000,
            "voltage": 12000,
            "current": 500,
            "safety_tx_blocked": 0,
            "safety_rx_invalid": 0,
            "tx_buffer_overflow": 0,
            "rx_buffer_overflow": 0,
            "gmlan_send_errs": 0,
            "faults": 0,
            "ignition_line": 1,
            "ignition_can": 1,
            "controls_allowed": 1,
            "heartbeat_lost": False,
            "alternative_experience": 0,
            "interrupt_load": 10,
            "fan_power": 50,
            "safety_rx_checks_invalid": 0,
            "spi_checksum_error_count": 0,
            "fan_stall_count": 0,
            "usb_power_mode": 1,
            "torque_interceptor_detected": 0
        }

    def reset(self, reconnect=False):
        pass

    def close(self):
        pass

    def is_internal(self):
        return False

# Modify this function to use MockPanda instead of real Panda
def flash_panda(panda_serial: str) -> MockPanda:
    return MockPanda(panda_serial)

def panda_sort_cmp(a: MockPanda, b: MockPanda):
  # Simulate deterministic ordering for the mock pandas
  return -1 if a.serial < b.serial else 1

def main() -> NoReturn:
  count = 0
  first_run = True
  params = Params()

  print("Running modified pandad.py with MockPanda")
  cloudlog.info("Running modified pandad.py with MockPanda")

  while True:
    try:
      count += 1
      cloudlog.event("pandad.flash_and_connect", count=count)
      params.remove("PandaSignatures")

      # Since we are using a MockPanda, we bypass the DFU checks
      panda_serials = ["MOCK_SERIAL"]
      cloudlog.info(f"{len(panda_serials)} mock panda(s) found, connecting - {panda_serials}")

      # Initialize the mock pandas
      pandas: List[MockPanda] = [flash_panda(serial) for serial in panda_serials]

      # Simulate health checks
      for panda in pandas:
        health = panda.health()
        if health["heartbeat_lost"]:
          params.put_bool("PandaHeartbeatLost", True)
          cloudlog.event("heartbeat lost", deviceState=health, serial=panda.get_usb_serial())

        if first_run:
          cloudlog.info(f"Resetting mock panda {panda.get_usb_serial()}")
          panda.reset()

      # Log panda fw versions
      params.put("PandaSignatures", b','.join(p.get_signature() for p in pandas))

      for p in pandas:
        p.close()

    except Exception:
      cloudlog.exception("pandad.uncaught_exception")
      continue

    first_run = False

    # Run boardd with the mock panda serials as arguments
    os.environ['MANAGER_DAEMON'] = 'boardd'
    os.chdir(os.path.join(BASEDIR, "selfdrive/boardd"))
    subprocess.run(["./boardd", *panda_serials], check=True)

if __name__ == "__main__":
  main()
