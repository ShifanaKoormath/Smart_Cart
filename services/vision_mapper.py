COLOR_TO_CATEGORY = {
    "orange": ["toiletries", "snacks"],
    "yellow": ["snacks"],
    "blue": ["toiletries"],
    "red": ["snacks", "beverages"],
    "white": ["grains", "dairy"],
    "green": ["beverages", "toiletries"]
}

def map_color_to_categories(detected_color):
    return COLOR_TO_CATEGORY.get(detected_color, [])
