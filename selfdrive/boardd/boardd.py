# pylint: skip-file

# Cython, now uses scons to build
from openpilot.selfdrive.boardd.boardd_api_impl import can_list_to_can_capnp
assert can_list_to_can_capnp

import time
from openpilot.system.swaglog import cloudlog
from selfdrive.car.toyota.values import CAR as TOYOTA

def can_capnp_to_can_list(can, src_filter=None):
  ret = []
  for msg in can:
    if src_filter is None or msg.src in src_filter:
      ret.append((msg.address, msg.busTime, msg.dat, msg.src))
  return ret

def can_sender(panda, msgs, bus):
  # Comment out the original implementation
  # try:
  #   for m in msgs:
  #     panda.can_send(m.address, m.dat, bus)
  # except panda.CanPacketDropped:
  #   cloudlog.error("Bus %d dropped at %d with %d messages remaining", bus, time.time(), len(msgs))
  #   return False

  # Always return True to simulate successful sending
  return True

def get_fake_panda():
    class FakePanda:
        def __init__(self):
            self.health = {"voltage": 12000, "current": 5000, "uptime": 1000}
        def get_health(self):
            return self.health
        def can_recv(self):
            # Simulate receiving CAN messages
            return []
        def can_send(self, addr, dat, bus):
            # Simulate sending CAN messages
            return True
    return FakePanda()

def boardd_mock_loop():
  # Simulate panda presence
  cloudlog.info("Simulating panda presence")

  # Simulate car data
  while True:
    # Create fake CAN messages here
    fake_can_msgs = [
      # Example: Speed message (modify according to the car model you're simulating)
      {"address": 0x2c4, "dat": b'\x00\x00\x00\x00\x00\x00\x00\x00', "bus": 0},
      # Add more fake messages as needed
    ]

    # Send fake messages
    for msg in fake_can_msgs:
      can_sender(None, [msg], msg['bus'])

    time.sleep(0.01)  # Simulate message frequency

def boardd_loop():
  cloudlog.info("Starting fake boardd loop")
  fake_panda = get_fake_panda()
  
  while True:
    # Simulate panda communication
    can_recv = fake_panda.can_recv()
    health = fake_panda.get_health()
    
    # Log some fake data to show it's working
    if len(can_recv) > 0:
      cloudlog.debug(f"Received {len(can_recv)} fake CAN messages")
    
    cloudlog.debug(f"Fake panda health: {health}")
    
    time.sleep(0.01)
