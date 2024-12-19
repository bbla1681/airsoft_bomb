from flask import Flask, request, jsonify

app = Flask(__name__)

# Store the current action state
action_state = {"action": "deactivate"}

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(action_state)

@app.route("/start_timer", methods=["POST"])
def start_timer():
    global action_state
    action_state["action"] = "start_timer"
    return jsonify({"status": "Timer started"}), 200

@app.route("/deactivate", methods=["POST"])
def deactivate():
    global action_state
    action_state["action"] = "deactivate"
    return jsonify({"status": "Deactivated"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)