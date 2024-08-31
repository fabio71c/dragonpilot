#!/usr/bin/env python3
import time
from openpilot.common.params import Params

def set_params():
    params = Params()
    params.put_bool("UpdateAvailable", False)
    params.put_bool("UpdaterFetchAvailable", False)
    params.put("UpdaterTargetBranch", "")
    params.put("UpdaterAvailableBranches", "")
    params.put("UpdateFailedCount", "0")

def main():
    set_params()
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
