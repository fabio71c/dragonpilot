# pylint: skip-file

# Cython, now uses scons to build
import time
from openpilot.system.swaglog import cloudlog
from openpilot.common.params import Params
from openpilot.selfdrive.boardd.boardd_api_impl import can_list_to_can_capnp

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

    def health_check(self):
        return True

def boardd_loop(fake_panda, sendcan, logcan, pandad_thread):
    cloudlog.info("Starting boardd loop with fake panda")
    params = Params()

    while True:
        health = fake_panda.get_health()
        cloudlog.debug(f"Fake panda health: {health}")

        # Send an empty list of CAN messages
        can_sends = []
        sendcan.send(can_list_to_can_capnp(can_sends, msgtype='sendcan'))

        # Receive an empty list of CAN messages
        can_rcv = fake_panda.can_recv()
        logcan.send(can_list_to_can_capnp(can_rcv, msgtype='can'))

        time.sleep(0.01)

def panda_connect():
    cloudlog.info("Connecting to fake panda")
    return FakePanda()

def main(sendcan, logcan, pandad_thread):
    cloudlog.info("Boardd is using a fake panda")
    fake_panda = panda_connect()
    boardd_loop(fake_panda, sendcan, logcan, pandad_thread)

if __name__ == "__main__":
    main()
