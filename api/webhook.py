from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/goto/call-event", methods=["POST"])
def goto_call_event():
    payload = request.json
    user_id = payload.get("user_id")
    event = payload.get("event")
    timestamp = payload.get("ts")
    # TODO: store events in DB or update cache
    print(f"Received {event} for {user_id} at {timestamp}")
    return jsonify({"status":"ok"}), 200

# Run Flask locally if needed
if __name__ == "__main__":
    app.run(port=5000)
