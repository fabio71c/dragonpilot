import random
from openpilot.selfdrive.car.fingerprints import FW_VERSIONS, CAR
from openpilot.selfdrive.car.honda.values import CAR as HONDA

class MockPanda:
    def __init__(self):
        self.health = {
            "voltage": 12000,
            "current": 5000,
            "can_rx_errs": 0,
            "can_send_errs": 0,
            "gmlan_send_errs": 0,
            "fault_status": 0,
            "ignition_line": 1,
            "gas_interceptor_detected": 0,
            "car_harness_status": 1,
            "usb_power_mode": 1,
            "safety_mode": 1,
            "safety_param": 0,
            "heartbeat_lost": False,
        }
        self.can_valid = True
        self.safety_model = 1
        self.hw_type = 3
        self.has_rtc = False
        self.is_grey = True
        self.car_fingerprint = HONDA.CIVIC  # Example fingerprint

    def health(self):
        return self.health

    def can_send(self, addr, dat, bus):
        # Simulate sending CAN message
        print(f"Sending CAN message: addr={addr}, dat={dat}, bus={bus}")
        return True

    def can_recv(self):
        # Simulate receiving CAN messages
        messages = []
        for _ in range(random.randint(1, 5)):
            addr = random.randint(0, 2047)
            bus = random.randint(0, 2)
            dat = bytes([random.randint(0, 255) for _ in range(8)])
            messages.append((addr, 0, dat, bus))
        return messages

    def get_firmware_version(self):
        return random.choice(list(FW_VERSIONS[CAR.HONDA_CIVIC_2016]))

    def set_safety_mode(self, mode):
        self.safety_model = mode
        print(f"Safety mode set to: {mode}")

    def set_can_loopback(self, enable):
        pass

    def set_power_save(self, power_save_enable):
        pass

    def set_esp_power(self, enabled):
        pass

def init_mock_panda():
    return MockPanda()