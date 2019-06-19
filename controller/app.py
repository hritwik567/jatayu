import os
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
from db import add_db_entry, get_db_entry, get_all_documents
import uuid, base64, zipfile, json
from flask_uuid import FlaskUUID
import requests


ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
FlaskUUID(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate(req_data):
    if req_data.get('language') != "python3":
        return False
    artifact = req_data.get('artifact')
    decoded = base64.b64decode(artifact)
    if artifact:
        with open('./temp.zip', 'wb') as result:
            result.write(decoded)
    zip_ref = zipfile.ZipFile("./temp.zip","r")
    zip_ref.extractall("extracted_file")
    flag1, flag2 = False, False
    for filename in os.listdir("extracted_file"):
        for files in os.listdir("extracted_file/"+ filename):
            if files == "requirements.txt":
                flag1 = True
            if files == "index.py":
                flag2 = True
    if flag1 and flag2:
        return True
    return False

@app.route('/functions/<uuid(strict=False):id>',  methods = ['GET'])
def get_function_info(id):
    return jsonify(get_db_entry(id))

@app.route('/functions', methods = ['GET'])
def get_all_functions():
    s = get_all_documents()
    return jsonify(functions = s)

@app.route('/upload',  methods = ['GET', 'POST'])
def upload_function():
    print("In upload function\n")
    if request.method == 'POST':
        req_data = request.get_json(force=True)
        if validate(req_data):
            function_uuid = uuid.uuid1()
            print("UUID : " + function_uuid.hex)
            add_db_entry(req_data, function_uuid)
            try:
                resp = requests.request(
                        method="POST",
                        url="http://localhost:4000/create_image",
                        json={"func_uuid": str(function_uuid.hex)},
                        allow_redirects=False)
            except:
                return jsonify(
                    function_name=req_data.get('name', ''),
                    run_state="failed",
                    language=req_data.get('language')
                    )
            #make request to the Container Creation Service with function uuid
            return jsonify(
                function_name=req_data.get('name', ''),
                function_id=function_uuid.hex,
                state="active",
                run_state="pending",
                language=req_data.get('language')
                )
        else:
            return jsonify(
                function_name=req_data.get('name', ''),
                run_state="failed",
                language=req_data.get('language')
                )

app.run(debug=True, port=6000)
