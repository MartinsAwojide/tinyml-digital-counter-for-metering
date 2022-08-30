# Draw Rectangle
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor
import image
import time

sensor.reset()                      # Reset and initialize the sensor.
# Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
x1_v = 75
y1_v = 107
w = 123
h = 40

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    img = img.draw_rectangle(x1_v, y1_v, w, h)
    # Note: OpenMV Cam runs about half as fast when connected
    print(clock.fps())
    # to the IDE. The FPS should increase once disconnected.
