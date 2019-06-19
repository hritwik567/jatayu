import os
import time
import db
import json
import requests
from flask import Flask, flash, request, jsonify
import uuid,base64, zipfile, json
from docker_helper import create_image
import collections

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
dockerde=collections.deque()

@app.route("/image_delete", methods=["DELETE"])
def delete_image():
    if request.args["func_name"]:
        result = db.del_image(request.args["func_name"])
        print(result)

@app.route("/create_image", methods=["POST"])
def image_create_handler():
    print("image creation request raised", request.data)
    req_data = json.loads(request.data)
    func_uuid = req_data["func_uuid"]
    doc = db.get_db_entry(func_uuid)
    artifact = doc.get('artifact')
    decoded = base64.b64decode(artifact)
    if artifact:
        with open('./temp.zip', 'wb') as result:
            result.write(decoded)
    zip_ref = zipfile.ZipFile("./temp.zip","r")
    zip_ref.extractall(os.path.join(os.getcwd(), "extracted_folder"))

    f = open(os.path.join(os.getcwd(), "extracted_folder", "sourcepkg", "index.py"))
    data = f.read()
    f.close()

    image_path = "/home/abhijeet.kaurav/images"

    image_name = create_image(data, image_path)
    db.update_entry(func_uuid, image_name)
    try:
        requests.request(
                method="POST",
                url="http://localhost:2000/new/deployments",  #my service will run on port 2000
                json={"name": func_uuid, "container_ref": image_name},
                allow_redirects=False)
    except:
        return "Sorry coudn't make a deployment"
    return image_name

@app.route('/image_pull',methods=['GET'])
def image_pull():
    if request.args["func_name"]:
        image_present=db.is_present_in_db(request.args["func_name"])
    if not image_present:
        msg="There is no image for the requested function"
        return msg
    else:
       print(image_present)
       return image_present
       return jsonify(image_present)

app.run(debug=True, port=4000)
