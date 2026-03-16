CONFIDENCE_THRESHOLD = 0.5

def handle_event(cart, product, event):
    print(f"🔍 Event confidence: {event['confidence']}")

    if event["confidence"] < CONFIDENCE_THRESHOLD:
        print("⚠️ Low confidence event ignored")
        return

    if event["event_type"] == "ADD":
        print(f"➕ ADD detected (Product ID: {product.id})")
        cart.add(product, event["weight_delta"])

    elif event["event_type"] == "REMOVE":
        print(f"➖ REMOVE detected (Weight change: {event['weight_delta']}g)")
        cart.remove_by_weight(event["weight_delta"])
