# app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

def generate_page(name):
    page = \
        f'''
        <h1>Ödestärningar</h1>
        <form action="/cmd/" method="get">
        <label for="name">Namn:</label><input type="text" id="name" name="name" value="{name}"><br><br>
        <input type="submit" value="Submit">
        </form>
        '''
    lines = ""
    line = ""
    with open("rolls.txt", "r") as f:
        while True:
            line = f.readline()
            print(line)
            lines = line + "<br>" + lines
            if line == "":
                break

    page = page + lines
    print(lines)

    return page


@app.route('/cmd/', methods=['GET'])
def cmd():
    name = request.args.get("name", None)
    print(f"Name: {name}")

    if not name:
        name = ""
    else:
        result = random.randrange(1,20)
        with open("rolls.txt", "a") as f:
            f.write(f"{name} slog 1T20, resultat: {result}\n")

    return generate_page(name)

@app.route('/')
def index():
    return generate_page("Anonym")

if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app)