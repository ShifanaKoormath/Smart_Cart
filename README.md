

# 🛒 Smart Cart System (Hybrid Simulation + Hardware Prototype)

## 📌 Overview

The **Smart Cart System** is a **demo-focused smart retail prototype** that automatically detects products placed inside a shopping cart using a combination of:

```
Weight sensing
Computer vision hints
Deterministic product resolution
```

The system continuously detects **product additions and removals**, updates the cart in real time, generates a bill, and enforces **payment verification before exit**.

This project is designed primarily for:

* Academic demonstrations
* IoT + Computer Vision concept validation
* System architecture explanation
* Smart retail prototype demonstrations

⚠️ This project is **not intended for production deployment**.

---

# 🎯 Key Capabilities

### Smart Cart Features

* ⚖️ **Weight-based product detection**
* 📷 **Camera-based visual hints**
* 🎨 **Dominant color extraction**
* 🧠 **Product resolution using weight + color hints**
* 🧾 **Real-time cart UI updates**
* 💳 **QR-based payment simulation**
* 🚪 **Exit gate payment verification**
* 🔁 **Session reset for new customer**

---

# 🧠 Core Design Philosophy

The system intentionally uses a **deterministic hybrid architecture** instead of AI-heavy recognition.

---

## Weight = Source of Truth

```
Weight Change
      ↓
Product Resolver
      ↓
Cart Update
```

Weight sensors are **the most reliable signal** in retail carts.

Therefore:

> Weight changes drive product detection.

---

## Vision = Contextual Hint

Computer vision is **not used to identify products directly**.

Instead it provides:

```
dominant colors
coarse shape hints
```

These hints **reduce ambiguity** between products.

Example:

```
Weight = 120g
Possible products = [Toothpaste, Biscuit]

Vision detects → blue packaging
Resolver selects → Toothpaste
```

---

## Backend Authority

The **backend pipeline controls all decisions**.

The UI is **display-only** and cannot modify:

* product identification
* billing logic
* cart state
* payment state

---

## Payment Enforcement

Exit is only allowed after verifying:

```
Cart total
↓
Payment status
↓
Exit gate unlock
```

---

# 🔄 System Workflow

```
Weight Change Detected
        │
        ▼
Weight Stabilization
        │
        ▼
Camera Frame Capture
        │
        ▼
Vision Hint Extraction
 • dominant colors
 • coarse shape
        │
        ▼
Color → Category Mapping
        │
        ▼
Product Resolution
(weight + hints)
        │
        ▼
Cart Update
        │
        ▼
Billing
        │
        ▼
QR Payment Simulation
        │
        ▼
Exit Gate Verification
        │
        ▼
Session Reset
```

---

# 🧩 Technology Stack

| Component     | Technology        |
| ------------- | ----------------- |
| Language      | Python 3.9+       |
| UI            | Tkinter           |
| Vision        | OpenCV            |
| QR Code       | qrcode + Pillow   |
| Data          | JSON catalog      |
| Hardware      | Load Cell + HX711 |
| Firmware      | Arduino           |
| Communication | Serial USB        |

---

# 📁 Project Structure

Current architecture separates **shared logic, hardware inputs, and simulation inputs**.

```
smart_cart_system
│
├── main.py
│
├── config
│   └── system_mode.py
│
├── common
│   ├── models
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── cart_item.py
│   │
│   ├── services
│   │   ├── camera_real.py
│   │   ├── event_handler.py
│   │   ├── product_loader.py
│   │   ├── product_resolver.py
│   │   └── vision_mapper.py
│   │
│   └── ui
│       └── smart_cart_ui.py
│
├── inputs
│   ├── simulation
│   │   ├── weight_provider_sim.py
│   │   └── simulator.py
│   │
│   └── hardware
│       └── weight_provider_serial.py
│
├── firmware
│   └── hx711_reader
│       └── hx711_reader.ino
│
├── data
│   └── products.json
│
├── docs
│
├── requirements.txt
└── README.md
```

---

# ⚙️ System Modes

The system supports **two operating modes**.

Mode is selected in:

