# 🤖 RoboEyes: High-Frame-Rate GC9A01 Blinking System

An optimized visual expression system for robots using dual 1.28-inch round LCDs and an RP2040, featuring high-speed pupil tracking and blinking animations.

<p align="center">
  <img width="400" src="https://github.com/user-attachments/assets/d4d73b5c-27c2-40ac-8f5b-01d5ba31416f" alt="RoboEyes Display View" />
</p>

---

## 🚀 The Backstory

Project "Uncanny Eyes" has long been the gold standard for robotic expressions, but it is notoriously resource-heavy. While originally designed for the ESP32, porting it to the Raspberry Pi Pico (RP2040) often results in sluggish frame rates and screen tearing due to the Pico's memory constraints and SPI bus bottlenecks.

I needed the eyes to look "alive," which requires fluid motion and instant response. By moving away from real-time procedural rendering and toward a **smart buffer manipulation** strategy, I achieved smooth, high-speed eye movement on the Pico that rivals much more powerful processors.

## ✨ Key Features

* **High-Speed Animation:** Uses a "Buffer-Pointer" technique to move pupils without re-drawing the entire frame, overcoming RP2040 RAM limits.
* **Dual-Display Synchronization:** Drives two GC9A01 round LCDs simultaneously for a cohesive facial expression.
* **Efficient Memory Usage:** Pre-loads BMP assets into the display buffer at boot, drastically reducing real-time computational overhead.
* **Randomized Expression Logic:** Features built-in "look and blink" algorithms to simulate natural, lifelike eye movement.
* **Expandable Control:** Ready to accept external X/Y coordinates via UART/I2C for active face tracking.

## 🛠️ Hardware Stack

* **Microcontroller:** Raspberry Pi Pico (RP2040).
* **Displays:** 2x GC9A01 1.28-Inch Round LCD TFT (240x240 resolution).
* **Communication:** High-speed SPI.
* **Optional Input:** ESP32-CAM (for providing real-time X/Y coordinates of human faces).



## 📐 How It Works

### The Memory Workaround
The RP2040 lacks the internal memory to hold multiple full-color 240x240 frames in a standard frame buffer while simultaneously processing complex "Uncanny Eye" math. 

**The Solution:**
1. **Boot Load:** The processor reads the BMP eye assets and writes them directly to the display's internal controller memory.
2. **The Window Trick:** Instead of sending 57,600 pixels every frame, the code simply updates the "window" or the specific coordinates where the pupil and eyelid are currently located.
3. **The Result:** This significantly reduces the amount of data sent over the SPI bus, resulting in a high-speed, flicker-free "blink."

### Interaction & Tracking
Currently, the eyes move to random positions to give the robot a "thinking" appearance while the head moves. However, the system is designed to interface with an **ESP32-CAM**: 
* The ESP32-CAM detects a face and calculates the $X, Y$ coordinates.
* It sends these coordinates to the Pico via Serial.
* The Pico shifts the pupil "pointer" to match those coordinates.
* **Outcome:** The robot maintains "eye contact" as you move across the room.



---

## 🚀 Installation & Usage

1. **Flash Firmware:** Ensure your Pico is running a stable MicroPython or C++ build.
2. **Upload Assets:** Transfer the required `.bmp` files (iris, pupil, eyelid) to the Pico's root directory.
3. **Wiring:** Connect the dual GC9A01 displays via the SPI pins. (Note: They can share the `SCK` and `MOSI` lines but require separate `CS` pins for independent control).

---

## 📜 Documentation

For wiring diagrams and the coordinate-mapping math used for the round display geometry, see the [RoboEyes Docs](./docs) folder.
