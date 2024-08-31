from openpilot.system.swaglog import cloudlog
from openpilot.selfdrive.boardd.panda_simulated import PandaSimulated
import time

class PandaManager:
    def __init__(self):
        self.panda = None

    def connect_panda(self):
        cloudlog.info("Starting simulated panda")
        while True:
            try:
                self.panda = PandaSimulated()
                cloudlog.info("Connected to simulated panda")
                break
            except Exception:
                cloudlog.exception("pandad.connect_simulated_panda.failed")
            time.sleep(1)

    def run(self):
        self.connect_panda()
        while True:
            try:
                # Your simulation logic here
                # For example:
                health = self.panda.get_health()
                cloudlog.info(f"Simulated panda health: {health}")
                time.sleep(1)
            except Exception as e:
                cloudlog.exception(f"Error in simulated panda loop: {e}")
                time.sleep(1)

def main():
    manager = PandaManager()
    manager.run()

if __name__ == "__main__":
    main()
