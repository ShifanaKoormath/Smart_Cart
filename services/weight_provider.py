class WeightProvider:
    """
    Provides weight deltas for add/remove events.
    Supports:
    - predefined demo weights
    - live keyboard input (for demo/testing)
    """

    def __init__(self, demo_weights=None, use_keyboard=False):
        self.demo_weights = demo_weights or []
        self.use_keyboard = use_keyboard
        self.index = 0

    def get_next_weight(self):
        if self.use_keyboard:
            return self._get_weight_from_keyboard()

        if self.index >= len(self.demo_weights):
            raise StopIteration("No more simulated weight inputs")

        weight = self.demo_weights[self.index]
        self.index += 1
        return weight

    def _get_weight_from_keyboard(self):
        while True:
            try:
                val = input("Enter weight change (e.g. 125, -120) or 'q' to quit: ")
                if val.lower() == "q":
                    raise StopIteration("User ended input")

                weight = float(val)
                if weight == 0:
                    print("⚠️ Weight cannot be zero")
                    continue

                return weight
            except ValueError:
                print("❌ Invalid input. Enter a number like 125 or -125.")
