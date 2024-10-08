import can
import os
import time
import pygame

# Initialize Pygame for GIF display
pygame.init()
screen = pygame.display.set_mode((800, 480))  # Adjust resolution to match your screen
pygame.display.set_caption("Car Speed GIF Display")

# Load GIFs
under_80_gif = pygame.image.load("under_80.gif")
over_80_gif = pygame.image.load("over_80.gif")

# Set up CAN interface
can_interface = 'can0'  # Update if using a different interface
bus = can.interface.Bus(channel=can_interface, bustype='socketcan')

# Function to display a GIF
def display_gif(gif):
    screen.blit(gif, (0, 0))
    pygame.display.update()

# Main loop to read CAN bus and update display
try:
    while True:
        # Read a message from the CAN bus
        message = bus.recv()
        
        # Check if the message ID matches the vehicle speed ID (e.g., 1200)
        if message.arbitration_id == 0x4B0:  # 0x4B0 is hexadecimal for 1200 in decimal
            # Extract speed data from the CAN message (adjust index as needed)
            front_left_speed = (message.data[0] * 256) + message.data[1] - 10000
            front_right_speed = (message.data[2] * 256) + message.data[3] - 10000
            rear_left_speed = (message.data[4] * 256) + message.data[5] - 10000
            rear_right_speed = (message.data[6] * 256) + message.data[7] - 10000

            # Calculate average vehicle speed (basic approximation)
            vehicle_speed = (front_left_speed + front_right_speed + rear_left_speed + rear_right_speed) / 4

            # Display appropriate GIF based on vehicle speed
            if vehicle_speed < 80:
                display_gif(under_80_gif)
            else:
                display_gif(over_80_gif)

        # Allow some delay to avoid spamming the CAN bus
        time.sleep(0.1)

        # Event handling for quitting the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

except KeyboardInterrupt:
    # Gracefully handle script termination
    print("\nTerminating...")
    pygame.quit()
    os._exit(0)