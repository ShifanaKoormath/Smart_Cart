import random

# Fake camera + detection logic
def capture_and_detect():
    """
    Simulates camera image capture and product detection.
    Returns (product_id, confidence)
    """

    detected_products = [
        ("P001", 0.92),  # Soap
        ("P002", 0.88),  # Biscuit
        ("P003", 0.95),  # Rice
        (None, 0.4)      # Failed detection
    ]

    return random.choice(detected_products)
