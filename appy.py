"""
Flask REST API for Drone-based Intelligent ET Sensing System
and Irrigation Water Use Accounting System.

Endpoints:
GET  /health         -> API Health Check
GET  /sensor-info    -> Sensor Information
POST /predict        -> Predict irrigation requirement
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sensor Information
SENSOR_INFO = {
    "temperature": {
        "label": "Temperature (°C)",
        "min": 0,
        "max": 50,
        "default": 30
    },
    "humidity": {
        "label": "Humidity (%)",
        "min": 0,
        "max": 100,
        "default": 65
    },
    "soil_moisture": {
        "label": "Soil Moisture (%)",
        "min": 0,
        "max": 100,
        "default": 40
    },
    "et_value": {
        "label": "Evapotranspiration (mm/day)",
        "min": 0,
        "max": 10,
        "default": 4
    }
}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "message": "Drone ET Sensing API is Running Successfully"
    })


@app.route("/sensor-info", methods=["GET"])
def sensor_info():
    return jsonify(SENSOR_INFO)


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    temperature = float(data.get("temperature", 0))
    humidity = float(data.get("humidity", 0))
    soil = float(data.get("soil_moisture", 0))
    et = float(data.get("et_value", 0))

    # Simple Irrigation Logic
    if soil < 30 and et > 5:
        irrigation = "High Irrigation Required"
        water = 50

    elif soil < 50 and et > 3:
        irrigation = "Moderate Irrigation Required"
        water = 30

    else:
        irrigation = "No Irrigation Required"
        water = 10

    return jsonify({

        "temperature": temperature,
        "humidity": humidity,
        "soil_moisture": soil,
        "et_value": et,

        "irrigation_status": irrigation,
        "recommended_water_liters": water,

        "drone_status": "Field Successfully Scanned",

        "recommendation":
        "Monitor soil moisture regularly for efficient irrigation."

    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
