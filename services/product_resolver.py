def resolve_product_by_weight(
    products,
    candidate_categories,
    weight_delta,
    aspect_ratio=None,
    area_ratio=None,
    tolerance=20
):
    target = abs(weight_delta)
    best_match = None
    min_diff = float("inf")

    for product in products.values():
        if product.category not in candidate_categories:
            continue

        if product.unit_weight is None:
            continue

        # ---- SHAPE FILTER (soft) ----
        shape = product.shape_profile
        if shape and aspect_ratio and area_ratio:
            ar_min, ar_max = shape.get("aspect_ratio", (0, 10))
            min_area = shape.get("min_area_ratio", 0)

            if not (ar_min <= aspect_ratio <= ar_max):
                continue
            if area_ratio < min_area:
                continue

        diff = abs(product.unit_weight - target)

        if diff < min_diff and diff <= tolerance:
            min_diff = diff
            best_match = product

    return best_match
