import urllib.request
import json
import base64, requests

"""
with open("./functions/sourcepkg.zip", "rb") as file:
    bytes = file.read()
    encoded = base64.b64encode(bytes)
encoded = encoded.decode('utf-8')
body = {'name': "test_func", 'artifact': encoded, 'language': "python3"}  
myurl = "http://127.0.0.1:5000/upload"

req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
req.add_header('Content-Length', len(jsondataasbytes))
print (jsondataasbytes)
response = urllib.request.urlopen(req, jsondataasbytes)
print (response)
"""
#FOR GET
#uuid = c172aff8924111e9930788e9fe567442
#myurl = "http://127.0.0.1:5000/functions/"+ uuid
#req = urllib.request.Request(myurl)


URL = "http://127.0.0.1:5000/functions"
r = requests.get(url = URL)
data = r.json() 
print(r)

