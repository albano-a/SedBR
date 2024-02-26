from flask import Flask, render_template, request
from flask_cors import CORS
from litologias import *



app = Flask(__name__, template_folder='layouts')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/openFile')
def openFile():
    return render_template('openFile.html')

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
