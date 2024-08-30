#!/usr/bin/env python3
import os
import time
import random
from typing import NoReturn, Dict, List

from openpilot.common.params import Params
from openpilot.system.swaglog import cloudlog

class MockPanda:
    def __init__(self):
        self.health = {
            'voltage': 12000,
            'current': 5000,
            'can_send_errs': 0,
            'can_rx_errs': 0,
            'gmlan_send_errs': 0,
            'fault_status': 0,
            'power_save_enabled': False,
            'safety_mode': 0,
            'heartbeat_lost': False,
        }
        self.can_messages = []

    def get_health(self) -> Dict:
        # Simulate some fluctuation in voltage and current
        self.health['voltage'] = 12000 + random.randint(-500, 500)
        self.health['current'] = 5000 + random.randint(-1000, 1000)
        self.health['uptime'] = int(time.time())
        return self.health

    def can_send(self, messages: List) -> None:
        self.can_messages.extend(messages)
        print(f"Sent CAN messages: {messages}")

    def can_recv(self) -> List:
        # Simulate receiving CAN messages
        received = self.can_messages[:random.randint(0, len(self.can_messages))]
        self.can_messages = self.can_messages[len(received):]
        print(f"Received CAN messages: {received}")
        return received

    def set_safety_mode(self, mode: int) -> None:
        self.health['safety_mode'] = mode
        print(f"Safety mode set to: {mode}")

def mock_boardd(panda: MockPanda) -> None:
    print("Mock boardd running...")
    # Simulate boardd operations
    panda.set_safety_mode(2)  # Set to some safety mode
    messages_to_send = [(0x200, 0, b'\x01\x02\x03', 0)]  # Example CAN message
    panda.can_send(messages_to_send)
    received = panda.can_recv()
    health = panda.get_health()
    print(f"Current panda health: {health}")

def main() -> NoReturn:
    print("Starting mock pandad")
    count = 0
    params = Params()
    mock_panda = MockPanda()

    while True:
        try:
            count += 1
            print(f"Mock pandad iteration: {count}")
            cloudlog.event("mock_pandad.iteration", count=count)

            # Simulate pandad activities
            mock_boardd(mock_panda)

            # Simulate some activity
            time.sleep(5)

        except Exception:
            cloudlog.exception("mock_pandad.uncaught_exception")

        time.sleep(5)

if __name__ == "__main__":
    main()