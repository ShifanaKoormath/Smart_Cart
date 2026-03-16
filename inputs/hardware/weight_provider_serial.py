import serial
import time


class WeightProvider:

    def __init__(self, port="COM4", baudrate=9600):

        print(f"🔌 Connecting to weight sensor on {port}...")

        self.ser = serial.Serial(port, baudrate, timeout=1)

        # Allow Arduino to reset after serial connection
        time.sleep(2)

        print("✅ Hardware weight provider active")

    def get_next_weight(self):

        while True:

            try:
                line = self.ser.readline().decode(errors="ignore").strip()

                if not line:
                    continue

                # Ignore startup messages
                if "Ready" in line:
                    continue

                # Debug print
                print(f"📡 Serial received: {line}")

                if line.startswith("ADD:"):
                    weight = float(line.split(":")[1])
                    return weight

                if line.startswith("REMOVE:"):
                    weight = float(line.split(":")[1])
                    return -weight

            except Exception as e:
                print(f"⚠️ Serial read error: {e}")
                continue