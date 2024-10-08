import can
import time

# Set up virtual CAN bus (vcan0)
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

try:
    speed_value = 0
    increment = 5
    while True:
        # Simulate vehicle speed CAN message
        data = [
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
            (speed_value >> 8) & 0xFF, speed_value & 0xFF,
        ]
        message = can.Message(arbitration_id=0x4B0, data=data, is_extended_id=False)
        bus.send(message)
        print(f'Current speed:\t{speed_value}mph')
        
        # Update speed value to oscillate between 0 and 120
        speed_value += increment
        if speed_value >= 120 or speed_value <= 0:
            increment = -increment
        
        time.sleep(0.5)  # Send message every 0.5 seconds

except KeyboardInterrupt:
    print("Vehicle emulator terminated.")