
class CartItem:
    def __init__(self, product):
        self.product = product
        self.quantity = 0
        self.weight = 0
        self.subtotal = 0

    def update_subtotal(self):
        if self.product.price_per_unit is not None:
            self.subtotal = self.quantity * self.product.price_per_unit
        else:
            self.subtotal = self.weight * self.product.price_per_gram
