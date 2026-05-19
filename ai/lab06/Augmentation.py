import numpy as np
import cv2


class Augmentation:
    def __init__(self, img: np.ndarray):
        if img is None:
            raise ValueError("img is None")
        if not isinstance(img, np.ndarray):
            raise TypeError("img must be numpy.ndarray")
        self.img = img.copy()

    def _get_rng(self, seed=None):
        return np.random.default_rng(seed)

    def rotate(self, img, rng, angle_range=(-25, 25)):
        h, w = img.shape[:2]
        angle = rng.uniform(*angle_range)
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    def flip(self, img, rng):
        flip_code = rng.choice([-1, 0, 1])
        return cv2.flip(img, flip_code)

    def brightness(self, img, rng, alpha_range=(0.8, 1.2), beta_range=(-30, 30)):
        alpha = rng.uniform(*alpha_range)
        beta = rng.integers(beta_range[0], beta_range[1] + 1)
        return cv2.convertScaleAbs(img, alpha=alpha, beta=int(beta))

    def gaussian_noise(self, img, rng, sigma_range=(5, 20)):
        sigma = rng.uniform(*sigma_range)
        noise = rng.normal(0, sigma, img.shape).astype(np.float32)
        noisy = img.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)

    def blur(self, img, rng, kernels=(3, 5)):
        k = int(rng.choice(kernels))
        return cv2.GaussianBlur(img, (k, k), 0)

    def scale(self, img, rng, scale_range=(0.8, 1.2)):
        h, w = img.shape[:2]
        scale = rng.uniform(*scale_range)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))

        resized = cv2.resize(img, (new_w, new_h))

        if scale >= 1.0:
            start_x = (new_w - w) // 2
            start_y = (new_h - h) // 2
            return resized[start_y:start_y + h, start_x:start_x + w]
        else:
            canvas = np.zeros_like(img)
            start_x = (w - new_w) // 2
            start_y = (h - new_h) // 2
            canvas[start_y:start_y + new_h, start_x:start_x + new_w] = resized
            return canvas

    def translate(self, img, rng, shift_ratio=0.15):
        h, w = img.shape[:2]
        tx = int(rng.uniform(-shift_ratio, shift_ratio) * w)
        ty = int(rng.uniform(-shift_ratio, shift_ratio) * h)
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    def augment_one(self, methods=None, seed=None):
        rng = self._get_rng(seed)
        img = self.img.copy()

        available = {
            "rotate": self.rotate,
            "flip": self.flip,
            "brightness": self.brightness,
            "gaussian_noise": self.gaussian_noise,
            "blur": self.blur,
            "scale": self.scale,
            "translate": self.translate,
        }

        if methods is None:
            methods = list(available.keys())

        unknown = [m for m in methods if m not in available]
        if unknown:
            raise ValueError(f"Unknown methods: {unknown}")

        count = int(rng.integers(1, len(methods) + 1))
        chosen = rng.choice(methods, size=count, replace=False)

        for method_name in chosen:
            img = available[method_name](img, rng)

        return img

    def generate(self, n=1, seed=None, methods=None):
        rng = self._get_rng(seed)
        result = []

        for _ in range(n):
            child_seed = int(rng.integers(0, 1_000_000_000))
            aug_img = self.augment_one(methods=methods, seed=child_seed)
            result.append(aug_img)

        return result