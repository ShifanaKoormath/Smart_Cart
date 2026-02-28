COLOR_TO_CATEGORY = {

    "orange": ["toiletries", "beverages", "snacks"],

    "red": ["toiletries", "snacks"],

    "blue": [
        "household",
        "stationery",
        "toiletries"
    ],

    "yellow": [
        "snacks",
        "groceries",
        "stationery"
    ],

    "green": [
        "groceries",
        "snacks"
    ],

    "white": [
        "dairy",
        "stationery",
        "toiletries"
    ],

    "purple": [
        "snacks"
    ],

    "black": [
        "stationery",
        "toiletries"

    ]
}


def map_color_to_categories(detected_color):
    return COLOR_TO_CATEGORY.get(detected_color, [])