# pylint: skip-file
from selfdrive.boardd.pandad import MockPanda as Panda

def boardd_thread(sm=None, pm=None):
    global mock_panda
    mock_panda = Panda()

    while True:
        try:
            # Simulate receiving CAN messages
            received = mock_panda.can_recv()
            print(f"Received CAN messages: {received}")
        except Exception as e:
            print(f"Error receiving CAN messages: {e}")
        # ... rest of the loop

          # Simulate sending CAN messages 
# Cython, now uses scons to build
from openpilot.selfdrive.boardd.boardd_api_impl import can_list_to_can_capnp
assert can_list_to_can_capnp

def can_capnp_to_can_list(can, src_filter=None):
  ret = []
  for msg in can:
    if src_filter is None or msg.src in src_filter:
      ret.append((msg.address, msg.busTime, msg.dat, msg.src))
  return ret
