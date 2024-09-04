from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = None
collections = None
@app.route("/data", methods=['POST', 'GET'])
def data_coll():
    global client
    data = request.json
    url = data.get('url')
    print(url)
    client = MongoClient(url)
    database_list = client.list_database_names()
    for db_name in database_list:
        print(db_name)
    return jsonify({"message": 'url recevied', 'db_list': database_list})


@app.route("/coll", methods=["POST", "GET"])
def coll_list():
    global client, collections  # Use the global 'client' variable

    data = request.json
    db_name = data.get('db_name')

    if client is None:
        return jsonify({"error": "Client not initialized"}), 400

    # Access the specified database
    db = client[db_name]

    # Get the list of collections in the specified database
    collections = db.list_collection_names()

    coll_Data = []

    for coll_name in collections:
        collection = db[coll_name]  # Get the collection object
        count = collection.count_documents({})
        # collection Details
        stats = db.command('collstats', coll_name)
        coll_size = stats.get('size', 'N/A')
        coll_total_index_size = stats.get('totalIndexSize', 'N/A')
        coll_avg_doc_size = stats.get('avgObjSize', 'N/A')
        coll_storage_size = stats.get('storageSize', 'N/A')
        coll_data_size = stats.get('dataSize', 'N/A')
        coll_number_extents = stats.get('nindexes', 'N/A')
        coll_Data.append({"collection_name": coll_name, "count": count, "coll_size": coll_size, "coll_total_index_size":coll_total_index_size, "coll_avg_doc_size":coll_avg_doc_size,
                          "coll_storage_size":coll_storage_size, "coll_number_extents":coll_number_extents})

    # Return the list of collections as JSON
    return jsonify({"collections": coll_Data})

@app.route('/coll_data', methods=['POST', 'GET'])
def coll_list_data():
    global client

    data = request.json
    db_name = data.get('db_name')
    coll_name = data.get('collection_name')

    if client is None:
        return jsonify({"error": "Client not initialized"}), 400

    if not db_name or not coll_name:
        return jsonify({"error": "Database name and collection name are required"}), 400

    # Access the specified database and collection
    db = client[db_name]
    collection = db[coll_name]

    # Retrieve all documents from the collection
    documents = list(collection.find())

    # Convert ObjectId to string for JSON serialization
    # for doc in documents:
    #     doc['_id'] = str(doc['_id'])

    for doc in documents:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        for key, value in doc.items():
            if isinstance(value, datetime):
                doc[key] = value.isoformat()

                # Return the documents as JSON
    return jsonify({"data": documents})



if __name__ == "__main__":
    app.run(debug=True)

