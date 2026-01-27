from models.cart import Cart
from services.simulator import simulate_event
from services.event_handler import handle_event
from services.product_loader import load_products
from services.camera_stub import capture_and_detect

products = load_products()
cart = Cart()

print("\n=== SMART CART DEMO START ===\n")

# Simulate ADD via camera
for i in range(3):
    print(f"\n[EVENT {i+1}] Camera scan")
    product_id, confidence = capture_and_detect()

    if product_id is None:
        print("📷 Camera failed to detect product")
        continue

    event = simulate_event(
        event_type="ADD",
        product_id=product_id,
        weight_delta=products[product_id].unit_weight or 500,
        confidence=confidence
    )

    handle_event(cart, products[product_id], event)
    cart.print_receipt()

# Simulate REMOVE
print("\n[EVENT 4] Product removed from cart")
remove_event = simulate_event("REMOVE", None, -120)
handle_event(cart, None, remove_event)
cart.print_receipt()

print("\n=== DEMO END ===")
