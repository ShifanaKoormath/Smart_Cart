

# 🛒 Smart Cart System (Demo Prototype)

## 📌 Overview

The **Smart Cart System** is a **demo-focused prototype** that simulates how a smart shopping cart can automatically detect products added or removed, calculate the bill in real time, and enforce payment verification before allowing exit.

This project is **not a production system**. It is designed for:

* Academic demonstrations
* Concept validation
* Architecture and workflow explanation

The system prioritizes:

```
Deterministic behavior
Explainable logic
Demo reliability
```

---

# 🎯 Key Capabilities

* 📷 **Camera-based product observation (OpenCV)**
* ⚖️ **Weight-based product identification (authoritative signal)**
* 🎨 **Vision hints using dominant color detection**
* 🧠 **Color palette verification against product catalog**
* 🧾 **Real-time cart updates and billing**
* 💳 **QR-based payment simulation**
* 🚪 **Exit gate verification**
* 🔁 **Session reset for new customer**
* 🖥️ **Interactive cart UI (Tkinter)**

---

# 🧠 Core Design Philosophy

The system intentionally follows a **deterministic hybrid approach**.

### Weight = Source of Truth

```
Weight change
↓
Product resolution
↓
Cart update
```

Weight sensors are the most reliable signal in retail environments.

---

### Vision = Contextual Hint

Vision is used only to **narrow possible product categories**, not to directly identify products.

Extracted hints include:

* Dominant colors (top 2)
* Coarse shape features

This prevents unreliable computer vision from causing misidentification.

---

### Backend Authority

The **backend logic controls all decisions**.

The UI is **display-only** and cannot modify:

* product resolution
* billing logic
* cart state
* payment state

---

### Payment Enforcement

The system prevents unpaid exit by verifying:

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
(weight + vision hints)
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

| Component          | Technology                        |
| ------------------ | --------------------------------- |
| Language           | Python 3.9+                       |
| UI                 | Tkinter                           |
| Vision             | OpenCV                            |
| QR Code            | qrcode + Pillow                   |
| Data               | JSON catalog                      |
| Backend            | Python services                   |
| Hardware (planned) | Load Cell + HX711 + ESP32/Arduino |

---

# 📁 Project Structure

```
smart_cart_system/
│
├── main.py                     # System pipeline entry point
│
├── models/
│   ├── product.py              # Product data model
│   ├── cart.py                 # Cart & CartItem logic
│
├── services/
│   ├── camera_real.py          # Camera capture & vision hints
│   ├── weight_provider.py      # Weight simulation / hardware abstraction
│   ├── product_resolver.py     # Product resolution logic
│   ├── event_handler.py        # Add / remove logic
│   ├── vision_mapper.py        # Color → category mapping
│
├── ui/
│   └── smart_cart_ui.py        # On-cart display UI
│
├── data/
│   └── products.json           # Product catalog
│
├── requirements.txt
└── README.md
```

---

# 🔧 Prerequisites

## 1️⃣ Python

Check installation:

```bash
python --version
```

Required:

```
Python 3.9+
```

Download if needed:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

During installation enable:

```
✔ Add Python to PATH
```

---

## 2️⃣ pip

Check pip:

```bash
pip --version
```

If missing:

```bash
python -m ensurepip --upgrade
```

---

## 3️⃣ Camera Availability

Ensure a webcam is connected.

Optional test:

```bash
python - <<EOF
import cv2
cap = cv2.VideoCapture(0)
print("Camera OK" if cap.isOpened() else "Camera NOT accessible")
cap.release()
EOF
```

---

⚠️ Notes

* Internet connection **not required after setup**
* No machine learning models required
* Weight sensor currently **simulated via keyboard input**

---

# ⚙️ Setup Instructions

Open VS Code → Open Project → Open Terminal.

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/ShifanaKoormath/Smart_Cart.git
cd smart_cart_system
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```
venv\Scripts\activate
```

### macOS / Linux

```
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

Key packages:

```
opencv-python
numpy
pillow
qrcode
```

---

## 4️⃣ Run the System

```
python main.py
```

---

# 🎮 Demo Mode Usage

## 🛍️ Adding Products

The system prompts for **weight change input**.

```
Positive weight → add product
Negative weight → remove product
```

Example:

```
125
```

Adds a product close to **125g**.

Example:

```
-120
```

Removes a **120g product**.

---

## 📷 Camera Interaction

When entering weight:

1. Hold product in front of camera
2. Wait for capture
3. Vision hints are extracted

Detected features include:

```
dominant colors
aspect ratio
area ratio
```

---

## 🧾 Billing

Click:

```
Proceed to Bill
```

The UI shows the final cart summary.

---

## 💳 Payment Simulation

Click:

```
Pay Now
```

A **QR code appears**.

Click:

```
Confirm Payment (Demo)
```

to simulate successful payment.

---

⚠️ QR scan itself **does NOT confirm payment**.

---

## 🚪 Exit Gate

Click:

```
Proceed to Exit Gate
```

Behavior:

| Payment Status | Gate   |
| -------------- | ------ |
| Paid           | Opens  |
| Unpaid         | Locked |

---

## 🔁 New Customer

Click:

```
New Cart
```

This resets the entire backend cart session.

---

# 🧪 Simulation Mode

This version uses **keyboard input instead of real sensors**.

```
Weight input → simulated load cell
Camera → real
Vision → hint only
Resolver → weight-dominant
```

This ensures **predictable demo behavior**.

---

# 🏷 Stable Simulation Checkpoint

A stable simulation version has been tagged.

```
simulation-stable-v1
```

This version represents the **fully working simulation pipeline**.

---

## Checkout Stable Demo Version

To restore the stable version:

```
git checkout simulation-stable-v1
```

Or create a safe branch:

```
git checkout -b simulation-stable simulation-stable-v1
```

This checkpoint ensures the demo can run even if hardware integration fails.

---

# 🔧 Hardware Integration (Future)

The architecture supports real hardware.

Planned hardware:

```
Load Cell
HX711 amplifier
Arduino / ESP32
Serial communication to Python
```

Only the module below needs modification:

```
services/weight_provider.py
```

All other logic remains unchanged.

---

# ⚠️ Limitations

This is intentionally a **demo prototype**.

Limitations include:

* No real payment gateway
* No ML-based product recognition
* No real exit gate hardware
* QR payment is simulated
* Weight sensor is simulated via keyboard

These choices improve:

```
Demo reliability
Explainability
Academic suitability
```

---

# 📌 Intended Use

Designed for:

* Academic demonstrations
* Smart retail concept explanation
* System architecture validation
* Computer vision + IoT integration demos

Not intended for production deployment.

---

# 👩‍💻 Author

Developed as a **Smart Cart System demonstration prototype**.

Maintained for academic and concept validation purposes.

---
