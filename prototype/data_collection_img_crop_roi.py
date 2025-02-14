# Code to take snapshot at interval based on pre-determined time duration and image settings
# Also, image files are saved using time data for traceability reasons

import sensor
import pyb
import time
import image
import lcd
import os
import random

RED_LED_PIN = 1
BLUE_LED_PIN = 3

w = 123
h = 44
x1_v = 74
y1_v = 73
x2_v = 75
y2_v = 71
x1_h = 75
y1_h = 75
x2_h = 75+120
y2_h = 75

sensor.reset()  # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565)  # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA)  # or sensor.QVGA (or others)
sensor.skip_frames(time=10000)  # Let new settings take affect.
lcd.init()  # Initialize the lcd screen.

pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time=2000)  # Give the user time to get ready.
pyb.LED(RED_LED_PIN).off()

welcome_string = "We're live!"
exit_string = "\nDone!\n"
snapshot_interval = 60000   # interval in milliseconds
image_folder_name = "Collection"+'_'+str(time.mktime(time.gmtime()))
welcome_display_delay = 3000
exit_display_delay = 60000
print(f"{welcome_string}")

img = sensor.snapshot()
img.draw_string(0, 0, str(welcome_string), scale=1)
lcd.display(img)
time.sleep_ms(welcome_display_delay)

if not image_folder_name in os.listdir():
    os.mkdir(image_folder_name)
    print(f"directory {image_folder_name} created")

image_counter = 0
time_record_start_seconds = time.mktime(time.gmtime())
record_length_seconds = 10800   # pre-defined video length in seconds


def snapshot_function(image_counter):
    while(time.mktime(time.gmtime()) - time_record_start_seconds < record_length_seconds):
        pyb.LED(BLUE_LED_PIN).on()
        time_diff = time.mktime(time.gmtime()) - time_record_start_seconds
        image_counter += 1
        print(f"img count: {image_counter} | time diff: {time_diff}")
        image_file_name = "Img"+'_' + \
            str(image_counter)+'_'+str(time.mktime(time.gmtime()))
        img = sensor.snapshot()
        img.draw_rectangle(x1_v, y1_v, w, h)
        img.crop(roi=(x1_v, y1_v, w, h))
        img.save(str(image_folder_name)+'/'+str(image_file_name), quality=100)
        lcd.display(img)
        print(f"{image_file_name}")
        pyb.LED(BLUE_LED_PIN).off()
        time.sleep_ms(snapshot_interval)


snapshot_function(image_counter)

print(f"{exit_string}")

img = sensor.snapshot()
img.draw_string(0, 0, str(exit_string), scale=1)
lcd.display(img)
time.sleep_ms(exit_display_delay)
