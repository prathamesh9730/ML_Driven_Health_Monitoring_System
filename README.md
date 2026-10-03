# ML_Driven_Health_Monitoring_System

This project is an **IoT and Machine Learning based health monitoring system** that I developed to monitor basic health parameters in real time and understand how IoT, Python, and Machine Learning can work together in a practical application.

The system uses a **NodeMCU ESP8266** connected to sensors such as the **MAX30102** and **DS18B20**. The MAX30102 is used to collect **heart rate and SpO₂ readings**, while the DS18B20 measures **temperature**. The readings can also be displayed on an OLED screen so they can be viewed directly from the hardware.

The sensor data is sent from the NodeMCU to a Python application through **serial communication**. Python processes the incoming data and passes the readings to a trained **Random Forest Machine Learning model**. Based on the heart rate, SpO₂, and temperature values, the model classifies the current condition into three categories: **Normal, Warning, or Critical**.

One of the main features I added is **real-time Telegram notification**. When the system detects a condition that needs attention, it can send a notification through a Telegram bot. This makes the system more useful because the user does not have to continuously watch the sensor readings.

The project also uses **Google Sheets** to store the collected health data. This provides a simple way to maintain a history of readings and review previous results.

### Technologies Used

* Python
* Machine Learning
* Random Forest Classifier
* Arduino / C++
* NodeMCU ESP8266
* MAX30102
* DS18B20
* OLED Display
* Telegram Bot
* Google Sheets
* Pandas
* NumPy
* Scikit-learn
* PySerial
* Joblib

### Project Workflow

**Sensors → NodeMCU → Serial Communication → Python → ML Model → Health Prediction → Telegram Notification → Google Sheets**
