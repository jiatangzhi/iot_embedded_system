from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Initialize MySQL connection
db = mysql.connector.connect(
    host="jiatangzhi.mysql.pythonanywhere-services.com",
    user="jiatangzhi",
    password="emlyonmcgill",
    database="jiatangzhi$sensor_readings"
)

cursor = db.cursor()

# Global variables to store the latest readings
latest_temperature = None
latest_humidity = None
latest_timestamp = None

@app.route('/')
def default_response():
    return "<b>Hello</b>"

@app.route('/new', methods=["POST"])
def new_record():
    global latest_temperature, latest_humidity, latest_timestamp

    my_json = request.get_json()

    temperature = my_json['temp']
    humidity = my_json['humidity']
    timestamp = my_json['timestamp']

    # Update the global variables
    latest_temperature = temperature
    latest_humidity = humidity
    latest_timestamp = timestamp

    print(f"Timestamp: {timestamp}")
    print(f"The temperature received is {temperature}.")
    print(f"The humidity received is {humidity}.")

    # Insert data into the database
    insert_query = "INSERT INTO temp_and_humidity (timestamp, temperature_celsius, humidity) VALUES (%s, %s, %s)"
    insert_data = (timestamp, temperature, humidity)

    cursor.execute(insert_query, insert_data)
    db.commit()

    data = {"status": "success", "temp": temperature, "humidity": humidity, "timestamp": timestamp}
    return jsonify(data), 200

@app.route('/temperature', methods=["GET"])
def get_temperature():
    if latest_temperature is None:
        return jsonify({"status": "error", "message": "No temperature data available"}), 404

    data = {
        "status": "success",
        "temp": latest_temperature,
        "humidity": latest_humidity,
        "timestamp": latest_timestamp
    }
    return jsonify(data), 200

@app.route('/readings', methods=["GET"])
def show_readings():
    # Fetch earliest and latest readings for the day
    query_min_max = """
        SELECT
            MIN(timestamp),
            MAX(timestamp),
            MIN(temperature_celsius),
            MAX(temperature_celsius),
            MIN(humidity),
            MAX(humidity)
        FROM
            temp_and_humidity
    """
    cursor.execute(query_min_max)
    result_min_max = cursor.fetchone()

    earliest_timestamp, latest_timestamp, min_temp, max_temp, min_humidity, max_humidity = result_min_max

    # Fetch the latest reading
    query_latest = """
        SELECT
            timestamp,
            temperature_celsius,
            humidity
        FROM
            temp_and_humidity
        ORDER BY
            timestamp DESC
        LIMIT 1
    """
    cursor.execute(query_latest)
    result_latest = cursor.fetchone()

    latest_timestamp, latest_temp, latest_humidity = result_latest

    return render_template(
        'readings.html',
        earliest_timestamp=earliest_timestamp,
        latest_timestamp=latest_timestamp,
        min_temp=min_temp,
        max_temp=max_temp,
        min_humidity=min_humidity,
        max_humidity=max_humidity,
        latest_temp=latest_temp,
        latest_humidity=latest_humidity
    )

# Uncomment the following line to run the app
# app.run(host='0.0.0.0')