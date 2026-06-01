import json
import time
import requests
from kafka import KafkaProducer

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx"

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="flight-kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print("Connected to Kafka")
        break
    except Exception as e:
        print("Kafka not ready:", e)
        time.sleep(5)

TOPIC = "flight-tracker"

while True:
    try:
        response = requests.get(
            f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}",
            timeout=30
        )

        print("=" * 50)
        print("REQUEST URL:", response.url)
        print("STATUS CODE:", response.status_code)
        print("RESPONSE:")
        print(response.text[:1000])
        print("=" * 50)

        data = response.json()

        if "data" not in data:
            print("No flight data found.")
            time.sleep(60)
            continue

        for flight in data["data"][:20]:
            record = {
                "flight_iata": flight.get("flight", {}).get("iata"),
                "airline": flight.get("airline", {}).get("name"),
                "departure_airport": flight.get("departure", {}).get("airport"),
                "arrival_airport": flight.get("arrival", {}).get("airport"),
                "flight_status": flight.get("flight_status")
            }

            producer.send(TOPIC, value=record)

            print(
                f"Sent -> {record['flight_iata']} | "
                f"{record['departure_airport']} -> "
                f"{record['arrival_airport']}"
            )

        producer.flush()

    except Exception as e:
        print("Producer Error:", e)

    time.sleep(300)