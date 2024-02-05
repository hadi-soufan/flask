import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Invalid data, Please provide a valid name.")

    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message="Store already exists")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
        abort(400, message="Invalid data, Please provide a valid price, store_id or name.")

    for item in items.values():
        if item["name"] == item_data["name"] and item_data["store_id"] == item["store_id"]:
            abort(400, message="Item already exists")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>/")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")


@app.delete("/store/<string:name>/item/<string:item_name>")
def delete_item(name, item_name):
    for store in stores:
        if store["name"] == name:
            for item in store["items"]:
                if item["name"] == item_name:
                    store["items"].remove(item)
                    return {"message": f"Item {item_name} deleted successfully"}, 200

    abort(404, message="Item not found")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)