import time
import traceback
import random
from cereal import car
import capnp

class MockCarState:
    def __init__(self):
        self.speed = 0
        self.steeringAngle = 0
        self.steeringTorque = 0
        self.brake = 0
        self.gas = 0
        self.gear_shifter = car.CarState.GearShifter.drive

    def update(self):
        self.speed += random.uniform(-1, 1)
        self.speed = max(0, min(self.speed, 120))
        self.steeringAngle = random.uniform(-30, 30)
        self.steeringTorque = random.uniform(-1, 1)
        self.brake = random.uniform(0, 1)
        self.gas = random.uniform(0, 1)

MOCK_CARSTATE = MockCarState()

def can_list_to_can_capnp(can_msgs):
    dat = car.CanData.new_message()
    dat.canId = []
    dat.dat = []
    dat.src = []
    for can_id, _, data, src in can_msgs:
        dat.canId.append(can_id)
        dat.dat.append(data)
        dat.src.append(src)
    return dat

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
            'uptime': 0,
            'tx_buffer_overflow': 0,
            'rx_buffer_overflow': 0,
            'fan_power': 0,
            'safety_tx_blocked': 0,
            'safety_rx_invalid': 0,
            'ignition_line': 1,
            'ignition_can': 1,
        }

    def health(self):
        self.health['uptime'] += 1
        return self.health

    def can_recv(self):
        # Generate random CAN messages
        num_messages = random.randint(0, 10)
        messages = []
        for _ in range(num_messages):
            addr = random.randint(0, 0x7FF)
            bus = random.randint(0, 2)
            data = bytes([random.randint(0, 255) for _ in range(8)])
            messages.append((addr, 0, data, bus))
        return messages

    def can_send_many(self, can_msgs, timeout=None):
        # Simulate sending CAN messages
        return True

def get_panda():
    return MockPanda()

def boardd_thread(sm=None, pm=None):
    print("Starting boardd_thread")
    global mock_panda
    mock_panda = get_panda()
    print("Mock Panda initialized")

    while True:
        try:
            print("Boardd loop iteration")
            health = mock_panda.health()
            print(f"Mock panda health: {health}")
            
            # Simulate receiving CAN messages
            received = mock_panda.can_recv()
            if received:
                print(f"Received {len(received)} CAN messages")
                for msg in received[:5]:  # Print first 5 messages
                    print(f"  {msg}")
            else:
                print("No CAN messages received")
            
            # Simulate sending CAN messages
            mock_panda.can_send_many([(0x1, 0, b'\x01\x02\x03', 0)])
            print("Sent mock CAN message")
            
            time.sleep(1)  # Sleep for 1 second to prevent flooding the console
        except Exception as e:
            print(f"Error in boardd_thread: {e}")
            print("Traceback:")
            traceback.print_exc()
            time.sleep(1)

if __name__ == "__main__":
    print("Starting boardd.py")
    boardd_thread()
