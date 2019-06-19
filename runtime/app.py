import os
import json
import requests

import main
import process_requests

from flask import Flask, request, Response, abort

app = Flask(__name__, instance_relative_config=True)
process_requests = process_requests.ProcessRequests()

@app.route("/new/deployments", methods=["POST"])
def new_deployment():
    try:
        data = json.loads(request.data)
    except:
        abort(400)
    print(data)
    # return str(data)
    main.create_dep("im" + data["name"], data["container_ref"])
    retval = process_requests.process_requests(data["name"])
    for i in retval:
        print(i)
        main.update_dep("im" + i, 0)
    return data["name"]

@app.route("/delete/deployments", methods=["POST"])
def delete_deployment():
    try:
        data = json.loads(request.data)
    except:
        abort(400)
    # return str(data)
    main.delete_dep(data["name"])
    process_requests.delete_requests(data["name"])
    return data["name"]

@app.route("/deployments/<string:function_id>/<path:request_url>", methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
@app.route("/deployments/<string:function_id>", methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
def httptrigger(function_id, request_url = None):
    # print("Data", request.data)
    # print("Json", request.json)
    # return "Jai Mata di"
    try:
        host, port, endpoint = main.get_request_meta("im" + function_id)
    except:
        return "Some error occured in runtime"
    print(host + ":" + str(port) + endpoint + request.url.split(function_id, 1)[1])
    # try:
    retval = process_requests.process_requests(function_id)
    for i in retval:
        print(i)
        if i != function_id:
            main.update_dep("im" + i, 0)
    main.update_dep("im" + function_id, 1)
    resp = requests.request(
        method=request.method,
        url="http://" + host + ":" + str(port) + request.url.split(function_id, 1)[1],
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        json=request.get_json(),
        cookies=request.cookies,
        allow_redirects=False)
    print(resp.content, resp.headers.items())
    return resp.content
    # except:
    #     return "Some error occured"

main.init_kube()
app.run(debug=True, port=2000)
