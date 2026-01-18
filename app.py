from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Flower state
flower_state = {
    "day": 1,
    "growth": 100,
    "last_watered": None
}

MAX_GROWTH = 200
GROWTH_STEP = 20

def check_flower_death():
    """Reset flower if not watered in 24 hours"""
    last = flower_state["last_watered"]
    if last:
        last_date = datetime.fromisoformat(last)
        if datetime.now() - last_date > timedelta(hours=24):
            flower_state["day"] = 1
            flower_state["growth"] = 100
            flower_state["last_watered"] = None
            return True
    return False

# your routes here
@app.route("/flower", methods=["GET"])
def get_flower():
    # return JSON data
    check_flower_death()
    return jsonify({"day": 1, "growth": 100, "last_watered": None})

@app.route("/water", methods=["POST"])
def water_flower():
    if check_flower_death():
        # Flower died, starting over
        return jsonify(flower_state)

    today = datetime.now().date().isoformat()
    last = flower_state["last_watered"]

    if last != today:
        # Increase growth and day
        flower_state["growth"] = min(flower_state["growth"] + GROWTH_STEP, MAX_GROWTH)
        flower_state["day"] = min(flower_state["day"] + 1, 7)
        flower_state["last_watered"] = datetime.now().isoformat()

    return jsonify(flower_state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # important for deployment
