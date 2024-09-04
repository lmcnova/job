from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
import hashlib

app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = 'uploads1/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- MongoDB Code ------------
client = MongoClient('mongodb://localhost:27017/')
db = client['personal_info']
# coll = db['job']
coll = db['test']

@app.route("/data", methods=['POST', 'GET'])
def data():
    try:
        company_name = request.form.get('companyName')
        role = request.form.get('role')
        apply_date = request.form.get('applyDate')
        personal_info = request.form.get('personalInfo')
        status = request.form.get('status')
        hear = request.form.get('hear')
        job_url = request.form.get('jobUrl')
        # Get the uploaded file
        resume = request.files.get('resume')




        if resume:
            # Save the file to the specified folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            resume.save(file_path)
            data = {
                "Company_name": f"{company_name}",
                "role": f'{role}',
                "apply_date": f'{apply_date}',
                "personal_info": f'{personal_info}',
                "status": f'{status}',
                "hear": f'{hear}',
                "job_url": f'{job_url}',
                "resume": f'{file_path}'
            }
            db['test'].insert_one(data)
            return jsonify({"message": "Successfully"})

        return "No file uploaded", 400


    except Exception as e:
        print(f"Error : {e}")
        return 'error'

@app.route("/get_data_job", methods=['POST', 'GET'])
def get_data_job():
    try:
        coll = db['test'].find({})

        documents = list(coll)

        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])


        return jsonify({'data': documents})


    except Exception as e:
        return e



@app.route("/delete_job/<string:id>", methods=['POST', 'GET'])
def delete_job(id):
    print(id)
    try:
        db['test'].delete_one({"_id": ObjectId(id)})
        return jsonify({'data', 'deteled'})

    except Exception as e:
        return  "ddddd"


@app.route("/job_fillter/<string:data>", methods=['POST', 'GET'])
def job_fillter(data):

    if data == "all":
        coll = db['test'].find({})

        documents = list(coll)

        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

    else:
        coll = db['test'].find({'status': f'{data}'})

        documents = list(coll)

        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

    return jsonify({'data': documents})

if __name__ == "__main__":
    app.run(debug=True)