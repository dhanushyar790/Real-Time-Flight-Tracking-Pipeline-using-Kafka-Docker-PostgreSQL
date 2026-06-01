import json
import time
import psycopg2
from kafka import KafkaConsumer

# Wait for Kafka
while True:
    try:
        consumer = KafkaConsumer(
            "flight-tracker",
            bootstrap_servers="flight-kafka:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="flight-consumer-group"
        )
        print("Connected to Kafka")
        break
    except Exception as e:
        print("Kafka not ready, retrying...")
        time.sleep(5)

# Wait for Postgres
while True:
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="flightdb",
            user="user",
            password="password"
        )
        cursor = conn.cursor()
        print("Connected to Postgres")
        break
    except Exception as e:
        print("Postgres not ready, retrying...")
        time.sleep(5)

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        id SERIAL PRIMARY KEY,
        flight_iata VARCHAR(20),
        airline VARCHAR(100),
        departure_airport VARCHAR(200),
        arrival_airport VARCHAR(200),
        flight_status VARCHAR(50),
        created_at TIMESTAMP DEFAULT NOW()
    )
""")
conn.commit()

# Consume messages
print("Listening for flight messages...")
for message in consumer:
    flight = message.value
    try:
        cursor.execute("""
            INSERT INTO flights (flight_iata, airline, departure_airport, arrival_airport, flight_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            flight.get("flight_iata"),
            flight.get("airline"),
            flight.get("departure_airport"),
            flight.get("arrival_airport"),
            flight.get("flight_status")
        ))
        conn.commit()
        print(f"Saved -> {flight.get('flight_iata')} | {flight.get('departure_airport')} -> {flight.get('arrival_airport')}")
    except Exception as e:
        print("DB Error:", e)
        conn.rollback()