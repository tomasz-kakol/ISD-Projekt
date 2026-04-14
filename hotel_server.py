from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

offers = {}


@app.post("/offer")
def create_offer():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Brak poprawnego JSON-a"}), 400

    offer_id = str(uuid4())
    price = 500.0

    offers[offer_id] = {
        "request": data,
        "price": price,
        "status": "pending"
    }

    print("\n[HOTEL] Otrzymano zapytanie:")
    print(data)
    print(f"[HOTEL] Wysłano ofertę: offer_id={offer_id}, price={price}")

    return jsonify({
        "offer_id": offer_id,
        "price": price,
        "valid_seconds": 30
    })


@app.post("/decision")
def handle_decision():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Brak poprawnego JSON-a"}), 400

    offer_id = data.get("offer_id")
    decision = data.get("decision")

    if offer_id not in offers:
        return jsonify({"error": "Nieznane offer_id"}), 404

    if decision not in {"accept", "reject"}:
        return jsonify({"error": "decision musi być 'accept' albo 'reject'"}), 400

    offers[offer_id]["status"] = decision

    print(f"[HOTEL] Decyzja dla {offer_id}: {decision}")

    return jsonify({
        "status": "ok",
        "offer_id": offer_id,
        "final_status": decision
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)