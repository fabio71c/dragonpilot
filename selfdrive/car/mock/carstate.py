import random
from openpilot.selfdrive.car.interfaces import CarStateBase

class MockCarState:
    def __init__(self):
        self.speed = 0
        self.steering_angle = 0
        self.gas = 0
        self.brake = 0
        self.is_engaged = False

    def update(self):
        # Simulate some basic car behavior
        self.speed += random.uniform(-1, 1)
        self.speed = max(0, min(self.speed, 120))  # Keep speed between 0 and 120
        self.steering_angle = random.uniform(-30, 30)
        self.gas = random.uniform(0, 1)
        self.brake = random.uniform(0, 1)
        self.is_engaged = random.choice([True, False])

def get_car_state():
    return MockCarState()

class CarState(CarStateBase):
    def __init__(self, CP):
        super().__init__(CP)
        self.speed = 0
        self.steering_angle = 0
        self.brake_pressed = False
        self.gas_pressed = False

    def update(self, cp, cp_cam):
        # Update mock state here
        self.speed += 1  # Just an example, increase speed by 1 unit each update
        self.steering_angle = (self.steering_angle + 5) % 360  # Rotate steering
        self.brake_pressed = not self.brake_pressed  # Toggle brake
        self.gas_pressed = not self.gas_pressed  # Toggle gas

        return self.speed, self.steering_angle, self.brake_pressed, self.gas_pressed
