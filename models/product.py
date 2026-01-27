class Product:
    def __init__(self, id, name, unit_weight=None, price_per_unit=None, price_per_gram=None):
        self.id = id
        self.name = name
        self.unit_weight = unit_weight
        self.price_per_unit = price_per_unit
        self.price_per_gram = price_per_gram
