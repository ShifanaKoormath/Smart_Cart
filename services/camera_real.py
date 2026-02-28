import cv2
import numpy as np
import time


def capture_and_detect():
    """
    Captures an image from webcam and extracts the top 2 dominant colors.

    Returns:
    detected_colors, confidence, aspect_ratio, area_ratio, cropped_frame
    """

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return None, 0.0, None, None, None

    # Camera warm-up
    time.sleep(0.8)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Failed to capture image")
        return None, 0.0, None, None, None

    h, w, _ = frame.shape

    # ---- CENTER CROP (reduce background noise) ----
    crop = frame[
        int(h * 0.35):int(h * 0.65),
        int(w * 0.35):int(w * 0.65)
    ]

    cv2.imwrite("last_capture.jpg", crop)
    print("📷 Image captured and cropped")

    # ---- HSV CONVERSION ----
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # ---- FILTER PIXELS ----
    mask = (hsv[:, :, 1] > 30) & (hsv[:, :, 2] > 70)
    filtered_pixels = hsv[mask]

    if len(filtered_pixels) < 80:
        return None, 0.0, None, None, crop

    # -----------------------------
    # DOMINANT COLOR CLUSTERS
    # -----------------------------
    hues = filtered_pixels[:, 0]

    hist, bins = np.histogram(hues, bins=18, range=(0, 180))

    # pick top 2 bins
    top_bins = hist.argsort()[-2:][::-1]

    detected_colors = []

    s_val = np.median(filtered_pixels[:, 1])
    v_val = np.median(filtered_pixels[:, 2])

    for b in top_bins:

        h_val = (bins[b] + bins[b + 1]) / 2

        color = classify_color(h_val, s_val, v_val)

        if color and color not in detected_colors:
            detected_colors.append(color)

    confidence = compute_confidence(s_val, v_val)

    aspect_ratio, area_ratio, bbox = extract_shape_features(crop)
    
    print(f"🎨 Detected dominant colors: {detected_colors}")

    return detected_colors, confidence, aspect_ratio, area_ratio, crop


def classify_color(h, s, v):
    """
    Coarse HSV color classification.
    """

    if v < 50:
        return "black"

    if s < 35 and v > 160:
        return "white"

    if h < 10 or h > 170:
        return "red"
    elif 10 <= h < 30:
        return "orange"
    elif 30 <= h < 50:
        return "yellow"
    elif 50 <= h < 85:
        return "green"
    elif 85 <= h < 140:
        return "blue"
    elif 140 <= h < 170:
        return "purple"

    return None


def extract_shape_features(crop):
    """
    Extract shape features using edge detection.
    Returns:
    aspect_ratio, area_ratio, bbox
    """

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None, None, None

    largest = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largest)

    crop_area = crop.shape[0] * crop.shape[1]
    object_area = cv2.contourArea(largest)

    aspect_ratio = w / h if h != 0 else 0
    area_ratio = object_area / crop_area

    bbox = (x, y, w, h)

    return aspect_ratio, area_ratio, bbox

def compute_confidence(s, v):
    """
    Confidence estimation.
    """

    confidence = ((s / 255) * 0.6 + (v / 255) * 0.4) + 0.2

    return round(min(confidence, 1.0), 2)