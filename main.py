from models.cart import Cart
from services.simulator import simulate_event
from services.event_handler import handle_event
from services.product_loader import load_products
from services.camera_real import capture_and_detect
from services.product_resolver import resolve_product_by_weight
from services.vision_mapper import map_color_to_categories
from services.weight_provider import WeightProvider

# Load product catalog (supports 10–15 products)
products = load_products()
cart = Cart()


weight_provider = WeightProvider(use_keyboard=True)



# -------- ADD FLOW (Camera + Vision) --------

print("\n=== SMART CART DEMO START ===\n")

for i in range(3):
    print(f"\n[EVENT {i+1}] Camera scan")

    detected_color, vision_conf, aspect_ratio, area_ratio = capture_and_detect()

    print(f"Shape: aspect={aspect_ratio}, area={area_ratio}")

    if detected_color is None or vision_conf < 0.3:
        print("❌ Vision unreliable, event rejected")
        continue

    candidate_categories = map_color_to_categories(detected_color)

    if not candidate_categories:
        print("❌ No matching category")
        continue
    try:
        simulated_weight = weight_provider.get_next_weight()
    except StopIteration:
        print("🔚 Weight input ended")
        break

    # 🔑 THIS IS WHERE WE USE WEIGHT AS DECISION MAKER
    product = resolve_product_by_weight(
    products,
    candidate_categories,
    simulated_weight,
    aspect_ratio,
    area_ratio
)


    if not product:
        print("⚠️ Weight mismatch, product not resolved")
        continue

    event = simulate_event(
        event_type="ADD",
        product_id=product.id,
        weight_delta=simulated_weight,
        confidence=vision_conf
    )

    handle_event(cart, product, event)
    cart.print_receipt()

# -------- REMOVE FLOW (Weight-based inference) --------
print("\n[EVENT 4] Product removed from cart")

remove_event = simulate_event(
    event_type="REMOVE",
    product_id=None,
    weight_delta=-120,   # simulated weight drop
    confidence=0.95
)

handle_event(cart, None, remove_event)
cart.print_receipt()

print("\n=== DEMO END ===")
