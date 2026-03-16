class Product:
    def __init__(
        self, id, name, category,
        unit_weight=None, price_per_unit=None, price_per_gram=None,
        vision_profile=None, shape_profile=None
    ):
        self.id = id
        self.name = name
        self.category = category
        self.unit_weight = unit_weight
        self.price_per_unit = price_per_unit
        self.price_per_gram = price_per_gram
        self.vision_profile = vision_profile or {}
        self.shape_profile = shape_profile or {}
