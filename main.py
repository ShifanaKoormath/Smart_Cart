from models.cart import Cart
from services.simulator import simulate_event
from services.event_handler import handle_event
from services.product_loader import load_products
from services.camera_real import capture_and_detect
from services.product_resolver import resolve_product_by_weight
from services.vision_mapper import map_color_to_categories
from services.weight_provider import WeightProvider
from ui.smart_cart_ui import SmartCartUI

# Load product catalog
products = load_products()
cart = Cart()
ui = SmartCartUI(cart)

weight_provider = WeightProvider(use_keyboard=True)

print("\n=== SMART CART DEMO START ===\n")

# -------- ADD FLOW --------
for i in range(3):
    print(f"\n[EVENT {i+1}] Camera scan")

    detected_color, vision_conf, aspect_ratio, area_ratio, frame = capture_and_detect()
    ui.update_frame(frame)

    print(f"Shape: aspect={aspect_ratio}, area={area_ratio}")

    if detected_color is None or vision_conf < 0.3:
        print("❌ Vision unreliable, event rejected")
        ui.update_event("REJECT", vision_conf)
        ui.refresh()
        continue

    candidate_categories = map_color_to_categories(detected_color)

    if not candidate_categories:
        print("❌ No matching category")
        ui.update_event("REJECT", vision_conf)
        ui.refresh()
        continue

    try:
        simulated_weight = weight_provider.get_next_weight()
    except StopIteration:
        print("🔚 Weight input ended")
        break

    product = resolve_product_by_weight(
        products,
        candidate_categories,
        simulated_weight,
        aspect_ratio,
        area_ratio
    )

    if not product:
        print("⚠️ Weight mismatch, product not resolved")
        ui.update_event("REJECT", vision_conf)
        ui.refresh()
        continue

    event = simulate_event(
        event_type="ADD",
        product_id=product.id,
        weight_delta=simulated_weight,
        confidence=vision_conf
    )

    handle_event(cart, product, event)
    ui.update_event(
        "ADD",
        event["confidence"],
        product_name=product.name
    )
    ui.refresh()

# -------- REMOVE FLOW --------
print("\n[EVENT 4] Product removed from cart")

remove_event = simulate_event(
    event_type="REMOVE",
    product_id=None,
    weight_delta=-120,
    confidence=0.95
)

handle_event(cart, None, remove_event)
ui.update_event(
    "REMOVE",
    remove_event["confidence"],
    product_name="item"
)
ui.refresh()

print("\n=== DEMO END ===")

ui.show_final_bill()
ui.mainloop()
