import machine
import time
import framebuf
import ssd1306

# ────────────────────────────────────────────────────────────────────────────
# 1. ADC (TEMT6000) einrichten
# ────────────────────────────────────────────────────────────────────────────
adc_pin = 26                    # GPIO26/ADC0 (physischer Pin 31)
sensor  = machine.ADC(adc_pin)  # TEMT6000 analoger Eingang

# Funktion: Rohwert (0…65535) → Spannung (0…3.3 V)
def raw_to_voltage(raw):
    return raw * 3.3 / 65535

# Funktion: Spannung → Lux (TEMT6000: ca. 2 µA = 1 lx bei 10 kΩ)
def voltage_to_lux(voltage):
    # Strom in µA: I [A] = U [V] / R [Ω]  mit  R = 10 000 Ω  und 1 A = 10^6 µA
    current_uA = voltage * 100       # (volt / 10000) * 1e6 = volt * 100
    # 2 µA entsprechen 1 lx → 1 µA = 0.5 lx
    return current_uA * 0.5

# ────────────────────────────────────────────────────────────────────────────
# 2. I²C und SSD1306 (128×64) einrichten
# ────────────────────────────────────────────────────────────────────────────
i2c = machine.I2C(
    0,                   # I2C-Port 0
    scl=machine.Pin(1),  # SCL → GP1 (physischer Pin 2)
    sda=machine.Pin(0),  # SDA → GP0 (physischer Pin 1)
    freq=400000          # 400 kHz
)

oled_width  = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# ────────────────────────────────────────────────────────────────────────────
# 3. Helfer: Bis zu 4 Zeichen mit Skalierungsfaktor 4 darstellen
# ────────────────────────────────────────────────────────────────────────────
def draw_lux_text(oled_fb, text):
    """
    Zeichnet 'text' (maximal 4 Zeichen) so groß wie möglich (Skalierung 4)
    auf das 128×64-OLED. Längere Strings werden abgeschnitten (erste 4 Zeichen).
    """
    # 1. Auf maximal 4 Zeichen beschränken:
    if len(text) > 4:
        text = text[:4]
    txt_len = len(text)

    # 2. Klein-Framebuffer für 8×8-Font (pro Zeichen 8×8 px)
    w_small = txt_len * 8
    h_small = 8
    buf = bytearray((w_small * h_small) // 8)
    fb_small = framebuf.FrameBuffer(buf, w_small, h_small, framebuf.MONO_HLSB)
    fb_small.fill(0)
    fb_small.text(text, 0, 0, 1)

    # 3. Fester Skalierungsfaktor 4 (damit 4 Zeichen maximal 128 px breit werden)
    scale = 4
    total_w = w_small * scale   # z. B. bei 4 Zeichen: 32 px × 4 = 128 px
    total_h = h_small * scale   # 8 px × 4 = 32 px

    # 4. Zentrieren (optional) – hier horizontal und vertikal
    x_off = (oled_width  - total_w) // 2
    y_off = (oled_height - total_h) // 2

    # 5. OLED leeren und skalierten Text aufmalen
    oled_fb.fill(0)
    for y in range(h_small):
        for x in range(w_small):
            if fb_small.pixel(x, y):
                x0 = x_off + x * scale
                y0 = y_off + y * scale
                for dy in range(scale):
                    for dx in range(scale):
                        oled_fb.pixel(x0 + dx, y0 + dy, 1)
    oled_fb.show()

# ────────────────────────────────────────────────────────────────────────────
# 4. Hauptschleife: Auslesen, Umrechnen, Nur Lux (4 Ziffern) anzeigen
# ────────────────────────────────────────────────────────────────────────────
try:
    while True:
        # 4.1 Sensor lesen und in Lux umwandeln
        raw_value = sensor.read_u16()
        voltage   = raw_to_voltage(raw_value)
        lux       = voltage_to_lux(voltage)
        lux_int   = int(lux)

        # 4.2 REPL-Ausgabe (rein optional)
        print("Lux:", lux_int)

        # 4.3 Nur Lux-Zahl (bis 4 Ziffern) so groß wie möglich anzeigen
        text = str(lux_int)
        draw_lux_text(oled, text)

        time.sleep(1)

except KeyboardInterrupt:
    print("Messung gestoppt")
    oled.fill(0)
    oled.text("Gestoppt", 20, 25)
    oled.show()
