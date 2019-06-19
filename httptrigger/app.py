import requests
import json
from flask import request, Flask

app = Flask(__name__)

def fun_obj_validator(fun_obj, method):
    state, run_state, fun_method = fun_obj['state'], fun_obj['run_state'], fun_obj.get('method', None)
    # if method != fun_method:
    #     return "Incorrect method invoked."
    if state == "deleted":
        return "Function object is not active."
    if run_state == "pending":
        return "Function object creation is pending."
    if run_state == "failed":
        return "Function object creation could not succeed."
    return None

@app.route("/functions/<string:function_id>/<path:request_url>", methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
@app.route("/functions/<string:function_id>", methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
def trigger_api(function_id):
    try:
        resp = requests.get("http://localhost:6000/functions/" + function_id)
        fun_obj = json.loads(resp.content)
    except:
        return "Some error occured"
    method = request.method
    vld_str = fun_obj_validator(fun_obj, method)
    if vld_str:
        return vld_str
    try:
        resp = requests.request(
                    method=request.method,
                    url="http://localhost:2000/deployments"  + request.url.split("functions", 1)[1],
                    headers={key: value for (key, value) in request.headers if key != 'Host'},
                    data=request.get_data(),
                    json=request.get_json(),
                    cookies=request.cookies,
                    allow_redirects=False)
        print("Response", resp)
        return resp.content
    except:
        return "Some error occured"

app.run(debug=True, port=3000)
