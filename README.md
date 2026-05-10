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

