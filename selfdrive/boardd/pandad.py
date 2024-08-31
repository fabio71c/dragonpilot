#!/usr/bin/env python3
import os
import time
import random
from typing import NoReturn, Dict, List

from openpilot.common.params import Params
from openpilot.system.swaglog import cloudlog

class MockPanda:
    def __init__(self):
        self._health = {
            'voltage': 12000,
            'current': 5000,
            'can_send_errs': 0,
            'can_rx_errs': 0,
            'gmlan_send_errs': 0,
            'fault_status': 0,
            'safety_mode': 2,  # SAFETY_ALLOUTPUT
            'power_save_enabled': False,
            'uptime': 0,
            'tx_buffer_overflow': 0,
            'rx_buffer_overflow': 0,
            'fan_power': 0,
            'safety_tx_blocked': 0,
            'safety_rx_invalid': 0,
            'ignition_line': 1,
            'ignition_can': 1,
        }
        self.can_messages = []  # Initialize the can_messages list

    def health(self):
        self._health['uptime'] += 1
        return self._health

    def can_recv(self):
        # Generate random CAN messages
        num_messages = random.randint(0, 10)
        received = []
        for _ in range(num_messages):
            addr = random.randint(0, 0x7FF)
            bus = random.randint(0, 2)
            data = bytes([random.randint(0, 255) for _ in range(8)])
            received.append((addr, 0, data, bus))
        return received

    def can_send_many(self, can_msgs, timeout=None):
        # Simulate sending CAN messages
        self.can_messages.extend(can_msgs)
        return True

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

def pandad_thread():
    global mock_panda
    mock_panda = MockPanda()

    while True:
        health = mock_panda.health()
        print(f"Mock panda health: {health}")
        
        # Simulate receiving CAN messages
        received = mock_panda.can_recv()
        if received:
            print(f"Received CAN messages: {received}")
        
        # Simulate sending CAN messages
        mock_panda.can_send_many([(0x1, 0, b'\x01\x02\x03', 0)])
        
        time.sleep(0.1)  # Sleep to prevent busy-waiting

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