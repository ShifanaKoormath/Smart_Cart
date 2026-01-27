

# 🛒 Smart Cart System – Camera-Integrated Hybrid Demo

## Project Overview

This project is a **Smart Cart System prototype** that demonstrates automated product addition and removal using a **hybrid sensing approach**.

The system integrates:

* **Real-time camera input** for visual feature extraction
* **Weight-based resolution** (currently simulated) for deterministic product identification
* **Live cart management** with automatic billing updates

The goal of the project is to showcase **system design, sensor integration, and decision logic**, rather than full-scale commercial deployment.

---

## Key Features

* 📷 **Real-time camera capture**
* 🎨 Visual feature extraction (dominant color + coarse shape hints)
* ⚖️ Weight-based product resolution (keyboard-simulated)
* ➕ Automatic add to cart
* ➖ Automatic removal from cart
* 🧾 Live bill calculation
* 🧠 Deterministic, explainable decision logic
* 🔌 Architecture ready for real hardware integration

---

## System Architecture

```
Camera
  ↓
Visual Feature Extraction
  ↓
Category Hint (NOT final decision)
  ↓
Weight Input (Simulated / Sensor-ready)
  ↓
Product Resolution
  ↓
Cart Update & Billing
```

### Design Principle

> **Vision is used as a hint, weight is the final authority.**

This avoids incorrect billing when products share similar visual characteristics.

---

## Technologies Used

* **Language:** Python
* **Computer Vision:** OpenCV
* **Architecture:** Modular, service-based design
* **Input Devices:**

  * Camera (real)
  * Weight sensor (simulated via keyboard input)

---

## Product Identification Logic

1. **Camera captures image**
2. **Visual features extracted**

   * Dominant color
   * Coarse shape metrics (aspect ratio, area)
3. **Possible product categories are inferred**
4. **Weight change is read**
5. **Product is resolved by matching weight**
6. **Cart is updated safely**

If confidence is low or ambiguity exists, the system **rejects the event instead of guessing**.

---

## Weight Simulation (Current Demo Mode)

For demonstration and testing, the weight sensor is simulated via **keyboard input**.

### Example Inputs

* `125` → Add Santoor Soap
* `120` → Add Colgate Toothpaste
* `-125` → Remove Santoor Soap
* `q` → End demo

This simulation layer is abstracted and can be replaced with a **real load cell sensor** without changing core logic.

---

## Why Not Vision-Only or ML?

* Product appearance varies widely across brands
* Color and shape are not unique identifiers
* Vision-only systems are prone to misclassification

### Engineering Decision

> **Weight provides deterministic identification, vision provides context.**

This design reflects **real-world smart retail systems**, prioritizing correctness over guessing.

---

## Limitations

* Weight sensor is currently simulated
* Products with identical weights cannot be distinguished without additional identifiers (e.g., barcode or RFID)
* Shape detection is coarse and used only as a secondary constraint
* System is designed for controlled demo environments

These limitations are **intentional and acknowledged**.

---

## Future Enhancements

* Integration with real load cell hardware
* Barcode / QR code scanning for SKU-level identification
* Improved object segmentation
* Optional ML-based category classification
* UI-based cart display

---

## Demo Readiness

The system is **demo-stable**, deterministic, and explainable.

It is designed to:

* Never add a wrong product
* Reject uncertain events safely
* Clearly demonstrate system logic

---

## Author Notes

This project focuses on **engineering trade-offs, modular design, and reliability**, rather than attempting to solve large-scale retail automation with limited data.

---

## License

Academic / Educational Use

---


