# pylint: skip-file

# Cython, now uses scons to build
from openpilot.selfdrive.boardd.boardd_api_impl import can_list_to_can_capnp
assert can_list_to_can_capnp

import time
from selfdrive.swaglog import cloudlog
from openpilot.common.params import Params

class FakePanda:
    def __init__(self):
        self.health = {"voltage": 12000, "current": 5000, "uptime": 1000}
        self.serial = "FAKE00000000"

    def get_health(self):
        return self.health

    def can_recv(self):
        return []

    def can_send(self, addr, dat, bus):
        return True

def boardd_loop(fake_panda):
    cloudlog.info("Starting boardd loop with fake panda")
    params = Params()
    params.put("PandaSignatures", fake_panda.serial)

    while True:
        health = fake_panda.get_health()
        cloudlog.debug(f"Fake panda health: {health}")
        time.sleep(0.1)

def panda_connect():
    cloudlog.info("Connecting to fake panda")
    return FakePanda()

def main():
    cloudlog.info("Boardd is using a fake panda")
    fake_panda = panda_connect()
    boardd_loop(fake_panda)

if __name__ == "__main__":
    main()
