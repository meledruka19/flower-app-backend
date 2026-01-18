import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow all domains for now


# Path to flower state file
FLOWER_STATE_FILE = "backend/flower_state.json"

# Helper to load state
def load_flower_state():
    if not os.path.exists(FLOWER_STATE_FILE):
        # default state if file doesn't exist
        return {"day": 0, "growth": 0, "last_watered": None}
    with open(FLOWER_STATE_FILE, "r") as f:
        return json.load(f)

# Helper to save state
def save_flower_state(state):
    with open(FLOWER_STATE_FILE, "w") as f:
        json.dump(state, f)

@app.route("/flower", methods=["GET"])
def get_flower():
    state = load_flower_state()
    return jsonify(state)

@app.route("/flower/water", methods=["POST"])
def water_flower():
    state = load_flower_state()
    # update growth and last watered time
    state["growth"] = min(state.get("growth", 0) + 10, 100)  # max 100%
    state["last_watered"] = datetime.utcnow().isoformat() + "Z"
    save_flower_state(state)
    return jsonify(state)

@app.route("/flower/reset", methods=["POST"])
def reset_flower():
    state = {"day": 0, "growth": 0, "last_watered": None}
    save_flower_state(state)
    return jsonify(state)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides the port
    app.run(host="0.0.0.0", port=port, debug=True)
