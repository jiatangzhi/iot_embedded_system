# IoT Embedded System

##  Introduction
The aim of this IoT project was to create a remote temperature and humidity sensor with the capability of providing real-time data of its sensor readings.
  
1. The sensor readings would be accessible via the internet on a webpage with added functionality such as current sensor readings, past maximum, and past minimum readings. This was done by creating an IoT device using a `Raspberry Pi Pico`, a `DHT11 sensor`, and an `SD card reader`.
2. Once the *DHT11 sensor* and *SD card* reader were connected to the *Pico*, the *Pico* was connected to a laptop. Using `Thonny`, a Python script was created and loaded onto the *Pico* to generate the temperature and humidity readings, save the sensor data as a JSON file on the *SD card*, and send the sensor readings to pythonanywhere via the internet.
3. The incoming sensor data in pythonanywhere is saved on an *SQL database*. When generating the readings on the website, the data is obtained from the SQL database. The SQL database is used to obtain the latest, maximum, and minimum sensor readings. An *HTML file* is used to create the format for the web page.

##  Project Summary
The project was developed in three phases. 
1. The wiring was done to connect the DHT11 and the SD card reader.
2. We created the Python scripts to perform the various functions needed for the IoT device such as measuring temperature and humidity, connecting to the internet, and sending data to pythonanywhere. Python script was also created on the server side to add the necessary RESTFUL service methods to perform the necessary functions. The SQL database was also created on pythonanywhere so that incoming data could be stored.
3. The report was written to document and explain all the processes in the IoT project.

### Use Case Diagram
<div align="center">
  <img src="https://github.com/jiatangzhi/iot_embedded_system/blob/main/images/use_case_diagram.png" alt="**Figure 1**. Use Case Diagram" width="500"/>
</div>

### Activity Diagrams
<div align="center">
  <img src="https://github.com/jiatangzhi/iot_embedded_system/blob/main/images/activity_diagram_1.png" alt="**Figure 2**. Activity Diagram for Uploading the data" width="300" style="display: inline-block;"/>
  <img src="https://github.com/jiatangzhi/iot_embedded_system/blob/main/images/activity_diagram_2.png" alt="**Figure 3**. Activity Diagram for Real-time Temperature & Humidity data" width="300" style="display: inline-block;"/>
</div>

### Database Diagram
This database diagram represents a table named `temp_and_humidity`. This table has three columns, each with its own data type:

timestamp: This column is of type datetime, which is used to store date and time information. It records when the temperature and humidity data were captured.
temperature_celsius: This column is of type float, which is used to store floating-point numbers. It records the temperature in degrees Celsius.
humidity: This column is also of type float. It records the humidity level as a floating-point number.

The table structure is designed to store time-series data of temperature and humidity readings.
<div align="center">
  <img src="https://github.com/jiatangzhi/iot_embedded_system/blob/main/images/database_diagram.png" alt="**Figure 5**. Database Diagram" width="300"/>
</div>

### Hardware Diagram
<div align="center">
  <img src="https://github.com/jiatangzhi/iot_embedded_system/blob/main/images/hardware_diagram.png" alt="**Figure 4**. Hardware Diagram" width="800"/>
</div>

## RESTFUL Service Methods
Our Flask application includes three primary RESTful service methods:

1. POST /new:<br>
This endpoint accepts a JSON payload to insert a new temperature and humidity reading into the SQL database. It also updates global variables to store the latest readings. This ensures that the most recent sensor data is always readily available.

2. GET /temperature:<br>
This endpoint retrieves the latest temperature and humidity readings along with their timestamps. If no temperature data is found, it returns a `404 Not Found` error with the message *No temperature data available*. This provides a straightforward mechanism for clients to access the most recent environmental conditions.

3. GET /readings:<br>
This endpoint renders an HTML template that displays daily statistics about the temperature and humidity readings. It fetches and presents data such as the earliest and latest timestamps, the minimum and maximum temperature, and the minimum and maximum humidity recorded for the day. This offers a comprehensive summary of the day's environmental data.

---
## Appendix
Latest temperature readings: 
```json
{
    "humidity": 48,
    "status": "success",
    "temp": 26.7,
    "timestamp": "2024-06-25 10:58:13"
}
```

Locally saved sensor readings on SD Card:
```json
{"temp": 27.6, "humidity": 52.0, "timestamp": "2024-06-22 18:17:46"}
{"temp": 27.6, "humidity": 51.0, "timestamp": "2024-06-22 18:18:46"}
```

### SQL Table

```sql
CREATE TABLE `temp_and_humidity` (
  `timestamp` datetime NOT NULL,
  `temperature_celsius` float NOT NULL,
  `humidity` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
