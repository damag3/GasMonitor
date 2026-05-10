from flask import Flask, jsonify, send_file
import board
import busio
import digitalio
import time
import threading

from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# ===================== CONFIG =====================
BUZZER_PIN = 27
BUTTON_PIN = 26

LED_GREEN = 5
LED_YELLOW = 6
LED_RED = 13

FILTER_SIZE = 10
mq2_buf = [0] * FILTER_SIZE
tgs_buf = [0] * FILTER_SIZE
idx = 0

mq2_raw = 0
tgs_raw = 0
mq2_norm = 0
tgs_norm = 0

mq2_prev = 0
mq2_base = 0

alarmState = False          # estado do buzzer
alarm_raw = False           # estado real dos sensores
sensorError = False
startup_counter = 0

silenced_until = 0          # cooldown

# ===================== HARDWARE =====================
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

chan_mq2 = AnalogIn(ads, 0)
chan_tgs = AnalogIn(ads, 1)

buzzer = digitalio.DigitalInOut(board.D27)
buzzer.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.D26)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led_green = digitalio.DigitalInOut(board.D5)
led_green.direction = digitalio.Direction.OUTPUT

led_yellow = digitalio.DigitalInOut(board.D6)
led_yellow.direction = digitalio.Direction.OUTPUT

led_red = digitalio.DigitalInOut(board.D13)
led_red.direction = digitalio.Direction.OUTPUT

# ===================== FILTER =====================
def moving_average(buf, val):
    global idx
    buf[idx] = val
    idx = (idx + 1) % FILTER_SIZE
    return sum(buf) // FILTER_SIZE

# ===================== BASELINE =====================
def update_baseline(val):
    global mq2_base

    if val < 50:
        return

    if mq2_base == 0:
        mq2_base = val
        return

    if abs(val - mq2_base) < 20:
        mq2_base = (mq2_base * 49 + val) // 50

# ===================== SENSOR =====================
def read_sensors():
    global mq2_raw, tgs_raw, mq2_norm, tgs_norm, sensorError

    raw_mq2 = chan_mq2.value
    raw_tgs = chan_tgs.value

    if raw_mq2 < 50 and raw_tgs < 50:
        sensorError = True
        return
    else:
        sensorError = False

    mq2_raw = moving_average(mq2_buf, raw_mq2)
    tgs_raw = moving_average(tgs_buf, raw_tgs)

    mq2_norm = int((mq2_raw / 32767) * 1023)
    tgs_norm = int((tgs_raw / 32767) * 1023)

    update_baseline(mq2_norm)

# ===================== LOGIC =====================
def update_alarm():
    global alarmState, alarm_raw, mq2_prev, silenced_until

    # Alarme real dos sensores
    mq2_alarm = mq2_norm >= 380
    tgs_alarm = tgs_norm >= 160
    fast = (mq2_norm - mq2_prev) > 120

    alarm_raw = mq2_alarm or tgs_alarm or fast
    mq2_prev = mq2_norm

    # Se estiver silenciado → buzzer OFF
    if time.time() < silenced_until:
        alarmState = False
        return

    # Se houver erro → buzzer OFF
    if sensorError:
        alarmState = False
        return

    # Caso contrário → buzzer segue o alarme real
    alarmState = alarm_raw

# ===================== BUZZER =====================
def update_buzzer():
    buzzer.value = alarmState

# ===================== LEDS =====================
def update_leds():
    now = time.time()

    # Erro de sensor
    if sensorError:
        led_green.value = False
        led_red.value = False
        led_yellow.value = int(now % 1 < 0.5)
        return

    # Arranque
    if startup_counter < 20:
        led_green.value = False
        led_red.value = False
        led_yellow.value = True
        return

    # Silenciado
    if now < silenced_until:
        led_green.value = int(now % 1 < 0.5)
        led_yellow.value = False
        led_red.value = False
        return

    # Alarme real
    if alarm_raw:
        led_green.value = False
        led_yellow.value = False
        led_red.value = True
        return

    # Normal
    led_green.value = True
    led_yellow.value = False
    led_red.value = False

# ===================== BACKGROUND LOOP =====================
def loop():
    global alarmState, startup_counter, silenced_until

    while True:
        if startup_counter < 20:
            startup_counter += 1
            read_sensors()
            update_leds()
            time.sleep(0.5)
            continue

        # Botão físico → silencia 3 minutos
        if not button.value:
            alarmState = False
            silenced_until = time.time() + 180
            update_buzzer()

        read_sensors()
        update_alarm()
        update_buzzer()
        update_leds()

        time.sleep(0.5)

threading.Thread(target=loop, daemon=True).start()

# ===================== WEB SERVER =====================
app = Flask(__name__)

@app.route("/")
def index():
    return send_file("dashboard.html")

@app.route("/data")
def data():
    return jsonify({
        "mq2": mq2_norm,
        "tgs": tgs_norm,
        "baseline": mq2_base,
        "alarm": alarmState,               # buzzer ON/OFF
        "alarm_raw": alarm_raw,            # sensores ultrapassaram limites
        "silenced": time.time() < silenced_until,
        "error": sensorError
    })

@app.route("/off")
def off():
    global alarmState, silenced_until
    alarmState = False
    silenced_until = time.time() + 180
    update_buzzer()
    return "OFF"

app.run(host="0.0.0.0", port=8080)
