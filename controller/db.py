from pymongo import MongoClient
import base64

functions = None
db = None
client = None

def get_functions_collection_instance():
    global functions, client, db
    if not functions:
        client = MongoClient('localhost', 27017)
        db = client.serverless
        functions = db.functions
    return functions

def add_db_entry(req_data, uuid):
    #print(req_data)
    print("HEREEEE")
    functions = get_functions_collection_instance()
    function = {
    'name': req_data.get('name',''),
    'uuid': uuid,
    'state': 'active',
    'run_state': 'pending',
    'artifact': req_data.get('artifact'),
    'language': req_data.get('language')
    }
    functions.insert_one(function)
    print("added to db")

def get_db_entry(function_uuid):
    functions = get_functions_collection_instance()
    return functions.findOne({uuid : function_uuid})

def get_all_documents():
    functions = get_functions_collection_instance()
    function_list = []
    cursor = functions.find({})
    for document in cursor:
        del document['_id']
        del document['artifact']
        print("Document: ", document)
        function_list.append(document)
    return function_list
