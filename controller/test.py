import urllib.request
import json
import base64, requests


with open("./temp.zip", "rb") as file:
    bytes = file.read()
    encoded = base64.b64encode(bytes)
encoded = encoded.decode('utf-8')
body = {'name': "test_func1", 'artifact': encoded, 'language': "python3"}
myurl = "http://127.0.0.1:5000/upload"

req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
req.add_header('Content-Length', len(jsondataasbytes))
print (jsondataasbytes)
response = urllib.request.urlopen(req, jsondataasbytes)
print (response)


# 935aa054928b11e9912dacde48001122


#FOR GET
"""
myurl = "http://127.0.0.1:5000/functions"
req = urllib.request.Request(myurl)
"""

#FOR GET WITH A UUID
"""
URL = "http://127.0.0.1:5000/functions/c172aff8-9241-11e9-9307-88e9fe567442"
r = requests.get(url = URL)
data = r.json()
print(data)
"""
