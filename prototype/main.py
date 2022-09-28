
import machine
import sensor
import image
import time
import os
import tf
import uos
import gc
import ulab
import ubinascii
import network
from mqtt import MQTTClient
import pyb
import lcd
import random
from time import sleep
from secret import SSID, KEY, user, password
gc.collect()

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

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
image_counter = 0

image_folder_name = "inference"+'_'
if not image_folder_name in os.listdir():
    os.mkdir(image_folder_name)
    print(f"directory {image_folder_name} created")

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat(
        'trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception(
        'Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception(
        'Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')


# Init wlan module and connect to network
print("Trying to connect. Note this may take a while...")

wlan = network.WLAN(network.STA_IF)
# wlan.deinit()
wlan.active(True)
wlan.connect(SSID, KEY, security=wlan.WPA_PSK)

# We should have a valid IP now via DHCP
print("WiFi Connected ", wlan.ifconfig())

client = MQTTClient("openmv", "io.adafruit.com", user=user,
                    password=password, port=1883)
client.connect()


def grab_roi(img_full):
    """
    -----
    img_full:
    cropped_numbers:
    return:
    """
    img_full_copy1 = img_full.copy()
    img_full_copy2 = img_full.copy()
    img_full_copy3 = img_full.copy()
    img_full_copy4 = img_full.copy()
    img_full_copy5 = img_full.copy()
    #initial_digit_position = 48
    x = 48
    y = 15
    w_ = 15
    h_ = 25
    cropped1 = img_full_copy1.crop(roi=(x, y, w_, h_))
    cropped2 = img_full_copy2.crop(roi=(x+15, y, w_, h_))
    cropped3 = img_full_copy3.crop(roi=(x+30, y, w_, h_))
    cropped4 = img_full_copy4.crop(roi=(x+43, y, w_, h_))
    cropped5 = img_full_copy5.crop(roi=(x+43+15, y, w_, h_))
    cropped_numbers = [cropped1, cropped2, cropped3, cropped4, cropped5]
    return cropped_numbers


def compress_image(normal_img):
    """
    -----
    img_full:
    img_t:
    return:
    """
    normal_img.compress(quality=90)
    img_bytes = ubinascii.b2a_base64(normal_img)
    img_t = img_bytes.decode("utf-8")  # compressed_img is a string
    compressed_img = img_t.strip()
    print(compressed_img)
    return compressed_img


def inference(cropped_numbers):
    """
    -----
    number_list:
    multiple_text:
    return:
    """
    number = ""

    for i in cropped_numbers:
        # default settings just do one detection... change them to search the image...
        scaled = i.scale(x_size=23, y_size=23, copy=True)
        for obj in net.classify(scaled, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
            #print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
            # This combines the labels and confidence values into a list of tuples
            predictions_list = list(zip(labels, obj.output()))
            print(f"{scaled}:{predictions_list}")
            # Convert the output to array
            obj_arr = ulab.numpy.array(obj.output())
            # Get the position of the max. value
            obj_arg = ulab.numpy.argmax(obj_arr)
            number += str(obj_arg)
    text = f"{number[:3]}.{number[-2:]}"
    print(text)
    return text


while (True):
    image_counter += 1
    img_full = sensor.snapshot()
    image_file_name = "Img"+'_' + \
        str(image_counter)+'_'+str(time.mktime(time.gmtime()))
    img_full.crop(roi=(x1_v, y1_v, w, h))
    img_full.save(str(image_folder_name)+'/'+str(image_file_name), quality=100)
    print(img_full)
    cropped_numbers = grab_roi(img_full)
    multiple_text = inference(cropped_numbers)
    img_t = compress_image(img_full)

    # replace Adafruit IO user with your Adafruit IO user
    #client.publish("igeorge/feeds/reading", i_t)
    client.publish("igeorge/feeds/unit", str(multiple_text))
    client.publish("igeorge/feeds/openmv", img_t)

    files_path = [x for x in os.listdir(image_folder_name) if x[0] != "."]
    print(f"number of image saved: {len(files_path)}")
    time.sleep(10)  # lower values will exceed Adafruit IO requirements
