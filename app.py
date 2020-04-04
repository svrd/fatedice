# app.py
from flask import Flask, request, redirect, url_for, session
from flask_socketio import SocketIO
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

def generate_page(name, dice):
    page = \
        f'''
        <h1>Ödestärningar</h1>
        <form action="/cmd/" method="get">
        <label for="name">Namn:</label><input type="text" id="name" name="name" value="{name}"><br>
        <label for="dice">Tärning:</label><input type="text" id="dice" name="dice" value="{dice}"><br>
        <label for="question">Ödesfråga:</label><input type="text" id="question" name="question" value=""><br>
        <select id="modifier" name="modifier"><br>
            <option value="0" selected>Femti/femti eller vet ej (0)</option>
            <option value="8">Garanterat (+8)</option>
            <option value="6">Helt säkert (+6)</option>
            <option value="4">Väldigt troligt (+4)</option>
            <option value="2">Ganska troligt (+2)</option>
            <option value="-2">Inte så troligt (-2)</option>
            <option value="-4">Väldigt otroligt (-4)</option>
            <option value="-6">Inte en chans (-6)</option>
            <option value="-8">Omöjligt (-8)</option>
        </select>
        <select id="kaos_factor" name="kaos_factor">
            <option value="6">Kaosfaktor=6</option>
            <option value="5">Kaosfaktor=5</option>
            <option value="4" selected>Kaosfaktor=4</option>
            <option value="3">Kaosfaktor=3</option>
        </select>
        <select id="kaos_modifier" name="kaos_modifier">
            <option value="2">Kaos (+2)</option>
            <option value="0" selected>Kaos (0)</option>
            <option value="-2">Kaos (-2)</option>
        </select><br>
        <input type="submit" value="Submit">
        </form>
        <button onClick="window.location.reload();">Ladda om sidan</button>
        '''
    lines = ""
    line = ""
    try:
        with open("rolls.txt", "r+") as f:
            while True:
                line = f.readline()
                lines = line + "<br>" + lines
                if line == "":
                    break
    except IOError:
        print("No file")
    page = page + lines

    return page


@app.route('/cmd/', methods=['GET'])
def cmd():
    name = request.args.get("name", None)
    dice = request.args.get("dice", None)
    question = request.args.get("question", None)
    modifier = request.args.get("modifier", None)
    kaos_factor = request.args.get("kaos_factor", None)
    kaos_modifier = request.args.get("kaos_modifier", None)
    print(f"Name: {name}")
    print(f"Dice: {dice}")
    print(f"Question: {question}")
    print(f"Modifier: {modifier}")
    print(f"Kaos Factor: {kaos_factor}")
    print(f"Kaos Modifier: {kaos_modifier}")

    if name:
        session['name'] = name
    

    if not name:
        name = session.get('name', 'Anonym')
    elif question is not None and question != "" \
            and modifier.lstrip('-').isnumeric() \
            and kaos_factor.isnumeric() \
            and kaos_modifier.lstrip('-').isnumeric():
        result1 = random.randint(1,10)
        result2 = random.randint(1,10)
        modifier_number = int(modifier)
        kaos_factor_number = int(kaos_factor)
        kaos_modifier_number = int(kaos_modifier)
        kaos_roll = random.randint(1,10)
        result = result1 + result2 + modifier_number + kaos_modifier_number
        answer = "NEJ"
        random_event = "NEJ"
        if result > 10:
            answer = "JA"
        if kaos_roll <= kaos_factor_number:
            if result1 == result2:
                answer = "Synnerligen " + answer
                random_event = "JA"
            elif result1 % 2 != 0 and result2 %2 != 0:
                answer = "Synnerligen " + answer
            elif result1 % 2 == 0 and result2 % 2 == 0:
                random_event = "JA"
        with open("rolls.txt", "a+") as f:
            f.write("\n")
            if random_event == "JA":
                f.write(f"Slumpmässig händelse!\n")
            f.write(f"Svar: {answer}!\n")
            f.write(f"Kaosfaktor: {kaos_factor}, Kaostärning: {kaos_roll}\n")
            f.write(f"Resultat: {result1} + {result2} + {modifier} + {kaos_modifier} = {result}\n")
            f.write(f"{name} frågade: {question}\n")
            f.write("\n")
        return redirect(url_for('index'))
    elif dice is not None and dice.isdigit():
        session['dice'] = dice
        result = random.randint(1,(int(dice)))
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} slog 1T{dice}, resultat: {result}\n")
        return redirect(url_for('index'))

    return generate_page(name, dice)

@app.route('/')
def index():
    name = session.get('name', 'Anonym')
    dice = session.get('dice', '20')
    return generate_page(name, dice)

if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app)