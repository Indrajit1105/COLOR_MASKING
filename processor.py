import cv2
import numpy as np
import re

img_path = "static/bag.jpg"
original = cv2.imread(img_path)
original = cv2.resize(original, (700, 500))

def get_bag_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    return cv2.bitwise_or(mask1, mask2)

def recolor_bag(color_bgr):
    mask = get_bag_mask(original)

    color_img = np.full(original.shape, color_bgr, dtype=np.uint8)
    recolored = cv2.bitwise_and(color_img, color_img, mask=mask)
    background = cv2.bitwise_and(original, original, mask=cv2.bitwise_not(mask))
    final = cv2.add(recolored, background)
    return final

def save_custom_color_image(color_bgr, save_path):
    img = recolor_bag(color_bgr)
    cv2.imwrite(save_path, img)

def hex_to_bgr(hex_color):
    # Strip leading "#" if present and check if it's a valid hex
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", hex_color.strip())
    if not match:
        raise ValueError("Invalid color format. Please use hex like #ff0000.")
    hex_clean = match.group(1)
    r, g, b = (int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
    return (b, g, r)  # Convert RGB to BGR for OpenCV