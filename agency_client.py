import random
import time
from datetime import datetime

import requests

# ***** - Miejsce na wpisanie adresu IP serwera hotelowego
HOTEL_URL = "http://*****:5001"


for i in range(10):
    max_acceptable_price = random.randint(400, 600)

    request_payload = {
        "current_date": "2026-06-03",
        "checkin": "2026-08-14",
        "checkout": "2026-08-17",
        "guests": random.choice([1, 2, 3]),
        "room_type": random.choice(["single", "double", "suite"]),
        "breakfast": random.choice([True, False]),
        "context": {
            "city": random.choice(["Warszawa", "Wrocław", "Kraków"]),
            "device": random.choice(["iPhone", "Android", "Laptop"]),
            "returning_client": random.choice([True, False])
        }
    }

    print(f"\n[AGENCJA] ===== Zapytanie nr {i + 1} =====")
    print("[AGENCJA] Czas:", datetime.now().strftime("%H:%M:%S"))
    print("[AGENCJA] Losowy próg akceptacji:", max_acceptable_price)
    print("[AGENCJA] Wysyłam zapytanie:", request_payload)

    try:
        response = requests.post(f"{HOTEL_URL}/offer", json=request_payload, timeout=5)
        response.raise_for_status()
        offer = response.json()
    except requests.RequestException as e:
        print("[AGENCJA] Błąd przy wysyłaniu zapytania:", e)
        if i < 9:
            print("[AGENCJA] Czekam 10 sekund do kolejnej próby...")
            time.sleep(10)
        continue

    print("[AGENCJA] Otrzymana oferta:", offer)

    decision_value = "accept" if offer["price"] <= max_acceptable_price else "reject"

    decision_payload = {
        "offer_id": offer["offer_id"],
        "decision": decision_value
    }

    print(f"[AGENCJA] Decyzja: {decision_value}")

    try:
        response2 = requests.post(f"{HOTEL_URL}/decision", json=decision_payload, timeout=5)
        response2.raise_for_status()
        print("[AGENCJA] Odpowiedź hotelu:", response2.json())
    except requests.RequestException as e:
        print("[AGENCJA] Błąd przy wysyłaniu decyzji:", e)

    if i < 9:
        print("[AGENCJA] Czekam 10 sekund do następnego zapytania...")
        time.sleep(10)

print("\n[AGENCJA] Koniec testu.")