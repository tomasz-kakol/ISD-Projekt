import random
import time
from abc import ABC, abstractmethod
from datetime import date, timedelta

import requests

# W miejscu ***** wstawiamy adres IP serwera hotelowego
HOTEL_URL = "http://*****:5001"


def next_weekday(d: date, target_weekday: int) -> date:
    """
    weekday: Monday=0, ..., Sunday=6
    Zwraca najbliższy przyszły dzień tygodnia.
    """
    delta = (target_weekday - d.weekday()) % 7
    if delta == 0:
        delta = 7
    return d + timedelta(days=delta)


class BasePersona(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.pending_price_limits = []

    @abstractmethod
    def generate_requests(self, current_date: date) -> list[dict]:
        pass

    def decide(self, offers: list[dict]) -> str | None:
        """
        Zwraca offer_id wybranej oferty albo None.
        Na razie zakładamy, że dla jednego zapytania dostajemy listę ofert
        i wybieramy najtańszą, o ile mieści się w limicie.
        """
        if not offers:
            return None

        if not self.pending_price_limits:
            print(f"[{self.name}] Brak zapamiętanego limitu ceny.")
            return None

        max_acceptable_price = self.pending_price_limits.pop(0)

        acceptable_offers = [
            offer for offer in offers if offer["price"] <= max_acceptable_price
        ]

        if not acceptable_offers:
            print(
                f"[{self.name}] Odrzuca ofertę/oferty. "
                f"Limit = {max_acceptable_price}, ceny = {[o['price'] for o in offers]}"
            )
            return None

        best_offer = min(acceptable_offers, key=lambda x: x["price"])

        print(
            f"[{self.name}] Akceptuje ofertę {best_offer['offer_id']}. "
            f"Limit = {max_acceptable_price}, cena = {best_offer['price']}"
        )

        return best_offer["offer_id"]


class LastMinutePersona(BasePersona):
    """
    Klient last-minute:
    - rezerwuje na 1-3 dni do przodu,
    - pobyt 1-3 dni,
    - ma niski/średni budżet,
    - generuje 0-2 zapytań dziennie, równomiernie.
    """

    def __init__(self):
        super().__init__(
            name="LastMinute",
            description="Rezerwuje na ostatnią chwilę i poluje na niskie ceny."
        )

    def generate_requests(self, current_date: date) -> list[dict]:
        requests_for_today = []

        num_requests = random.randint(0, 2)

        for _ in range(num_requests):
            lead_days = random.randint(1, 3)
            stay_length = random.randint(1, 3)

            checkin = current_date + timedelta(days=lead_days)
            checkout = checkin + timedelta(days=stay_length)

            max_price = random.randint(400, 600)
            self.pending_price_limits.append(max_price)

            payload = {
                "current_date": current_date.isoformat(),
                "checkin": checkin.isoformat(),
                "checkout": checkout.isoformat(),
                "guests": random.choice([1, 2]),
                "room_type": random.choice(["single", "double"]),
                "breakfast": random.choice([True, False]),
                "context": {
                    "city": random.choice(["Wrocław", "Warszawa", "Kraków"]),
                    "device": random.choice(["iPhone", "Android", "Laptop"]),
                    "returning_client": random.choice([True, False]),
                }
            }

            print(
                f"[{self.name}] Generuje zapytanie. "
                f"Termin za {lead_days} dni, długość {stay_length} dni, limit {max_price}"
            )

            requests_for_today.append(payload)

        print(f"[{self.name}] Liczba zapytań dziś: {num_requests}")
        return requests_for_today


class WeekendPremiumPersona(BasePersona):
    """
    Klient z wysoką akceptacją ceny:
    - najczęściej celuje w piątek/sobotę,
    - czasem także w dni robocze,
    - pobyt zawsze 7 dni,
    - ma wysoki budżet,
    - generuje 0-2 zapytań dziennie, równomiernie.
    """

    def __init__(self):
        super().__init__(
            name="WeekendPremium",
            description="Preferuje weekendowe przyjazdy i ma wysoki budżet."
        )

    def generate_requests(self, current_date: date) -> list[dict]:
        requests_for_today = []

        num_requests = random.randint(0, 2)

        for _ in range(num_requests):
            if random.random() < 0.80:
                target_weekday = random.choice([4, 5])  # Friday, Saturday
            else:
                target_weekday = random.choice([0, 1, 2, 3])  # Mon-Thu

            checkin = next_weekday(current_date, target_weekday)
            checkout = checkin + timedelta(days=7)

            max_price = random.randint(1000, 1200)
            self.pending_price_limits.append(max_price)

            payload = {
                "current_date": current_date.isoformat(),
                "checkin": checkin.isoformat(),
                "checkout": checkout.isoformat(),
                "guests": 2,
                "room_type": random.choice(["double", "suite"]),
                "breakfast": True,
                "context": {
                    "city": random.choice(["Warszawa", "Poznań", "Gdańsk"]),
                    "device": random.choice(["iPhone", "MacBook", "Android"]),
                    "returning_client": random.choice([True, False]),
                }
            }

            print(
                f"[{self.name}] Generuje zapytanie. "
                f"Check-in: {checkin}, checkout: {checkout}, limit {max_price}"
            )

            requests_for_today.append(payload)

        print(f"[{self.name}] Liczba zapytań dziś: {num_requests}")
        return requests_for_today
class RareLongStaySuitePersona(BasePersona):
    """
    Rzadki klient:
    - średnio pojawia się raz na 2 dni (50% szans dziennie),
    - jeśli już wysyła zapytanie, to tylko jedno,
    - zawsze bierze suite,
    - zawsze na 21 dni,
    - ma wysoki budżet.
    """

    def __init__(self):
        super().__init__(
            name="RareLongStaySuite",
            description="Rzadki klient na długi pobyt w suite."
        )

    def generate_requests(self, current_date: date) -> list[dict]:
        requests_for_today = []

        # średnio raz na 2 dni
        if random.random() >= 0.5:
            print(f"[{self.name}] Dziś nie generuje zapytania.")
            return requests_for_today

        # np. rezerwacja kilka-kilkanaście dni do przodu
        lead_days = random.randint(3, 14)
        checkin = current_date + timedelta(days=lead_days)
        checkout = checkin + timedelta(days=21)

        max_price = random.randint(1000, 1200)
        self.pending_price_limits.append(max_price)

        payload = {
            "current_date": current_date.isoformat(),
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
            "guests": random.choice([1, 2]),
            "room_type": "suite",
            "breakfast": random.choice([True, False]),
            "context": {
                "city": random.choice(["Warszawa", "Kraków", "Gdańsk", "Wrocław"]),
                "device": random.choice(["iPhone", "Android", "Laptop"]),
                "returning_client": random.choice([True, False]),
            }
        }

        print(
            f"[{self.name}] Generuje zapytanie. "
            f"Suite, pobyt 21 dni, termin za {lead_days} dni, limit {max_price}"
        )

        requests_for_today.append(payload)
        return requests_for_today

class Agency:
    def __init__(self, hotel_url: str, personas: list[BasePersona]):
        self.hotel_url = hotel_url
        self.personas = personas
        self.accepted = 0
        self.rejected = 0

    def send_request_to_hotel(self, request_payload: dict) -> dict | None:
        try:
            response = requests.post(
                f"{self.hotel_url}/offer",
                json=request_payload,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print("[AGENCJA] Błąd przy wysyłaniu zapytania do hotelu:", e)
            return None

    def send_decision_to_hotel(self, offer_id: str, decision: str) -> None:
        try:
            response = requests.post(
                f"{self.hotel_url}/decision",
                json={"offer_id": offer_id, "decision": decision},
                timeout=5
            )
            response.raise_for_status()
            print("[AGENCJA] Potwierdzenie od hotelu:", response.json())
        except requests.RequestException as e:
            print("[AGENCJA] Błąd przy wysyłaniu decyzji:", e)

    def build_daily_schedule(self, current_date: date) -> list[tuple[int, int, BasePersona, dict]]:
        """
        Zwraca listę zdarzeń w postaci:
        (hour, minute, persona, request_payload)
        posortowaną chronologicznie.
        """
        events = []

        for persona in self.personas:
            requests_for_today = persona.generate_requests(current_date)

            for request_payload in requests_for_today:
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                events.append((hour, minute, persona, request_payload))

        events.sort(key=lambda x: (x[0], x[1]))
        return events

    def run(self, start_date: date, days: int, sleep_between_events: float = 1.0) -> None:
        for day_offset in range(days):
            current_date = start_date + timedelta(days=day_offset)

            print("\n" + "=" * 80)
            print(f"[AGENCJA] Dzień symulacji: {current_date}")
            print("=" * 80)

            daily_events = self.build_daily_schedule(current_date)

            if not daily_events:
                print("[AGENCJA] Brak zapytań tego dnia.")
                print(
                    f"[AGENCJA] Statystyki: accept={self.accepted}, reject={self.rejected}"
                )
                continue

            print(f"[AGENCJA] Liczba wszystkich zapytań dziś: {len(daily_events)}")

            last_hour = None
            last_minute = None

            for hour, minute, persona, request_payload in daily_events:
                if (hour, minute) != (last_hour, last_minute):
                    print(f"\n[AGENCJA] Czas symulacyjny: {hour:02d}:{minute:02d}")
                    last_hour, last_minute = hour, minute

                print(f"[AGENCJA] Wysyłam zapytanie od persony {persona.name}")
                print(f"[AGENCJA] Payload: {request_payload}")

                offer = self.send_request_to_hotel(request_payload)

                if offer is None:
                    continue

                print(f"[AGENCJA] Oferta od hotelu: {offer}")

                chosen_offer_id = persona.decide([offer])

                if chosen_offer_id is None:
                    decision = "reject"
                    self.rejected += 1
                else:
                    decision = "accept"
                    self.accepted += 1

                self.send_decision_to_hotel(offer["offer_id"], decision)

                print(
                    f"[AGENCJA] Statystyki do tej pory: "
                    f"accept={self.accepted}, reject={self.rejected}"
                )

                time.sleep(sleep_between_events)

    def run_one_day(self, current_date: date, sleep_between_events: float = 1.0) -> None:
        """
        Wygodna metoda pomocnicza do testowania tylko jednego dnia.
        """
        print("\n" + "=" * 80)
        print(f"[AGENCJA] Dzień symulacji: {current_date}")
        print("=" * 80)

        daily_events = self.build_daily_schedule(current_date)

        if not daily_events:
            print("[AGENCJA] Brak zapytań tego dnia.")
            return

        print(f"[AGENCJA] Liczba wszystkich zapytań dziś: {len(daily_events)}")

        for hour, minute, persona, request_payload in daily_events:
            print(f"\n[AGENCJA] Czas symulacyjny: {hour:02d}:{minute:02d}")
            print(f"[AGENCJA] Wysyłam zapytanie od persony {persona.name}")

            offer = self.send_request_to_hotel(request_payload)

            if offer is None:
                continue

            print(f"[AGENCJA] Oferta od hotelu: {offer}")

            chosen_offer_id = persona.decide([offer])

            if chosen_offer_id is None:
                decision = "reject"
                self.rejected += 1
            else:
                decision = "accept"
                self.accepted += 1

            self.send_decision_to_hotel(offer["offer_id"], decision)

            print(
                f"[AGENCJA] Statystyki do tej pory: "
                f"accept={self.accepted}, reject={self.rejected}"
            )

            time.sleep(sleep_between_events)


if __name__ == "__main__":
    personas = [
        LastMinutePersona(),
        WeekendPremiumPersona(),
        RareLongStaySuitePersona(),
    ]

    agency = Agency(HOTEL_URL, personas)

    # Wersja wielodniowa:
    agency.run(start_date=date(2026, 6, 1), days=5, sleep_between_events=1.0)

    # Albo do testu jednego dnia:
    # agency.run_one_day(current_date=date(2026, 6, 1), sleep_between_events=1.0)