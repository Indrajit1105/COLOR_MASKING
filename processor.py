# processor.py

import cv2
import numpy as np

img_path = "static/img.jpeg"
original = cv2.imread(img_path)
original = cv2.resize(original, (500, 700))

color_map = {
    "Blue": (255, 0, 0),
    "Green": (0, 255, 0),
    "Yellow": (0, 255, 255),
    "Purple": (255, 0, 255),
    "White": (255, 255, 255),
    "Black": (20, 20, 20),
}

def get_color_options():
    return list(color_map.keys())

def get_bag_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    return cv2.bitwise_or(mask1, mask2)

def recolor_bag(color_name):
    color_bgr = color_map[color_name]
    mask = get_bag_mask(original)

    color_img = np.full(original.shape, color_bgr, dtype=np.uint8)
    recolored = cv2.bitwise_and(color_img, color_img, mask=mask)
    background = cv2.bitwise_and(original, original, mask=cv2.bitwise_not(mask))
    final = cv2.add(recolored, background)
    return final

def save_recolored_image(color_name, save_path):
    img = recolor_bag(color_name)
    cv2.imwrite(save_path, img)
