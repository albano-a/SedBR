from flask import Flask, render_template, request
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='layouts')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


# example
# @app.route('/about')
# def about():
#     return render_template('about.html')


if __name__ == "__main__":
    app.run(port=5000)
