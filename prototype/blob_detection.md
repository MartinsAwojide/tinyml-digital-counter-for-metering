### Find Rectangular Blob 

- Prepare Sensor 
- Define the Color Thresholds
- Detecting Blobs 
- Toggling LEDs

```
# blob_detector - By: george - Thu Aug 18 2022

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

# Define the min/max LAB values we're looking for
digital_section = (43, 100, -32, 17, -40, 42)


ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led


clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    #print(clock.fps())
    blobs = img.find_blobs([digital_section], area_threshold=5000, merge=True)


    for blob in blobs:
        # Draw a rectangle where the blob was found
        img.draw_rectangle(blob.rect(), color=(0,255,0))
        # Draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))


         # Turn on green LED if a blob was found
        if len(blobs) > 0:
            ledGreen.on()
            ledRed.off()
        else:
        # Turn the red LED on if no blob was found
            ledGreen.off()
            ledRed.on()

        pyb.delay(50) # Pauses the execution for 50ms
        print(clock.fps()) # Prints the framerate to the serial console

```


- [Blob Detection with OpenMV](https://docs.arduino.cc/tutorials/nicla-vision/blob-detection#blob-detection)
- [Find color blocks](https://book.openmv.cc/image/blob.html)