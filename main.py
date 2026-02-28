import time

from models.cart import Cart
from services.simulator import simulate_event
from services.event_handler import handle_event
from services.product_loader import load_products
from services.camera_real import capture_and_detect
from services.product_resolver import resolve_product_by_weight
from services.vision_mapper import map_color_to_categories
from services.weight_provider import WeightProvider
from ui.smart_cart_ui import SmartCartUI


# ---------------- DEBUG PRINTER ----------------
def print_debug_info(
    weight_delta,
    detected_colors,
    vision_conf,
    aspect_ratio,
    area_ratio,
    candidate_categories,
    product=None
):

    print("\n==============================")
    print(" SMART CART EVENT PIPELINE")
    print("==============================")

    print(f"Weight delta: {weight_delta} g")
    print(f"Detected colors: {detected_colors}")
    if aspect_ratio:
        print(f"Aspect ratio: {aspect_ratio:.2f}")

    if area_ratio:
        print(f"Area ratio: {area_ratio:.3f}")

    print(f"Candidate categories: {candidate_categories}")

    if product:
        diff = abs(product.unit_weight - abs(weight_delta))
        print("\nResolver result:")
        print(f"Matched product: {product.name}")
        print(f"Expected weight: {product.unit_weight} g")
        print(f"Weight difference: {diff} g")
    else:
        print("\nResolver result: ❌ NO MATCH")

    print("==============================\n")


# ---------------- STABILIZATION ----------------
def wait_for_weight_stabilization():
    """
    Simulates load cell stabilization time.
    In real system: checks variance of readings.
    """
    print("⏳ Waiting for weight to stabilize...")
    time.sleep(1.5)


# ---------------- LOAD SYSTEM ----------------
products = load_products()
cart = Cart()
weight_provider = WeightProvider(use_keyboard=True)

running = True


def shutdown_backend():
    """
    Called by UI (End Demo / Exit Gate success).
    """
    global running
    running = False
    print("🛑 Shutdown signal received from UI")


ui = SmartCartUI(cart, on_shutdown=shutdown_backend)


# ---------------- PIPELINE STEP ----------------
def pipeline_step():
    global running

    if not running:
        print("🔚 Backend shutdown complete")
        return

    print("\n🔔 Waiting for next cart event...")

    try:
        if not running:
            return

        # 1️⃣ Weight trigger
        weight_delta = weight_provider.get_next_weight()

    except StopIteration:
        print("🔚 Weight input ended")
        return

    # 2️⃣ Noise filter
    if abs(weight_delta) < 5:
        print("⚠️ Noise ignored")
        ui.after(150, pipeline_step)
        return

    # 3️⃣ Stabilization
    wait_for_weight_stabilization()

    # 4️⃣ Event type
    event_type = "ADD" if weight_delta > 0 else "REMOVE"

    # 5️⃣ Camera capture
    detected_colors, vision_conf, aspect_ratio, area_ratio, frame = capture_and_detect()
    ui.update_frame(frame)

    # 6️⃣ Vision reject
    if detected_colors is None:
        print("❌ Vision failed to detect color")
        ui.update_event("REJECT", vision_conf)
        ui.refresh()
        ui.after(200, pipeline_step)
        return

    if vision_conf < 0.15:
        print(f"⚠️ Low vision confidence ({vision_conf:.2f}) — continuing for demo")

    # 7️⃣ Color → category mapping
    candidate_categories = []

    for color in detected_colors:
        candidate_categories.extend(map_color_to_categories(color))

    candidate_categories = list(set(candidate_categories))

    print(f"Color '{detected_colors}' mapped to categories: {candidate_categories}")

    if not candidate_categories:
        print("❌ No matching category")
        ui.update_event("REJECT", vision_conf)
        ui.refresh()
        ui.after(200, pipeline_step)
        return

    # ---------------- ADD FLOW ----------------
    if event_type == "ADD":

        product = resolve_product_by_weight(
            products,
            candidate_categories,
            weight_delta,
            detected_colors,
            aspect_ratio,
            area_ratio
        )

        # Print full pipeline debug
        print_debug_info(
            weight_delta,
            detected_colors,
            vision_conf,
            aspect_ratio,
            area_ratio,
            candidate_categories,
            product
        )

        if not product:
            print("⚠️ No product matched for detected category + weight")
            ui.update_event("REJECT_MATCH", vision_conf)
            ui.refresh()
            ui.after(200, pipeline_step)
            return
        if ui.view_mode != "CART":
            ui.after(200, pipeline_step)
            return

        event = simulate_event(
            event_type="ADD",
            product_id=product.id,
            weight_delta=weight_delta,
            confidence=vision_conf
        )

        handle_event(cart, product, event)

        ui.update_event("ADD", vision_conf, product.name)
        ui.refresh()

    # ---------------- REMOVE FLOW ----------------
    else:

        print_debug_info(
            weight_delta,
            detected_colors,
            vision_conf,
            aspect_ratio,
            area_ratio,
            candidate_categories,
            None
        )

        if ui.view_mode != "CART":
            ui.after(200, pipeline_step)
            return

        event = simulate_event(
            event_type="REMOVE",
            product_id=None,
            weight_delta=weight_delta,
            confidence=vision_conf
        )

        handle_event(cart, None, event)

        ui.update_event("REMOVE", vision_conf, "item")
        ui.refresh()

    # 7️⃣ Schedule next cycle
    ui.after(200, pipeline_step)


# ---------------- START SYSTEM ----------------
print("\n=== SMART CART PIPELINE MODE START ===\n")

ui.after(500, pipeline_step)
ui.mainloop()

print("\n=== DEMO END ===")