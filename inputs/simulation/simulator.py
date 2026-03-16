def simulate_event(event_type, product_id, weight_delta, confidence=0.95):
    return {
        "event_type": event_type,
        "product_id": product_id,
        "weight_delta": weight_delta,
        "confidence": confidence
    }
