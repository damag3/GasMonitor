# GasMonitor – Gas Detection System for Raspberry Pi Zero W

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-green)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Zero%20W-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

GasMonitor is a lightweight, industrial‑style gas detection system built on:

- Raspberry Pi Zero W  
- ADS1115 (16‑bit ADC)  
- MQ‑2 sensor (butane / smoke)  
- TGS2610 sensor (methane)  
- Status LEDs (green, yellow, red)  
- Buzzer  
- Physical button  
- 40×40 cooling fan  
- Web dashboard (Flask)

Includes:

- Moving‑average filtering  
- Automatic baseline tracking  
- Fast‑rise detection  
- 3‑minute cooldown after silencing  
- Physical LED indicators  
- Web dashboard  
- `/data` API endpoint for integrations  

---

## 📦 Project Structure

gasmonitor/
├── gas_monitor.py
├── dashboard.html
├── README.md
└── gasenv/ (ignored)


---

## 🔧 Hardware Wiring

### Sensors
- MQ‑2 → ADS1115 A0  
- TGS2610 → ADS1115 A1  
- ADS1115 → I2C (SCL/SDA)

### Buzzer
- GPIO 27 → buzzer +  
- GND → buzzer –

### Button
- GPIO 26 → button  
- GND → button  
*(internal pull‑up enabled)*

### LEDs
- Green → GPIO 5  
- Yellow → GPIO 6  
- Red → GPIO 13  
- Each with 220 Ω resistor

### Fan (40×40)
- 5V → fan +  
- GND → fan –  
- Optional: 470 µF capacitor across 5V/GND

---

## 🧪 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USER/gasmonitor.git
cd gasmonitor

python3 -m venv gasenv
source gasenv/bin/activate

pip install flask adafruit-circuitpython-ads1x15

source gasenv/bin/activate
python3 gas_monitor.py


http://<PI_IP>:8080
```

🖥️ MagicMirror² Integration
This project integrates with the MagicMirror module:

👉 MMM‑GasMonitor  
https://github.com/damag3/MMM-GasMonitor

