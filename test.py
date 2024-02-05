import os
import tempfile
from flask import Flask, request
from flask import current_app
from flask import g
from flask import json
from flask import jsonify
from flask import url_for
from werkzeug.exceptions import HTTPException, NotFound

# Create a temporary directory for the database
DATABASE_DIR = tempfile.mkdtemp()

# Create a mock database of stores
DATABASE = os.path.join(DATABASE_DIR, "database.json")

# Create a new Flask application
app = Flask(__name__)


# Load the mock database of stores on startup
@app._got_first_request
def load_database():
    with open(DATABASE, "r") as f:
        g.database = json.load(f)

# A mock function to simulate a database of stores
def get_stores():
    return g.database

# A mock function to simulate creating a new store
def create_store(name):
    store_id = max([s["id"] for s in g.database]) + 1
    g.database.append({"id": store_id, "name": name, "items": []})
    return g.database[-1], 201

# A mock function to simulate getting a store by name
def get_store_by_name(name):
    for store in g.database:
        if store["name"] == name:
            return store
    raise NotFound()

# A mock function to simulate creating an item in a store
def create_item(store_name, item_name, item_price):
    for store in g.database:
        if store["name"] == store_name:
            item_id = max([i["id"] for i in store["items"]]) + 1
            store["items"].append({"id": item_id, "name": item_name, "price": item_price})
            return store["items"][-1], 201
    raise NotFound()

# A mock function to simulate getting all items in a store
def get_items_in_store(store_name):
    for store in g.database:
        if store["name"] == store_name:
            return store["items"]
    raise NotFound()

# A mock function to simulate deleting an item from a store
def delete_item(store_name, item_name):
    for store in g.database:
        if store["name"] == store_name:
            for item in store["items"]:
                if item["name"] == item_name:
                    store["items"].remove(item)
                    return {"message": f"Item {item_name} deleted successfully"}, 200
    raise NotFound()

# Register the mock functions with the Flask application
@app.route("/store", methods=["GET"])
def get_stores():
    return jsonify(get_stores())

@app.route("/store", methods=["POST"])
def create_store():
    data = request.get_json()
    return jsonify(create_store(data["name"]))

@app.route("/store/<string:name>", methods=["GET"])
def get_store_by_name(name):
    return jsonify(get_store_by_name(name))

@app.route("/store/<string:store_name>/item", methods=["POST"])
def create_item(store_name):
    data = request.get_json()
    return jsonify(create_item(store_name, data["name"], data["price"]))

@app.route("/store/<string:store_name>/item", methods=["GET"])
def get_items_in_store(store_name):
    return jsonify(get_items_in_store(store_name))

@app.route("/store/<string:store_name>/item/<string:item_name>", methods=["DELETE"])
def delete_item(store_name, item_name):
    return jsonify(delete_item(store_name, item_name))

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)