```
config/system_mode.py
```

Example:

```python
SYSTEM_MODE = "simulation"
```

or

```python
SYSTEM_MODE = "hardware"
```

---

# 🧪 Simulation Mode

Simulation mode allows the system to run **without hardware sensors**.

Weight input is **typed manually** through the terminal.

### Enable Simulation Mode

```
config/system_mode.py
```

```
SYSTEM_MODE = "simulation"
```

---

### Run System

```
python main.py
```

---

### Adding Products

Terminal prompt:

```
Enter weight change (e.g. 125, -120)
```

Examples:

```
125
```

Adds a **125g product**

```
-120
```

Removes a **120g product**

---

### Camera Behavior

While entering weight:

1. Hold product in front of camera
2. Camera captures frame
3. Vision hints extracted

Example debug output:

```
Detected colors: ['orange']
Aspect ratio: 1.3
Area ratio: 0.98
```

---

### Stable Simulation Checkpoint

A fully working simulation pipeline is tagged.

```
simulation-stable-v1
```

Restore it with:

```
git checkout simulation-stable-v1
```

This ensures a **working demo even if hardware fails**.

---

# 🔧 Hardware Mode

Hardware mode uses **real sensors**.

### Hardware Components

| Component       | Purpose                |
| --------------- | ---------------------- |
| Load Cell       | Measure product weight |
| HX711 Amplifier | Convert analog signal  |
| Arduino         | Read sensor values     |
| USB Webcam      | Capture product images |
| Laptop          | Run backend pipeline   |

---

# 🔌 Hardware Wiring

### Load Cell → HX711

Typical wires:

| Load Cell Wire | HX711 Pin |
| -------------- | --------- |
| Red            | E+        |
| Black          | E-        |
| White          | A-        |
| Green          | A+        |

---

### HX711 → Arduino

| HX711 | Arduino |
| ----- | ------- |
| VCC   | 5V      |
| GND   | GND     |
| DT    | D2      |
| SCK   | D3      |

---

### Arduino → Laptop

```
USB Cable
```

Used for:

```
Power
Serial Communication
```

---

# ⚙️ Firmware Upload

Open Arduino IDE.

Upload:

```
firmware/hx711_reader/hx711_reader.ino
```

The firmware outputs:

```
ADD:125
REMOVE:120
```

These values represent **weight differences detected by the sensor**.

---

# 🔌 Serial Communication

Python reads Arduino data using:

```
inputs/hardware/weight_provider_serial.py
```

Example serial output:

```
ADD:125
REMOVE:120
```

Python converts this into:

```
+125  → add product
-120  → remove product
```

---

# 🚀 Running Hardware Mode

Set mode:

```
config/system_mode.py
```

```
SYSTEM_MODE = "hardware"
```

Then run:

```
python main.py
```

Expected output:

```
=== SMART CART PIPELINE MODE START (HARDWARE) ===
```

---

# 📷 Camera Requirements

Any standard **USB webcam** works.

Minimum recommended:

```
720p
30fps
fixed focus
```

Test camera:

```
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

---

# ⚠️ Important Notes

### Close Arduino Serial Monitor

Python cannot access the COM port if Arduino IDE is using it.

---

### Ensure Stable Platform

Load cell must be mounted on a **rigid platform** to avoid vibration noise.

---

### Calibration Required

Load cell calibration factor must be tuned inside:

```
hx711_reader.ino
```

Example:

```
float calibration_factor = -98.64;
```

---

# ⚠️ Known Limitations

This project intentionally avoids complexity.

Limitations include:

* No ML-based product recognition
* No real payment gateway
* No real exit gate hardware
* QR payment is simulated
* Vision is coarse classification only

These choices improve:

```
System explainability
Demo reliability
Academic suitability
```

---

# 📌 Intended Use

This project is designed for:

* Academic demonstrations
* IoT + Computer Vision coursework
* Smart retail system prototypes
* System architecture explanation

It is **not intended for commercial deployment**.

---

# 👩‍💻 Author

Developed as a **Smart Cart System hybrid simulation + hardware prototype** for academic demonstration and system design validation.

