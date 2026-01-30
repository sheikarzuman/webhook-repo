
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client.github_events
collection = db.events


# Home route (UI)
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# GitHub webhook endpoint
@app.route("/webhook", methods=["POST"])
def github_webhook():
    payload = request.json
    event = request.headers.get("X-GitHub-Event")

    # Handle GitHub ping event
    if event == "ping":
        return jsonify({"msg": "pong"}), 200

    # PUSH event
    if event == "push":
        data = {
            "request_id": payload["head_commit"]["id"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(data)

    # PULL REQUEST & MERGE events
    elif event == "pull_request":
        pr = payload["pull_request"]
        action_type = payload["action"]

        if action_type == "opened":
            action = "PULL_REQUEST"
        elif action_type == "closed" and pr.get("merged"):
            action = "MERGE"
        else:
            return jsonify({"status": "ignored"}), 200

        data = {
            "request_id": str(pr["id"]),
            "author": pr["user"]["login"],
            "action": action,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(data)

    return jsonify({"status": "ok"}), 200


# Endpoint for UI polling
@app.route("/events", methods=["GET"])
def get_events():
    events = list(
        collection.find({}, {"_id": 0}).sort("timestamp", -1)
    )
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)
