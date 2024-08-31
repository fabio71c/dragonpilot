import time
import traceback
from selfdrive.boardd.pandad import MockPanda as Panda

def boardd_thread(sm=None, pm=None):
    print("Starting boardd_thread")
    global mock_panda
    mock_panda = Panda()
    print("Mock Panda initialized")

    while True:
        try:
            print("Boardd loop iteration")
            health = mock_panda.health()
            print(f"Mock panda health: {health}")
            
            # Simulate receiving CAN messages
            received = mock_panda.can_recv()
            if received:
                print(f"Received CAN messages: {received}")
            else:
                print("No CAN messages received")
            
            # Simulate sending CAN messages
            mock_panda.can_send_many([(0x1, 0, b'\x01\x02\x03', 0)])
            print("Sent mock CAN message")
            
            time.sleep(1)  # Sleep for 1 second to prevent flooding the console
        except Exception as e:
            print(f"Error in boardd_thread: {e}")
            print("Traceback:")
            traceback.print_exc()
            time.sleep(1)

if __name__ == "__main__":
    print("Starting boardd.py")
    boardd_thread()
