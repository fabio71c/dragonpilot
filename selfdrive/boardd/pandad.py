#!/usr/bin/env python3
import os
import time
import subprocess
from typing import NoReturn

from openpilot.common.params import Params
from openpilot.system.swaglog import cloudlog

def main() -> NoReturn:
    print("Starting mock pandad")
    count = 0
    params = Params()

    while True:
        try:
            count += 1
            print(f"Mock pandad iteration: {count}")
            cloudlog.event("mock_pandad.iteration", count=count)

            # Simulate some activity
            time.sleep(5)

            # Run mock boardd
            os.environ['MANAGER_DAEMON'] = 'boardd'
            os.chdir(os.path.join(os.path.dirname(__file__), ".."))
            
            # Instead of running the boardd executable, we'll just print a message
            print("Mock boardd running...")
            time.sleep(5)  # Simulate boardd running for 5 seconds

        except Exception:
            cloudlog.exception("mock_pandad.uncaught_exception")

        time.sleep(5)

if __name__ == "__main__":
    main()