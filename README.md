# 👁️ RoboEyes: High-Frame-Rate Blinking System

**RoboEyes** is a high-speed visual expression system. By pairing a **Raspberry Pi Pico (RP2040)** with dual **GC9A01 round LCDs**, it creates lifelike eye movement and autonomous blinking that bridges the gap between a machine and a face.

---

<div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center;">
  <div style="flex: 1; min-width: 300px;">
    <h2>🚀 The Backstory</h2>
    <p>
      Project "Uncanny Eyes" has long been the gold standard for robotic expressions, but it is notoriously resource-heavy. Porting it to the RP2040 often results in sluggish frame rates due to memory constraints.
    </p>
    <p>
      I needed the eyes to look "alive," which requires fluid motion and instant response. By moving away from real-time procedural rendering and toward a <b>smart buffer manipulation</b> strategy, I achieved smooth, high-speed movement that rivals much more powerful processors.
    </p>
  </div>
  <div style="flex: 1; min-width: 300px; text-align: center;">
    <img src="https://github.com/user-attachments/assets/d4d73b5c-27c2-40ac-8f5b-01d5ba31416f" alt="RoboEyes Project View" style="max-width: 100%; height: auto;" />
  </div>
</div>

---

## ✨ Key Features

* **High-Speed Animation:** Uses a "Buffer-Pointer" technique to move pupils without re-drawing the entire frame, overcoming RP2040 RAM limits.
* **Dual-Display Synchronization:** Drives two GC9A01 round LCDs simultaneously for a cohesive, synchronized facial expression.
* **Natural Blinking Logic:** Implements an asynchronous state machine for randomized blinks and saccade-masking.
* **Efficient Memory Usage:** Pre-loads BMP assets into the display buffer at boot, drastically reducing real-time computational overhead.
* **Tracking-Ready:** Built-in UART/I2C listeners to receive $X, Y$ coordinates from the **FaceTracker** module for active eye contact.

## 🛠️ Hardware Stack

* **Microcontroller:** Raspberry Pi Pico (RP2040).
* **Displays:** 2x GC9A01 1.28-Inch Round LCD TFT (240x240 resolution).
* **Communication:** High-speed SPI for display data; Serial/UART for tracking data.
* **Optional Input:** **ESP32-CAM** (The FaceTracker module providing real-time human coordinates).

---

## 🔌 Wiring & Pinout

To drive dual displays on the Pico, we share the SPI bus but use independent Chip Select (CS) pins to maintain high refresh rates.

| Peripheral | Pico Pin | Function | Notes |
| :--- | :--- | :--- | :--- |
| **Both LCDs** | GP18 | SCK | Shared Clock |
| **Both LCDs** | GP19 | MOSI | Shared Data Line |
| **Left LCD** | GP17 | CS | Left Eye Select |
| **Right LCD** | GP20 | CS | Right Eye Select |
| **ESP32-CAM** | GP1 | RX | Receives $X, Y$ tracking data |

---

## 📐 How It Works

### The Memory Workaround
The RP2040 lacks the RAM to hold multiple full-color frames. To solve this, we use **The Window Trick**: instead of sending 57,600 pixels every frame, the code only updates the specific coordinates where the pupil or eyelid is moving. This results in a high-speed, flicker-free "blink."

### Interaction & Tracking
When integrated with the **FaceTracker** system:
1. **Detection:** The ESP32-CAM calculates the face center.
2. **Transmission:** Coordinates are sent via Serial to the Pico.
3. **Actuation:** The Pico shifts the pupil "pointer" to the matching $X, Y$ position.
4. **Outcome:** The robot maintains "eye contact" as you move across the room.

---

## ⚡ Quick Start

1. **Flash Firmware:** Ensure your Pico is running a stable MicroPython or C++ build.
2. **Upload Assets:** Transfer the required `.bmp` files (iris, pupil, eyelid) to the Pico's root directory.
3. **Wiring:** Connect the dual displays via the SPI pins as shown in the table above.
4. **Test:** Run the `main.py` script; the eyes should perform a "boot-up" blink and enter random-look mode.

## 🗺️ Future Roadmap

* **Saccade Masking:** Perfectly timing a blink to occur exactly when the eye moves to a new target, hiding the "jump."
* **Emotional States:** Adding logic to change pupil size or eyelid "droop" based on the robot's simulated mood.
* **Direct I2C Mapping:** Moving from UART to I2C to allow the Pico and ESP32-CAM to share the same bus as the servos.

---

<small>© 2026 MatsRobot | Licensed under the [MIT License](https://github.com/MatsRobot/matsrobot.github.io/blob/main/LICENSE)</small>
