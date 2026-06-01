# ✈️ Real-Time Flight Tracking Data Pipeline

A real-time data engineering project that streams live flight data using Apache Kafka, processes it with a Python consumer, and stores it in PostgreSQL. The entire system is containerized using Docker Compose.

---

## 🚀 Project Architecture

Flight API → Kafka Producer → Kafka Topic → Kafka Consumer → PostgreSQL

---

## 📌 Features

- Fetch live flight data from AviationStack API
- Stream data using Apache Kafka
- Producer–Consumer architecture
- Store processed data in PostgreSQL
- Fully containerized using Docker Compose
- Retry mechanism for Kafka and PostgreSQL connection stability

---

## 🛠️ Tech Stack

Python, Apache Kafka, Zookeeper, PostgreSQL, Docker, Docker Compose, REST API

---

## 📂 Project Structure

.
├── docker-compose.yml
├── Dockerfile
├── flight-producer.py
├── flight-consumer.py
├── requirements.txt
└── README.md

---

## 📊 PostgreSQL Table Schema

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    flight_iata VARCHAR(20),
    airline VARCHAR(100),
    departure_airport VARCHAR(200),
    arrival_airport VARCHAR(200),
    flight_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

---

## 🔄 Data Flow

1. Producer fetches data from AviationStack API  
2. Data is sent to Kafka topic `flight-tracker`  
3. Consumer reads messages from Kafka  
4. Data is stored in PostgreSQL database  

---

## 📈 Future Improvements

- Streamlit dashboard for live tracking  
- Real-time analytics and visualization  
- Deploy on AWS / GCP  
- Flight delay prediction using ML  

---

## 👨‍💻 Author

DHANUSHYA R
GitHub:https://github.com/dhanushyar790
LinkedIn: www.linkedin.com/in/dhanushyaravichandran
