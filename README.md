# webhook-repo

This repository contains a **Flask-based GitHub webhook receiver** that listens to
events from a GitHub repository, stores them in MongoDB, and displays them via a
simple UI.

## Project Overview
The application receives GitHub webhook events such as:
- Push
- Pull Request
- Merge (bonus)

It processes only the required fields, stores them in MongoDB, and exposes an
endpoint that the UI polls every 15 seconds to display the latest activity.

## Tech Stack
- Python
- Flask
- MongoDB (Atlas)
- ngrok (for local webhook testing)
- HTML + JavaScript (UI)

## Application Flow
1. GitHub triggers an event in `action-repo`
2. GitHub sends the event payload to `/webhook`
3. Flask processes the payload
4. Relevant data is stored in MongoDB
5. UI polls the backend every 15 seconds to display updates

## MongoDB Schema
Each event is stored with the following fields:
- request_id
- author
- action (PUSH / PULL_REQUEST / MERGE)
- from_branch
- to_branch
- timestamp (UTC)

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-webhook-repo-url>
cd webhook-repo
