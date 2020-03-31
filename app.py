# app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config.from_object(Config)
db = SQLAlchemy(app)

def generate_page():
    name = ""
    if 'name' in g:
        print(f"Setting name to {g.name}")
        name = g.name
    else:
        print("name is not set")

    page = \
        f'''
        <h1>Välkommen {name}<h1>
        '''
    return page


@app.route('/cmd/', methods=['GET'])
def cmd():
    name = request.args.get("name", None)
    print(f"Name: {name}")

    if not name:
        name = ""

    g.name = name

    return generate_page()

@app.route('/')
def index():
    return generate_page()

if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app)