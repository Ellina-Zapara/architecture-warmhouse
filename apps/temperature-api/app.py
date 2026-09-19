import os
import random
import hashlib

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me-in-production")
Session(app)

# ── DB config ────────────────────────────────────────────
DB_HOST     = os.environ.get("DB_HOST", "localhost")
DB_PORT     = os.environ.get("DB_PORT", "5432")
DB_NAME     = os.environ.get("DB_NAME", "smarthome")
DB_USER     = os.environ.get("DB_USER", "smarthome")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "smarthome")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )


# ── Location ↔ sensor mapping (legacy) ───────────────────
LOCATION_BY_SENSOR = {1: "Living Room", 2: "Bedroom", 3: "Kitchen"}
SENSOR_BY_LOCATION  = {v: k for k, v in LOCATION_BY_SENSOR.items()}

# ── Users (simple, for login demo) ────────────────────────
USERS = {"admin": "admin", "user1": "user1"}


# ── Auth ──────────────────────────────────────────────────
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def do_login():
    data      = request.get_json(silent=True) or {}
    username  = data.get("username", "")
    password  = data.get("password", "")

    if username in USERS and USERS[username] == password:
        session["username"] = username
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/index")
def index():
    if "username" in session:
        return render_template("index.html")
    return redirect(url_for("login"))


# ── API: Sensors ─────────────────────────────────────────
@app.route("/api/sensors", methods=["POST"])
def create_sensor():
    data        = request.get_json(silent=True) or {}
    device_id   = data.get("device_id")
    device_type = data.get("type", "sensor")
    location    = data.get("location")

    if not device_id or not location:
        return jsonify({"error": "device_id and location are required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO sensors (device_id, type, location)
                   VALUES (%s, %s, %s)
                   RETURNING id, device_id, type, location, created_at""",
                (device_id, device_type, location),
            )
            row = cur.fetchone()
        conn.commit()
        return jsonify(dict(row)), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": "Sensor with this device_id already exists"}), 409
    finally:
        conn.close()


@app.route("/api/sensors", methods=["GET"])
def get_all_sensors():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, device_id, type, location, created_at FROM sensors ORDER BY id")
            rows = cur.fetchall()
        return jsonify([dict(r) for r in rows]), 200
    finally:
        conn.close()


# ── Temperature (simulated remote sensor) ─────────────────
@app.route("/temperature", methods=["GET"])
def get_temperature():
    location       = request.args.get("location", "").strip()
    sensor_id_raw  = request.args.get("sensorId", "").strip()

    sensor_id = None
    if sensor_id_raw:
        try:
            sensor_id = int(sensor_id_raw)
        except ValueError:
            return jsonify({"error": "sensorId must be an integer"}), 400

    if not location:
        if sensor_id is not None:
            location = LOCATION_BY_SENSOR.get(sensor_id, "Unknown")
        else:
            location = "Unknown"

    if sensor_id is None:
        sensor_id = SENSOR_BY_LOCATION.get(location, 0)

    temperature = round(random.uniform(18.0, 35.0), 1)

    return jsonify({
        "location": location,
        "sensorId": sensor_id,
        "temperature": temperature,
    }), 200


# ── Health ────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "ok", "database": "connected"}), 200
    except Exception:
        return jsonify({"status": "degraded", "database": "unreachable"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
