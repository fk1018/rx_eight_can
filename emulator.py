import can
import time

# Set up virtual CAN bus (vcan0)
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

try:
    while True:
        # Simulate vehicle speed CAN message
        speed_value = 50  # Change this value for testing different speeds
        data = [
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
        ]
        message = can.Message(arbitration_id=0x4B0, data=data, is_extended_id=False)
        bus.send(message)
        time.sleep(0.5)  # Send message every 0.5 seconds

except KeyboardInterrupt:
    print("Vehicle emulator terminated.")
