
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid
import argparse
path = "raw/"
ouput = "cropped"

digits_before = 4
digit_after = 2

parser = argparse.ArgumentParser()
parser.parse_args()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process command line arguments.')
    parser.add_argument('-path', type=dir_path)
    parser.add_argument('-output', type=dir_path)
    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid path")


def cropped():
    print("Hello world")
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


def main():
    parsed_args = parse_arguments()
    cropped()


if __name__ == "__main__":
    main()
