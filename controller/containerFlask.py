import os
from flask import Flask, flash, request
from werkzeug.utils import secure_filename

from index import handler

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/execute_function',  methods = ['GET', 'POST'])
def execute_function():
    print("Calling handler function")
    handler()

app.run(debug=True)