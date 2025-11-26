from flask import jsonify, request

ALLOWED_USER_AGENTS = [
    "Mozilla",
    "Chrome",
    "Safari",
    "Firefox",
    "Edge",
]


def restrict_user_agents(app):
    @app.before_request
    def check_user_agent():
        user_agent = request.headers.get("User-Agent", "")
        if not any(browser in user_agent for browser in ALLOWED_USER_AGENTS):
            return jsonify({"error": "Access denied"}), 403
