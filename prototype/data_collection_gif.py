# GIF Video Recording Example
#
# Note: You will need an SD card to run this example.
#
# You can use your OpenMV Cam to record gif files. You can either feed the
# recorder object RGB565 frames or Grayscale frames. Use photo editing software
# like GIMP to compress and optimize the Gif before uploading it to the web.

import sensor, image, time, gif, pyb, lcd, time, random

RED_LED_PIN = 1
BLUE_LED_PIN = 3

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.
lcd.init() # Initialize the lcd screen.

pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000) # Give the user time to get ready.

pyb.LED(RED_LED_PIN).off()
pyb.LED(BLUE_LED_PIN).on()

random_num = random.randint(0, 100)
random_num_2 = random.randint(0, 100)
print(random_num)
g = gif.Gif(f"Meter_Recording_{random_num}{random_num_2}.gif", loop=True)

print("We're live!")

time_record_start_seconds = time.mktime(time.gmtime())

video_length_seconds = 60   # pre-defined video length in seconds

while(time.mktime(time.gmtime()) - time_record_start_seconds < video_length_seconds):
    time_diff = time.mktime(time.gmtime()) - time_record_start_seconds
    print(f"time difference: {time_diff}")
    img = sensor.snapshot()
    lcd.display(img) # Take a picture and display the image.

    clock.tick()# clock.avg() returns the milliseconds between frames - gif delay is in
    g.add_frame(sensor.snapshot(), delay=int(clock.avg()/50)) # delay in centiseconds.
    #g.add_frame(sensor.snapshot(), delay=1000) # delay in centiseconds.
    img.draw_string(0,0,str(time_diff))
    print(clock.fps())
    lcd.display(img)

print("\nVideo Length in second(s):", time.mktime(time.gmtime()) - time_record_start_seconds)

g.close()
pyb.LED(BLUE_LED_PIN).off()
print("\nDone! Reset the camera to see the saved recording.\n")
