#!/usr/bin/env python3
import time
import os
import signal

from cereal import car, log, messaging
from openpilot.common.params import Params
from openpilot.selfdrive.manager.process_config import managed_processes

def cleanup_sockets():
    os.system("rm -rf /tmp/openpilot_*")

def signal_handler(sig, frame):
    print('Cleaning up and exiting...')
    cleanup_sockets()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
cleanup_sockets()

if __name__ == "__main__":
  CP = car.CarParams(notCar=True)
  Params().put("CarParams", CP.to_bytes())

  procs = ['camerad', 'ui', 'modeld', 'calibrationd']
  for p in procs:
    managed_processes[p].start()

  pm = messaging.PubMaster(['controlsState', 'deviceState', 'pandaStates', 'carParams'])

  msgs = {s: messaging.new_message(s) for s in ['controlsState', 'deviceState', 'carParams']}
  msgs['deviceState'].deviceState.started = True
  msgs['carParams'].carParams.openpilotLongitudinalControl = True

  msgs['pandaStates'] = messaging.new_message('pandaStates', 1)
  msgs['pandaStates'].pandaStates[0].ignitionLine = True
  msgs['pandaStates'].pandaStates[0].pandaType = log.PandaState.PandaType.uno
  msgs['controlsState'] = mock_controls_state

  try:
    while True:
      try:
          for s in msgs:
              try:
                  pm.send(s, msgs[s])
              except Exception as e:
                  print(f"Error sending message {s}: {e}")
                  time.sleep(0.1)  # Add a small delay
          time.sleep(0.01)  # Add a small delay in the main loop
      except Exception as e:
          print(f"Main loop error: {e}")
          time.sleep(1)  # Longer delay if there's an error
  except KeyboardInterrupt:
    for p in procs:
      managed_processes[p].stop()
