
---

# 🛒 Smart Cart System (Demo Prototype)

## 📌 Overview

The **Smart Cart System** is a **demo-focused prototype** that simulates how a smart shopping cart can automatically detect products added or removed, calculate the bill in real time, and enforce payment verification before allowing exit.

This project is **not a production system**. It is designed for:

* Academic demonstration
* Concept validation
* Architecture and workflow explanation

The system prioritizes **deterministic behavior, explainability, and demo safety**.

---

## 🎯 Key Capabilities

* 📷 **Real camera integration** (OpenCV)
* ⚖️ **Weight-based product identification (authoritative)**
* 🎨 **Vision-based hints** (dominant color + coarse shape)
* 🧾 **Real-time cart billing**
* 💳 **Payment simulation using QR code**
* 🚪 **Exit gate verification (paid vs unpaid detection)**
* 🔁 **Session reset for next customer**
* 🖥️ **On-cart UI display (Tkinter)**

---

## 🧠 Core Design Philosophy

* **Weight is the source of truth**
  Vision is used only as a *hint* to reduce ambiguity.

* **No ML-based product recognition**
  Ensures explainability and avoids misclassification.

* **Backend is authoritative**
  UI never makes business decisions.

* **Payment and exit verification are mandatory**
  Prevents unpaid exits.

---

## 🔄 System Workflow

```
Weight Change Detected
 → Weight Stabilization
 → Camera Capture
 → Vision Hint Extraction (color + shape)
 → Product Resolution using Weight
 → Cart Update (Add / Remove)
 → Billing
 → Payment (QR-based simulation)
 → Exit Gate Verification
 → New Cart / Session Reset
```

---

## 🧩 Technology Stack

| Component          | Technology                        |
| ------------------ | --------------------------------- |
| Language           | Python 3.9+                       |
| UI                 | Tkinter                           |
| Vision             | OpenCV                            |
| QR Code            | qrcode + Pillow                   |
| Backend            | Custom Python services            |
| Hardware (planned) | Load Cell + HX711 + Arduino/ESP32 |

---

## 📁 Project Structure

```
smart_cart_system/
│
├── main.py                     # Entry point
│
├── models/
│   ├── product.py              # Product model
│   ├── cart.py                 # Cart & CartItem logic
│
├── services/
│   ├── camera_real.py          # Camera capture & vision hints
│   ├── weight_provider.py      # Weight input abstraction
│   ├── product_resolver.py     # Weight + vision resolution
│   ├── event_handler.py        # Add / remove logic
│   ├── vision_mapper.py        # Color → category mapping
│
├── ui/
│   └── smart_cart_ui.py        # On-cart UI (Tkinter)
│
├── data/
│   └── products.json           # Product catalog
│
├── requirements.txt
└── README.md
```

---



---

## 🔧 Prerequisites (Check & Install)

Follow these steps **before** setting up the project.

---

### 1️⃣ Check Python Installation

Run:

```bash
python --version
```

or:

```bash
python3 --version
```

✅ Required: **Python 3.9 or higher**

#### ❌ If Python is NOT installed

* Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* During installation:

  * ✔️ Check **“Add Python to PATH”**
  * ✔️ Complete installation

Verify again:

```bash
python --version
```

---

### 2️⃣ Check pip Installation

Run:

```bash
pip --version
```

or:

```bash
pip3 --version
```

#### ❌ If pip is missing

Run:

```bash
python -m ensurepip --upgrade
```

Then verify:

```bash
pip --version
```

---

### 3️⃣ Check Camera Availability

* Ensure a webcam is connected
* Close applications that may use the camera (Zoom, Teams, browser, etc.)

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

### ⚠️ Notes

* No internet connection required after installation
* No machine learning models required
* Hardware weight sensor is **simulated via keyboard input** for demo

---



## ⚙️ Setup Instructions


Open VS Code
Open Project directory
Open View -> terminal and run commands below one by one.


### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ShifanaKoormath/Smart_Cart.git
cd smart_cart_system
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

**Activate it:**

* Windows:

```bash
venv\Scripts\activate
```

* macOS / Linux:

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages include:**

* opencv-python
* pillow
* qrcode
* numpy

---

### 4️⃣ Run the Project

```bash
python main.py
```

---

## 🎮 How to Use (Demo Mode)

### 🛍️ Shopping


* You will be prompted to **enter weight changes manually**:

  * Positive value → product added
  * Negative value → product removed
* The camera captures the product image.(place product steadily before camera)

Example:

```
125   → add product of ~125g
-120  → remove product of ~120g
```

---

### 🧾 Billing

* Click **“Proceed to Bill”** in the UI.
* Review the final bill.

---

### 💳 Payment (Simulation)

* Click **“Pay Now”**
* A **QR code is generated** (demo only).
* Click **“Confirm Payment (Demo)”** to simulate payment success.

> QR scanning alone does NOT confirm payment — explicit confirmation is required.

---

### 🚪 Exit Gate Verification

* Click **“Proceed to Exit Gate”**
* If payment is completed → Gate opens
* If payment is not completed → Gate remains locked (violation detected)

---

### 🔁 New Session

* Click **“New Cart”** to reset the backend cart and start a fresh session.

---

## 🔧 Hardware Integration (Planned)

The system is designed so that **real hardware can be added later** without modifying core logic.

### Planned Setup:

* Load Cell + HX711
* Arduino / ESP32
* Serial communication to Python

Only `WeightProvider` needs to be modified to read serial input.

---

## ⚠️ Limitations

* No real payment gateway integration
* No ML-based product recognition
* No real exit gate hardware
* Demo-only QR codes
* Keyboard-simulated weight input

These are **intentional design choices** for safety, explainability, and academic scope.

---

## 📌 Intended Use

* Academic projects
* System architecture demonstrations
* Smart retail concept validation

**Not intended for real-world deployment.**

---

## 👩‍💻 Author / Maintainer

Developed as a **Smart Cart System demo prototype**
for academic and demonstration purposes.

---
