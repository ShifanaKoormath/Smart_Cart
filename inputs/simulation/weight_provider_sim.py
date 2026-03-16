class WeightProvider:
    """
    Simulation weight provider.

    Supports:
    - Live keyboard input (default)
    - Optional scripted demo weights
    """

    def __init__(self, demo_weights=None):
        self.demo_weights = demo_weights
        self.index = 0

    def get_next_weight(self):
        """
        Returns next weight delta.
        Positive -> ADD
        Negative -> REMOVE
        """

        # -------- KEYBOARD MODE (default) --------
        if self.demo_weights is None:
            return self._get_weight_from_keyboard()

        # -------- SCRIPTED DEMO MODE --------
        if self.index >= len(self.demo_weights):
            raise StopIteration("No more simulated weight inputs")

        weight = self.demo_weights[self.index]
        self.index += 1
        return weight

    def _get_weight_from_keyboard(self):
        """
        Manual weight entry for simulation.
        """

        while True:
            try:
                val = input(
                    "Enter weight change (e.g. 125, -120) or 'q' to quit: "
                ).strip()

                if val.lower() == "q":
                    raise StopIteration("User ended input")

                weight = float(val)

                if weight == 0:
                    print("⚠️ Weight cannot be zero")
                    continue

                return weight

            except ValueError:
                print("❌ Invalid input. Enter a number like 125 or -125.")