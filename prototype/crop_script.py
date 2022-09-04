
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid
path = "raw/"

digits_before = 4
digit_after = 2

for file in os.listdir(path):
    image_transform = cv2.imread(path + file, cv2.IMREAD_GRAYSCALE)
    print(image_transform)

    # Before dp
    for digit in range(digits_before):
        if digit >= 0:
            if digit == 3 or digit == 4:
                continue
            initial_x = 44
            x = initial_x + digit*15
            y = 15
            w = 15
            h = 25
            gen = str(uuid.uuid4())
            cropped = image_transform
            cropped = cropped[y:y+h, x:x+w]
            cv2.imwrite(f'cropped2/{digit}_{gen}.png', cropped)
            plt.imshow(cropped)
            plt.show()

    # After dp
    for digit in range(digit_after):
        if digit >= 0:
            initial_x = 86
            x = initial_x + digit*15
            y = 15
            w = 15
            h = 25
            gen = str(uuid.uuid4())
            cropped = image_transform
            cropped = cropped[y:y+h, x:x+w]
            cv2.imwrite(f'cropped2/{digit}_{gen}.png', cropped)
            plt.imshow(cropped)
            plt.show()
