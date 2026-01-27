class WeightProvider:
    """
    Provides weight deltas for add/remove events.

    CURRENT MODES:
    - Predefined demo weights (scripted demo)
    - Live keyboard input (manual simulation)

    ============================================================
    WHEN INTEGRATING REAL WEIGHT SENSOR (IMPORTANT GUIDE)
    ============================================================

    Hardware expected:
    - Load cell (5kg / 10kg)
    - HX711 amplifier
    - Microcontroller (Arduino / ESP32 / Raspberry Pi Pico)

    Steps to integrate real hardware:

    1️⃣ Hardware wiring (outside Python):
       - Load cell -> HX711
       - HX711 -> Microcontroller
       - Microcontroller -> PC via USB (Serial)

    2️⃣ Microcontroller responsibility:
       - Continuously read load cell values
       - Compute WEIGHT DELTA (difference from last stable weight)
       - Send ONLY the delta value via Serial
         Example serial output:
           +125
           -120

    3️⃣ Python changes (THIS FILE ONLY):
       - Import `serial`
       - Initialize serial port in __init__()
       - Read weight delta from serial in get_next_weight()
       - Ignore noise using a small threshold (e.g. < 5g)

    4️⃣ DO NOT modify:
       - main.py
       - resolver logic
       - cart logic

    This abstraction ensures hardware can be added
    without touching business logic.
    ============================================================
    """

    def __init__(self, demo_weights=None, use_keyboard=False):
        self.demo_weights = demo_weights or []
        self.use_keyboard = use_keyboard
        self.index = 0

        # ---------------- REAL SENSOR SETUP (TO ENABLE LATER) ----------------
        # Uncomment and configure ONLY when real hardware is connected.
        #
        # import serial
        # self.ser = serial.Serial(
        #     port="COM3",          # Windows example (Linux: /dev/ttyUSB0)
        #     baudrate=9600,
        #     timeout=1
        # )
        #
        # The microcontroller must send weight DELTA values as plain text.
        # ---------------------------------------------------------------------

    def get_next_weight(self):
        """
        Returns the next weight delta.
        Positive value  -> ADD product
        Negative value  -> REMOVE product
        """

        # ---------------- REAL SENSOR MODE ----------------
        # Enable this block ONLY after hardware integration.
        #
        # try:
        #     line = self.ser.readline().decode().strip()
        #     weight = float(line)
        #
        #     # Ignore sensor noise / vibrations
        #     if abs(weight) < 5:
        #         return self.get_next_weight()
        #
        #     return weight
        # except Exception:
        #     print("⚠️ Sensor read error")
        #     return None
        # ---------------------------------------------------

        # ---------------- KEYBOARD SIMULATION MODE ----------------
        if self.use_keyboard:
            return self._get_weight_from_keyboard()

        # ---------------- SCRIPTED DEMO MODE ----------------
        if self.index >= len(self.demo_weights):
            raise StopIteration("No more simulated weight inputs")

        weight = self.demo_weights[self.index]
        self.index += 1
        return weight

    def _get_weight_from_keyboard(self):
        """
        Manual weight input for demo/testing.
        This simulates real-time weight changes.
        """

        while True:
            try:
                val = input(
                    "Enter weight change (e.g. 125, -120) or 'q' to quit: "
                )

                if val.lower() == "q":
                    raise StopIteration("User ended input")

                weight = float(val)

                if weight == 0:
                    print("⚠️ Weight cannot be zero")
                    continue

                return weight

            except ValueError:
                print("❌ Invalid input. Enter a number like 125 or -125.")
