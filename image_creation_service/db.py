from pymongo import MongoClient
import base64
import uuid

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
    functions = get_functions_collection_instance()
    function = {
        'name': req_data.get('name',''),
        'uuid': uuid,
        'state': 'active',
        'run_state': 'pending',
        'artifact': req_data.get('artifact'),
        'language': req_data.get('language'),
        'image_url':''
    }
    functions.insert_one(function)

def update_entry(function_uuid,image_url):
    functions=functions = get_functions_collection_instance()
    uuid_value={'uuid' : uuid.UUID(function_uuid),}
    update_values={"$set":{'image_url':image_url,'run_state':'running'}}
    functions.update_one(uuid_value,update_values)

def get_db_entry(function_uuid):
    functions = get_functions_collection_instance()
    cursor = functions.find({'uuid' : uuid.UUID(function_uuid)})
    for document in cursor:
        del document['_id']
        return document

def get_all_documents():
    functions = get_functions_collection_instance()
    function_list = []
    cursor = functions.find({})
    for document in cursor:
        del document['_id']
        function_list.append(document)
    return function_list
