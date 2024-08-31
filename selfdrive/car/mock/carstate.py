import random

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
