"""
Copyright (c) Project TemperStat. All rights reserved.
by Aditya Borgaonkar & Sahil Gothoskar, 2020.

https://github.com/adityaborgaonkar
https://github.com/SahilGothoskar

TemperStat — Raspberry Pi IoT dashboard for real-time temperature and humidity
monitoring using a DHT11 sensor. Readings are logged to a CSV file and can be
emailed to any recipient via a web form.
"""

# ---------------------------------------------------------------------------
# Standard library imports
# ---------------------------------------------------------------------------
import csv
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE

# ---------------------------------------------------------------------------
# Third-party imports
# ---------------------------------------------------------------------------
import Adafruit_DHT
from flask import Flask, render_template, request

# ---------------------------------------------------------------------------
# Flask application setup
# ---------------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------------
# Sensor configuration
# GPIO pin 17 connected to the DHT11 data line
# ---------------------------------------------------------------------------
SENSOR_PIN = 17
sensor = Adafruit_DHT.DHT11

# ---------------------------------------------------------------------------
# In-memory data store
# Lists accumulate readings for the duration of the running session so the
# dashboard can display historical min / max values and a live chart.
# ---------------------------------------------------------------------------
data_temp = []   # Celsius temperature readings
data_hum = []    # Relative humidity readings (%)
data_time = []   # HH:MM:SS timestamps for each reading

# ---------------------------------------------------------------------------
# Email configuration
# ---------------------------------------------------------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MY_EMAIL = "temperstat@gmail.com"
MY_PASSWORD = "temperstat20"  # NOTE: move to environment variable in production
READINGS_FILE = "readings.csv"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/mail", methods=["POST", "GET"])
def mail():
    """
    Send the accumulated CSV readings to the email address submitted via the
    web form.  The CSV is attached as a file download.
    """
    subject = "IOT Project :: TemperStat Readings"
    to_email = request.form["email"]

    # Build the MIME message with the CSV attached
    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"] = COMMASPACE.join([to_email])
    msg["Subject"] = subject

    # Attach the CSV file as a binary payload
    attachment = MIMEBase("application", "octet-stream")
    with open(READINGS_FILE, "rb") as f:
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition", "attachment", filename=READINGS_FILE
    )
    msg.attach(attachment)

    # Connect to Gmail via TLS, authenticate, and send
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(MY_EMAIL, MY_PASSWORD)
        smtp.sendmail(MY_EMAIL, to_email, msg.as_string())

    return render_template("mail.html", toemail=to_email)


@app.route("/", methods=["POST", "GET"])
def index():
    """
    Main dashboard route.

    - Reads the latest temperature and humidity from the DHT11 sensor.
    - Appends the reading to the in-memory lists and to readings.csv.
    - Passes current, historical, min, and max values to the Jinja2 template.
    """
    # Capture the current time as a human-readable string
    now = datetime.now().strftime("%H:%M:%S")

    # Read sensor data; retries automatically on transient failures
    temperature, humidity = read_sensor()

    # Accumulate readings for historical chart and statistics
    data_temp.append(temperature)
    data_hum.append(humidity)
    data_time.append(now)

    # Compute running statistics across the session
    temperature_max = max(data_temp)
    temperature_min = min(data_temp)
    humidity_max = max(data_hum)
    humidity_min = min(data_hum)

    # Persist the reading to the CSV log file
    with open(READINGS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, temperature, humidity])

    return render_template(
        "index.html",
        temperature=temperature,
        humidity=humidity,
        data_temp=data_temp,
        data_hum=data_hum,
        data_time=data_time,
        temperature_max=temperature_max,
        temperature_min=temperature_min,
        humidity_max=humidity_max,
        humidity_min=humidity_min,
    )


# ---------------------------------------------------------------------------
# Sensor helper
# ---------------------------------------------------------------------------

def read_sensor():
    """
    Read temperature and humidity from the DHT11 sensor.

    Adafruit_DHT.read_retry() retries up to 15 times before giving up,
    handling the sensor's occasional missed reads gracefully.

    Returns:
        (float, float): temperature in °C and relative humidity in %.
    """
    humidity, temperature = Adafruit_DHT.read_retry(sensor, SENSOR_PIN)
    if humidity is not None and temperature is not None:
        return temperature, humidity


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # debug=True enables hot-reload; set to False in production
    app.run(debug=True)




