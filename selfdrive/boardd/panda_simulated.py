import random
from typing import List, Tuple

class PandaSimulated:
    def __init__(self):
        self.health = {
            "voltage": 12000,
            "current": 5000,
            "uptime": 0,
            "safety_mode": 0,
            "ignition_line": 0,
            "ignition_can": 0,
            "controls_allowed": 1,
            "gas_interceptor_detected": 0,
            "car_harness_status": 1,
            "usb_power_mode": 0,
            "safety_param": 0,
        }
        self.can_health = {
            "bus_off_cnt": 0,
            "error_passive": 0,
            "rx_errs": 0,
            "tx_errs": 0,
            "total_rx_lost_cnt": 0,
            "total_tx_lost_cnt": 0,
            "total_error_cnt": 0,
            "total_tx_cnt": 0,
            "total_rx_cnt": 0,
        }

    def health(self):
        self.health["uptime"] += 1
        return self.health

    def can_health(self, bus):
        self.can_health["total_tx_cnt"] += random.randint(1, 10)
        self.can_health["total_rx_cnt"] += random.randint(1, 10)
        return self.can_health

    def can_send_many(self, can_msgs, bus=0, sync=False):
        # Simulate sending CAN messages
        pass

    def can_recv(self) -> List[Tuple[int, int, bytes, int]]:
        # Simulate receiving CAN messages
        num_msgs = random.randint(0, 5)
        return [(random.randint(0, 2), random.randint(0, 0x7FF), 
                 bytes([random.randint(0, 255) for _ in range(8)]), 0) 
                for _ in range(num_msgs)]

    def get_serial(self):
        return "SIMULATED00000000"

    def get_type(self):
        return "SIMULATED"

    def is_internal(self):
        return True

    def up_to_date(self):
        return True

    def set_safety_mode(self, mode=0):
        self.health["safety_mode"] = mode

    def set_power_save(self, power_save_enabled):
        pass

    def send_heartbeat(self):
        pass

    def set_can_speed_kbps(self, bus, speed):
        pass

    def set_alternative_experience(self, experience):
        pass

    def reset(self):
        pass
