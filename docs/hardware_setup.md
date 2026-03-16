# 🔧 Smart Cart Hardware Debugging Guide

This document helps diagnose **common hardware problems** when integrating the Smart Cart System with a **load cell + HX711 amplifier + microcontroller**.

If the system does not work as expected, follow these checks **in order**.

---

# 1️⃣ Debugging Strategy (Always Follow This Order)

When troubleshooting remotely, **never debug everything at once**.

Use this step-by-step pipeline:

```
Hardware Wiring
      ↓
Arduino Firmware
      ↓
Arduino Serial Monitor
      ↓
Python Serial Reader
      ↓
Smart Cart Pipeline
```

If a stage fails, **fix it before moving forward**.

---

# 2️⃣ No Output in Arduino Serial Monitor

## Symptoms

Serial Monitor shows **nothing**.

## Possible Causes

### Firmware not uploaded

Ensure firmware is uploaded:

```
firmware/hx711_reader/hx711_reader.ino
```

Press **Upload (→)** in Arduino IDE.

---

### Wrong board selected

Check:

```
Tools → Board
```

Example:

```
Arduino Uno
ESP32 Dev Module
```

---

### Wrong COM port

Check:

```
Tools → Port
```

Example:

```
COM3
COM7
```

---

# 3️⃣ Serial Output Shows Only Zeros

Example:

```
0
0
0
0
```

## Possible Causes

### Load cell wired incorrectly

Verify wiring:

| Load Cell | HX711 |
| --------- | ----- |
| Red       | E+    |
| Black     | E-    |
| White     | A-    |
| Green     | A+    |

Incorrect wiring is **the most common issue**.

---

### HX711 not powered

Verify connections:

| HX711 | Microcontroller |
| ----- | --------------- |
| VCC   | 5V / 3.3V       |
| GND   | GND             |

---

# 4️⃣ Weight Changes but Values Are Wrong

Example:

```
500g object shows 1200g
```

This means the **calibration factor is incorrect**.

Open firmware:

```
firmware/hx711_reader/hx711_reader.ino
```

Find:

```cpp
float calibration_factor = -7050;
```

Adjust until the measured weight matches the real weight.

Recommended process:

1. Place a **known weight**
2. Adjust value
3. Upload firmware
4. Repeat

---

# 5️⃣ Weight Fluctuates Constantly

Example output:

```
120
123
118
125
121
```

## Possible Causes

### Mechanical vibration

Load cells detect very small vibrations.

Solutions:

* Use a **stable platform**
* Avoid touching the table
* Ensure load cell is mounted securely

---

### Electrical noise

Possible fixes:

* Shorter wires
* Good ground connection
* Shielded cables

---

### Sensor noise (normal)

Software filters will ignore small fluctuations.

The Smart Cart system ignores:

```
< 5g weight change
```

---

# 6️⃣ Serial Works But Python Cannot Read Data

Example Python error:

```
serial.serialutil.SerialException
```

## Fix

Install serial library:

```bash
pip install pyserial
```

---

### Wrong COM port in Python

Open:

```
providers/hardware/weight_provider_serial.py
```

Check:

```python
port="COM3"
```

Update to the correct port.

Example:

```
COM7
COM5
```

---

# 7️⃣ Python Receives Data But Smart Cart Does Not Trigger

Example:

Python shows weight values but pipeline does not react.

Possible causes:

### Weight change too small

The system ignores small noise.

Minimum trigger threshold:

```
5 grams
```

---

### Weight not stabilizing

Ensure the object is **placed steadily**.

The system waits for stabilization before triggering detection.

---

# 8️⃣ Camera Works But Product Not Detected

Check the following:

### Lighting conditions

Ensure the product is well lit.

Avoid:

* shadows
* glare
* strong backlight

---

### Product placement

Place the product **inside the camera capture region**.

The camera reads the **center area of the frame**.

---

# 9️⃣ Product Identified Incorrectly

Possible causes:

### Similar weights

Products with similar weights may cause confusion.

Vision hints help reduce this but are not perfect.

---

### Camera color misclassification

Lighting conditions can change detected color.

This is expected behavior in simple vision systems.

---

# 🔟 Complete System Not Responding

Restart everything in this order:

1️⃣ Disconnect USB
2️⃣ Restart Arduino IDE
3️⃣ Reconnect board
4️⃣ Upload firmware again
5️⃣ Restart Python program

---

# 11️⃣ Quick Test Commands

## Test Arduino Serial Output

Use Arduino **Serial Monitor**.

Expected output:

```
0
0
125
125
250
```

---

## Test Python Serial Reader

Create temporary script:

```python
import serial

ser = serial.Serial("COM3",115200)

while True:
    print(ser.readline().decode().strip())
```

Run:

```
python test_serial.py
```

---

# 12️⃣ Most Common Problems (Quick Checklist)

Before deeper debugging, check these first:

✔ HX711 powered
✔ Load cell wires correct
✔ Firmware uploaded
✔ Correct COM port
✔ Serial monitor shows weight values
✔ Python can read serial data

Most hardware issues are solved by fixing **one of these**.

---

# 13️⃣ When Asking for Help

When reporting an issue, always include:

1️⃣ Photo of wiring
2️⃣ Arduino Serial Monitor output
3️⃣ Python error message
4️⃣ Board type (Arduino / ESP32)
5️⃣ COM port used

This information helps diagnose problems quickly.

---

# 📌 Final Advice

Hardware debugging is easiest when done **one layer at a time**.

```
Hardware
 → Firmware
 → Serial output
 → Python reader
 → Smart Cart pipeline
```

Do not try to debug everything simultaneously.

Follow the steps above to identify problems quickly.
