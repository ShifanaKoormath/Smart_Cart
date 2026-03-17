def resolve_product_by_weight(
    products,
    candidate_categories,
    weight_delta,
    detected_colors,
    aspect_ratio=None,
    area_ratio=None
):
    target = abs(weight_delta)
    tolerance = 5

    candidates = []

    # -------- PRIMARY FILTER --------
    for product in products.values():

        if product.category not in candidate_categories:
            continue

        if product.unit_weight is None:
            continue

        palette = product.vision_profile.get("dominant_colors", [])

        if not any(c in palette for c in detected_colors):
            continue

        diff = abs(product.unit_weight - target)

        if diff <= tolerance:
            candidates.append((product, diff))

    # -------- FALLBACK --------
    if not candidates:

        print("⚠️ Color mismatch — fallback")

        for product in products.values():

            if product.category not in candidate_categories:
                continue

            diff = abs(product.unit_weight - target)

            if diff <= tolerance:
                candidates.append((product, diff))

    candidates.sort(key=lambda x: x[1])

    return [c[0] for c in candidates]