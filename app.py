import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from litologias import *

def csv_to_html():
    df = pd.read_csv('upload/poco_teste.csv', sep=';')
    return df.to_html(classes='table table-striped')

app = Flask(__name__, template_folder='layouts')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show')
def home():
    table = csv_to_html()
    return render_template('show.html', table=table)

@app.route('/openFile')
def openFile():
    return render_template('openFile.html')

# Receives the uploaded content
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Now you can use the file variable to access the uploaded file
    # For example, you can save the file:
    file.save('upload/' + file.filename)
    return 'Arquivo importado e salvo. \nRedirecionando pra página inicial...'

@app.route('/remove', methods=['POST'])
def remove_file():
    filename = request.json['filename']
    os.remove(os.path.join('./upload', filename))
    return '', 204

@app.route('/rename', methods=['POST'])
def rename_file():
    oldName = request.json['oldName']
    newName = request.json['newName']
    os.rename(os.path.join('./upload', oldName), os.path.join('./upload', newName))
    return '', 204

@app.route('/get-wells', methods=['GET'])
def get_wells():
    files = os.listdir('./upload')
    return render_template('uploaded_wells.html', wells=files)



# a route that opens a python file with dictionaries
@app.route('/litologias')
def litologias():
    return lithologies_name



# example
# @app.route('/about')
# def about():
#     return render_template('about.html')


if __name__ == "__main__":
    app.run(port=5000)
