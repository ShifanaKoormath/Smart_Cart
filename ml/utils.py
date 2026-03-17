COLOR_MAP = {
    "orange": 1,
    "yellow": 2,
    "blue": 3,
    "green": 4,
    "red": 5,
    "purple": 6,
    "black": 7,
    "white": 8
}

def extract_ml_features(weight, aspect_ratio, area_ratio, dominant_color):
    return {
        "weight": weight,
        "aspect_ratio": aspect_ratio if aspect_ratio else 0,
        "area_ratio": area_ratio if area_ratio else 0,
        "color_code": COLOR_MAP.get(dominant_color, 0)
    }