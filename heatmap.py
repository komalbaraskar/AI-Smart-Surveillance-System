import numpy as np
import cv2

heatmap = np.zeros((480, 640))

def update_heatmap(boxes):
    global heatmap

    heatmap *= 0.95

    for (l, t, r, b) in boxes:
        x = int((l + r) / 2)
        y = int((t + b) / 2)

        if 0 <= x < 640 and 0 <= y < 480:
            heatmap[y-5:y+5, x-5:x+5] += 1

    heatmap_img = cv2.applyColorMap(
        cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype('uint8'),
        cv2.COLORMAP_JET
    )

    return heatmap_img


"""
The heatmap accumulates positional data of detected people. Areas where people stay longer or move frequently become hotter (red), while less active areas remain cooler (blue).
🔵 Blue → Very low activity
🟢 Green → Moderate movement
🟡 Yellow → High movement
🔴 Red → Very high activity (important zone)"""