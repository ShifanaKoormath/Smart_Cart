import cv2
import numpy as np
import time


def capture_and_detect():
    """
    Captures an image from webcam, extracts dominant color
    using filtered HSV pixels.
    Returns (detected_color, confidence)
    """

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return None, 0.0

    # Camera warm-up
    time.sleep(1)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Failed to capture image")
        return None, 0.0

    h, w, _ = frame.shape

    # ---- CENTER CROP (fixed region) ----
    crop = frame[
        int(h * 0.25):int(h * 0.75),
        int(w * 0.25):int(w * 0.75)
    ]

    cv2.imwrite("last_capture.jpg", crop)
    print("📷 Image captured and cropped")

    # ---- HSV CONVERSION ----
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # ---- FILTER PIXELS ----
    # Ignore white text, dark regions, background noise
    mask = (hsv[:, :, 1] > 50) & (hsv[:, :, 2] > 80)
    filtered_pixels = hsv[mask]

    # If too few useful pixels, reject
    if len(filtered_pixels) < 100:
        return None, 0.0

    # Compute average HSV of filtered pixels
    h_val, s_val, v_val = np.mean(filtered_pixels, axis=0)

    detected_color = classify_color(h_val, s_val, v_val)
    confidence = compute_confidence(s_val, v_val)
    aspect_ratio, area_ratio = extract_shape_features(crop)

    return detected_color, confidence, aspect_ratio, area_ratio, crop


def classify_color(h, s, v):
    """
    Coarse HSV-based color classification.
    Brown / dark colors are treated as ambiguous.
    """

    # Too dark
    if v < 50:
        return None

    # Brown / dark orange → ambiguous (reject)
    if (10 <= h <= 40) and v < 120:
        return None

    # White / very light packaging
    if s < 40 and v > 150:
        return "white"

    # Hue-based classification
    if h < 10 or h > 160:
        return "red"
    elif 10 <= h < 35:
        return "orange"
    elif 35 <= h < 45:
        return "yellow"
    elif 45 <= h < 85:
        return "green"
    elif 85 <= h < 130:
        return "blue"

    return None
def extract_shape_features(crop):
    """
    Extract very basic shape features from the cropped image.
    Returns aspect_ratio and area_ratio.
    """

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None, None

    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)

    crop_area = crop.shape[0] * crop.shape[1]
    object_area = cv2.contourArea(largest)

    aspect_ratio = w / h if h != 0 else 0
    area_ratio = object_area / crop_area

    return aspect_ratio, area_ratio


def compute_confidence(s, v):
    """
    Confidence based on saturation and brightness.
    Slight boost added for indoor lighting calibration.
    """
    confidence = (s / 255 + v / 255) / 2 + 0.15
    return round(min(1.0, confidence), 2)
