from models.cart_item import CartItem

class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product, weight):
        if product.id not in self.items:
            self.items[product.id] = CartItem(product)

        item = self.items[product.id]

        if product.price_per_unit is not None:
            item.quantity += 1
        else:
            item.weight += weight

        item.update_subtotal()

    def remove_by_weight(self, weight_delta):
        if not self.items:
            return

        target_weight = abs(weight_delta)
        closest_item = None
        min_diff = float("inf")

        for item in self.items.values():
            if item.product.unit_weight is not None:
                diff = abs(item.product.unit_weight - target_weight)
                if diff < min_diff:
                    min_diff = diff
                    closest_item = item

        if closest_item:
            closest_item.quantity -= 1

            if closest_item.quantity <= 0:
                del self.items[closest_item.product.id]
            else:
                closest_item.update_subtotal()

    def total(self):
        return sum(item.subtotal for item in self.items.values())
    def print_receipt(self):
        print("\n------ CART SUMMARY ------")
        if not self.items:
            print("Cart is empty")
        else:
            for item in self.items.values():
                if item.product.price_per_unit is not None:
                    print(
                        f"{item.product.name} | Qty: {item.quantity} | "
                        f"Subtotal: ₹{item.subtotal}"
                    )
                else:
                    print(
                        f"{item.product.name} | Weight: {item.weight}g | "
                        f"Subtotal: ₹{item.subtotal:.2f}"
                    )
        print("--------------------------")
        print(f"TOTAL: ₹{self.total():.2f}")
        print("--------------------------\n")
