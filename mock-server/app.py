from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join("data", "customers.json")


def load_customers():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/customers", methods=["GET"])
def get_customers():
    customers = load_customers()

    # Query params
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    if page < 1 or limit < 1:
        return jsonify({"error": "Page and limit must be positive integers"}), 400

    total = len(customers)

    start = (page - 1) * limit
    end = start + limit

    paginated_data = customers[start:end]

    return jsonify({
        "data": paginated_data,
        "total": total,
        "page": page,
        "limit": limit
    }), 200


@app.route("/api/customers/<string:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customers = load_customers()

    for customer in customers:
        if customer.get("customer_id") == customer_id:
            return jsonify(customer), 200

    return jsonify({"error": "Customer not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)