# 👁️ RoboEyes: High-Frame-Rate GC9A01 SPI System

**RoboEyes** is a high-speed, low-latency visual expression system for robotics. By leveraging the **RP2040’s dual-core architecture** and dual **GC9A01 round LCDs**, it implements complex ocular movements, including **partial window refreshes** and **asynchronous blinking state machines**.

---

<table width="100%">
  <tr>
    <td width="60%" align="left" valign="middle">
      <h2>🚀 Engineering Challenge: Memory Optimization</h2>
    </td>
    <td width="40%" align="center" valign="middle">
      <img src="https://github.com/user-attachments/assets/d4d73b5c-27c2-40ac-8f5b-01d5ba31416f" alt="RoboEyes Dual Display Hardware Interface" width="250" style="border-radius: 8px;" />
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <p>
        Standard procedural rendering (like the classic "Uncanny Eyes") is notoriously resource-heavy, often bottlenecking the RP2040's limited SRAM.
      </p>
      <p>
        This project overcomes these constraints by shifting from procedural math to <b>Smart Buffer Manipulation</b>. By utilizing high-speed SPI and targeted window updates, the system delivers lifelike, 60FPS fluid motion that rivals much more powerful processors, while leaving CPU cycles free for UART telemetry handling.
      </p>
    </td>
  </tr>
</table>

---

## ✨ Key Technical Features

* **Partial Refresh Logic:** Updates only the <b>active pixel regions</b> of the GC9A01 display, drastically reducing SPI bus congestion.
* **Dual-CS Synchronization:** Drives two independent displays over a shared SPI bus using optimized Chip Select multiplexing.
* **Asynchronous State Machine:** Manages randomized blinking and <b>saccade-masking</b> via non-blocking timers.
* **RGB565 Asset Pipeline:** Pre-loads 16-bit BMP assets into local storage for immediate access during tracking interrupts.
* **UART Telemetry Integration:** Ready-to-use serial listener designed to map <b>centroid coordinates</b> from the ESP32-CAM FaceTracker.

## 🛠️ Hardware Stack

* **MCU:** Raspberry Pi Pico (RP2040) @ 133MHz.
* **Display Hardware:** 2x GC9A01 1.28-Inch Round LCD TFT (240x240 resolution).
* **Communication:** High-speed Hardware SPI for video; 3.3V UART for coordinate input.
* **Co-Processor (Optional):** **ESP32-CAM** providing real-time human tracking coordinates.

---

## 🔌 Wiring & Pinout (Dual-SPI)

To maximize frame rates, the displays share the Clock (SCK) and Data (MOSI) lines while using independent CS pins to manage bus contention.

| Peripheral | Pico Pin | Function | Logic Level |
| :--- | :--- | :--- | :--- |
| **Global SPI** | GP18 | SCK | 3.3V Clock |
| **Global SPI** | GP19 | MOSI | 3.3V Data |
| **Left LCD** | GP17 | CS | Chip Select L |
| **Right LCD** | GP20 | CS | Chip Select R |
| **Telemetry RX** | GP1 | UART RX | 3.3V Serial |

---

## 📐 Logic & Data Flow

### The Window Refresh Strategy
The RP2040 lacks the memory to buffer a full 57,600-pixel frame in 16-bit color. This system solves the bottleneck by defining **Dynamic Clipping Windows**:
1. Only the bounding box of the moving pupil is calculated.
2. The SPI controller is pointed to those specific coordinates.
3. Only the "delta" pixels are transmitted, bypassing the static iris/sclera data.

### Centroid Tracking Loop
1. **Reception:** UART receives $X, Y$ centroid data from the FaceTracker.
2. **Mapping:** The Pico translates world-space coordinates into the 240x240 pixel space of the GC9A01.
3. **Synchronization:** Both displays update their pupil offsets simultaneously via the shared bus.
4. **Outcome:** The robot maintains constant, human-like eye contact.

---

## ⚡ Quick Start

1. **Firmware:** Flash the Pico with the provided build (Optimized for SPI throughput).
2. **Assets:** Transfer `.bmp` assets (pupil, iris, eyelid) to the onboard flash.
3. **Calibration:** Configure the `eye_config.h` file to set your default pupil travel limits.
4. **Deployment:** Power via a stable 3.3V/5V rail and initiate the UART link.

## 🗺️ Future Roadmap

* **DMA SPI Transfer:** Freeing up both RP2040 cores during data transmission.
* **Interactive Mood Logic:** Adjusting eyelid "droop" and pupillary dilation via HTTP/JSON commands.
* **I2C Bus Consolidation:** Migrating UART telemetry to a shared I2C bus with the servo controller.

---

<small>© 2026 MatsRobot | Licensed under the [MIT License](https://github.com/MatsRobot/matsrobot.github.io/blob/main/LICENSE)</small>
