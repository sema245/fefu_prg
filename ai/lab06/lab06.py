from pathlib import Path
import cv2
import numpy as np
import Augmentation

OUTS = {
    'aug': 'src/aug',
    'mask': 'src/aug_mask',
    'grab': 'src/aug_grab_mask',
}
for p in OUTS.values():
    Path(p).mkdir(parents=True, exist_ok=True)

def red_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ranges = (
        ((0, 100, 100), (10, 255, 255)),
        ((170, 100, 100), (180, 255, 255)),
    )
    mask = sum(
        cv2.inRange(hsv, np.array(lo), np.array(hi))
        for lo, hi in ranges
    )
    k = np.ones((3, 3), np.uint8)
    return cv2.dilate(cv2.erode(mask, k, 1), k, 1)

def grabcut_mask(img, mask):
    gc = np.full(img.shape[:2], cv2.GC_PR_BGD, np.uint8)
    gc[mask == 255] = cv2.GC_PR_FGD
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, gc, None, bgd, fgd, 5, cv2.GC_INIT_WITH_MASK)
    return np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)

def augment_and_save(data, dst, n=50, seed=42):
    for i, img in enumerate(Augmentation.Augmentation(data).generate(n, seed=seed)):
        cv2.imwrite(f'{dst}/augmented_{i}.jpg', img)

img = cv2.imread('heli.jpg')
if img is None:
    raise ValueError('Не удалось загрузить heli.jpg')

mask = red_mask(img)
grab = grabcut_mask(img, mask)

for key, data in {'aug': img, 'mask': mask, 'grab': grab}.items():
    augment_and_save(data, OUTS[key])