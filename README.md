# TEMT6000‐Luxmesser mit Raspberry Pi Pico und SSD1306-OLED

Dieses Projekt liest mit einem TEMT6000-Lichtsensor die Umgebungshelligkeit aus, rechnet den Messwert in Lux um und zeigt ihn auf einem 128 × 64-SSD1306-OLED an. Die Firmware läuft unter MicroPython auf einem Raspberry Pi Pico.

---

## Inhaltsverzeichnis

1. [Projektübersicht](#projektübersicht)  
2. [Benötigte Hardware](#benötigte-hardware)  
3. [Verkabelung](#verkabelung)  
4. [Software und Bibliotheken](#software-und-bibliotheken)  
5. [Installation und Setup](#installation-und-setup)  

---

## Projektübersicht

Mit diesem Projekt kannst du in Echtzeit die Umgebungshelligkeit in Lux messen und auf einem kleinen OLED-Display darstellen.  
- **Sensor:** TEMT6000 (Fototransistor + 10 kΩ-Vorwiderstand)  
- **Mikrocontroller:** Raspberry Pi Pico (MicroPython)  
- **Anzeige:** SSD1306-OLED (I²C, 128 × 64 Pixel)  

Das Skript liest den analogen Ausgang des TEMT6000, rechnet über ADC → Spannung → Sensorstrom → Lux um und aktualisiert jede Sekunde das Display. Dabei werden bis zu vier Ziffern (maximaler Luxwert) in optimaler Großschrift zentriert dargestellt.

---

## Benötigte Hardware

1. **Raspberry Pi Pico** (Micro-USB-Port, MicroPython-Firmware)  
2. **TEMT6000-Lichtsensor** (Breakout-Modul mit 10 kΩ-Widerstand)  
3. **SSD1306-OLED-Display** (128 × 64 Pixel, I²C, 3.3 V)  
4. **Jumper-Kabel** (male-female oder male-male, je nach Breakout-Pin-Header)  
5. **Micro-USB-Kabel** (für Strom und Thonny-Flashen)  
6. (Optional) **Breadboard** für saubere, fixe Verkabelung  

---

## Verkabelung

> **Hinweis:** Alle Komponenten arbeiten mit 3.3 V–Logik. Auf keinen Fall 5 V an GPIO-Pins anlegen!

### 1. TEMT6000 → Pico

- **TEMT6000 VCC** → **Pico 3V3 (Pin 36)**  
- **TEMT6000 GND** → **Pico GND (Pin 38)**  
- **TEMT6000 OUT** → **Pico GPIO26/ADC0 (Pin 31)**  

### 2. SSD1306 OLED (128×64) → Pico (I²C 0)

- **OLED VCC** → **Pico 3V3 (ebenfalls Pin 36)**  
- **OLED GND** → **Pico GND (Pin 38)**  
- **OLED SDA** → **Pico GPIO0 (SDA, Pin 1)**  
- **OLED SCL** → **Pico GPIO1 (SCL, Pin 2)**  

> Beide I²C-Leitungen (SDA, SCL) benötigen keine Pull-Ups, da das SSD1306-Modul i. d. R. bereits welche onboard hat.  
> Falls dein Modul keine Pull-Ups enthält, solltest du je 4.7 kΩ Pull-Ups von SDA/SCL auf 3.3 V ergänzen.



---

## Software und Bibliotheken

1. **MicroPython-Firmware**  
   - Lade die neueste MicroPython-Firmware für den Raspberry Pi Pico von [micropython.org/download/rp2-pico](https://micropython.org/download/rp2-pico/).  
   - Flashe die `.uf2`-Datei auf den Pico (Boot-Knopf gedrückt halten, Verbindung via USB, dann kopieren).

2. **Thonny IDE**  
   - Empfohlen: Thonny 3.3x (mit MicroPython-Unterstützung).  
   - Konfiguriere in Thonny oben rechts den Interpreter auf „MicroPython (Raspberry Pi Pico)“.

3. **ssd1306.py Bibliothek**  
   - Benötigt für SSD1306-Ansteuerung via I²C.  
   - Lade das Treiber-Modul `sdd1306.py` 
   - **In Thonny**:  
     1. Öffne `ssd1306.py` lokal auf deinem PC.  
     2. In Thonny auf den Pico verbunden → „Datei → Speichern unter... → Raspberry Pi Pico“ → Datei-Name: `ssd1306.py`.  
     3. Damit liegt die Bibliothek direkt im Root-Verzeichnis des Pico–Dateisystems.

---

## Installation und Setup

1. **Pico flashen**  
   - Vergewissere dich, dass der Pico mit MicroPython läuft 

2. **ssd1306.py auf den Pico kopieren**  
   - Wie oben beschrieben, unter dem Dateinamen `ssd1306.py` im Stammverzeichnis abspeichern.

3. **Code auf den Pico kopieren**  
   - Erstelle in Thonny eine neue Datei, z. B. `main.py`. Füge den folgenden Code ein:
