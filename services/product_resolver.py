def resolve_product_by_weight(
    products,
    candidate_categories,
    weight_delta,
    detected_colors,
    aspect_ratio=None,
    area_ratio=None
):
    target = abs(weight_delta)
    tolerance = 5  # small tolerance for demo stability

    best_product = None
    smallest_diff = float("inf")

    # -------- PRIMARY SEARCH (category + color + weight) --------
    for product in products.values():

        if product.category not in candidate_categories:
            continue

        if product.unit_weight is None:
            continue

        # palette check
        palette = product.vision_profile.get("dominant_colors", [])

        if not any(c in palette for c in detected_colors):
            continue

        diff = abs(product.unit_weight - target)

        if diff <= tolerance and diff < smallest_diff:
            smallest_diff = diff
            best_product = product

    # -------- FALLBACK SEARCH (ignore color but keep category) --------
    if best_product is None:

        print("⚠️ Color mismatch — trying category + weight fallback")

        for product in products.values():

            if product.category not in candidate_categories:
                continue

            diff = abs(product.unit_weight - target)

            if diff <= tolerance and diff < smallest_diff:
                smallest_diff = diff
                best_product = product

    return best_product