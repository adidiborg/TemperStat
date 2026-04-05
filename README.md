# TemperStat 🌡️

<p align="center">
  <img src="https://www.raspberrypi.org/app/uploads/2018/03/RPi-Logo-Reg-SCREEN-199x250.png" alt="Raspberry Pi" width="80" />
</p>

<p align="center">
  <strong>Real-time Temperature &amp; Humidity Dashboard</strong><br/>
  Powered by Raspberry Pi 4 &bull; DHT11 Sensor &bull; Flask
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Raspberry%20Pi-4-c51a4a?logo=raspberrypi&logoColor=white" alt="Raspberry Pi" />
  <img src="https://img.shields.io/badge/Sensor-DHT11-green" alt="DHT11" />
  <img src="https://img.shields.io/badge/CSS-Bulma-00d1b2?logo=bulma&logoColor=white" alt="Bulma CSS" />
</p>

---

## 📖 About

**TemperStat** is an IoT project that reads temperature (°C) and humidity (%) from a **DHT11 sensor** connected to a **Raspberry Pi 4** via GPIO pin 17, and serves a live dashboard using **Flask**. Readings auto-refresh every 5 seconds and are logged to a CSV file that can be emailed to any address directly from the web UI.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌡️ **Live Temperature** | Current reading in °C with session min / max |
| 💧 **Live Humidity** | Current reading in % with session min / max |
| 📊 **Historical Table** | Last 11 readings displayed in a clean table |
| 📧 **Email Export** | Enter an email address → receive `readings.csv` as an attachment |
| 🔄 **Auto-Refresh** | Dashboard refreshes every 5 seconds for near-real-time updates |
| 📝 **CSV Logging** | Every reading is appended to `readings.csv` with a timestamp |

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| **Hardware** | Raspberry Pi 4, DHT11 sensor |
| **Backend** | Python 3, Flask |
| **Sensor Library** | `Adafruit_DHT` |
| **Frontend** | Jinja2 templates, [Bulma CSS](https://bulma.io), Font Awesome icons |
| **Email** | `smtplib` via Gmail SMTP (TLS) |
| **Data Store** | In-memory lists (session) + `readings.csv` (persistent) |

---

## 🗂️ Project Structure

```
TemperStat/
├── app.py              # Flask application — routes, sensor reading, email
├── readings.csv        # Append-only log of all sensor readings
├── templates/
│   ├── index.html      # Main dashboard — live stats, table, email form
│   └── mail.html       # Confirmation page after successful email send
├── LICENSE
└── README.md
```

---

## 🔌 Hardware Setup

```
Raspberry Pi 4 GPIO
─────────────────────
  Pin 1  (3.3 V)  ──→  DHT11 VCC
  Pin 7  (GPIO 17) ──→  DHT11 DATA
  Pin 9  (GND)    ──→  DHT11 GND
```

> A 10 kΩ pull-up resistor between VCC and DATA is recommended for reliable reads.

---

## 🚀 Getting Started

### Prerequisites

- Raspberry Pi 4 running Raspbian / Raspberry Pi OS
- Python 3 installed
- DHT11 sensor wired to **GPIO 17**

### Installation

```bash
# Clone the repository
git clone https://github.com/SahilGothoskar/TemperStat.git
cd TemperStat

# Install dependencies
pip install flask Adafruit_DHT

# Run the application
python app.py
```

The dashboard will be available at **http://localhost:5000**.

---

## 🛣️ Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/`      | Reads the sensor, logs the data, and renders the dashboard |
| `POST` | `/mail`  | Sends `readings.csv` to the email address from the form |

---

## 📧 Email Configuration

The app sends mail through Gmail SMTP. Update the following constants in `app.py` to use your own credentials:

```python
MY_EMAIL   = "your-email@gmail.com"
MY_PASSWORD = "your-app-password"
```

> **Tip:** Use a [Gmail App Password](https://support.google.com/accounts/answer/185833) instead of your account password.

---

## 📄 CSV Format

Readings are appended to `readings.csv` with the following columns:

| Column | Example |
|--------|---------|
| Time | `14:32:07` |
| Temperature | `28` |
| Humidity | `65` |

---

## ⚠️ Notes

- The dashboard **auto-refreshes every 5 seconds** (`<meta http-equiv="refresh" content="5">`), so every page load triggers a new sensor read.
- In-memory lists (`data_temp`, `data_hum`, `data_time`) reset when the Flask process restarts. The CSV file persists across restarts.
- `Adafruit_DHT.read_retry()` retries up to 15 times internally to handle the sensor's occasional missed reads.

---

## 👥 Authors

| | Name | GitHub |
|---|------|--------|
| 🧑‍💻 | **Sahil Gothoskar** | [@SahilGothoskar](https://github.com/SahilGothoskar) |
| 🧑‍💻 | **Aditya Borgaonkar** | [@adityaborgaonkar](https://github.com/adityaborgaonkar) |

---

<p align="center">Made with ❤️ on a Raspberry Pi</p>
