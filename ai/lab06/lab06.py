import os
import numpy as np
import cv2
import Augmentation

os.makedirs('src/aug', exist_ok=True)
os.makedirs('src/aug_mask', exist_ok=True)
os.makedirs('src/aug_grab_mask', exist_ok=True)

img_bgr = cv2.imread('heli.jpg')
if img_bgr is None:
    raise ValueError("Не удалось загрузить heli.jpg")

img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])
mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)

mask = mask1 + mask2

kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(mask, kernel, iterations=1)
mask = cv2.dilate(erosion, kernel, iterations=1)

grab_mask = np.full(img_bgr.shape[:2], cv2.GC_PR_BGD, dtype=np.uint8)
grab_mask[mask == 255] = cv2.GC_PR_FGD

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

cv2.grabCut(img_bgr, grab_mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

grab_mask_final = np.where(
    (grab_mask == cv2.GC_FGD) | (grab_mask == cv2.GC_PR_FGD),
    255,
    0
).astype('uint8')

aug = Augmentation.Augmentation(img_bgr)
aug_mask = Augmentation.Augmentation(mask)
aug_grab_mask = Augmentation.Augmentation(grab_mask_final)

aug_result = aug.generate(50, seed=42)
aug_mask_result = aug_mask.generate(50, seed=42)
aug_grab_mask_result = aug_grab_mask.generate(50, seed=42)

for i, img in enumerate(aug_result):
    cv2.imwrite(f'src/aug/augmented_{i}.jpg', img)

for i, img in enumerate(aug_mask_result):
    cv2.imwrite(f'src/aug_mask/augmented_{i}.jpg', img)

for i, img in enumerate(aug_grab_mask_result):
    cv2.imwrite(f'src/aug_grab_mask/augmented_{i}.jpg', img)