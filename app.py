# app.py
from rollparser import parse_roll
from flask import Flask, request, redirect, url_for, session
from flask_socketio import SocketIO
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

def generate_page(name, dice, roll):
    page = \
        f'''
        <h1>Ödestärningar</h1>
        <form action="/cmd/" method="get">
        <label for="name">Namn:</label><input type="text" id="name" name="name" value="{name}"><br>
        <label for="dice">Tärning:</label><input type="text" id="dice" name="dice" value="{dice}">
        <input type="submit" name="dice_button" value="Tärning"><br>

        <input type="submit" name="d100_button" value="1T100">
        <input type="submit" name="d20_button" value="1T20">
        <input type="submit" name="d12_button" value="1T12">
        <input type="submit" name="d10_button" value="1T10">
        <input type="submit" name="d8_button" value="1T8">
        <input type="submit" name="d6_button" value="1T6">
        <input type="submit" name="d4_button" value="1T4">
        <input type="submit" name="d2_button" value="1T2"><br>

        <label for="roll">Slag:</label><input type="text" id="roll" name="roll" value="{roll}">
        <input type="submit" name="roll_button" value="Slag"><br>

        <label for="question">Ödesfråga:</label><input type="text" id="question" name="question" value="">
        <input type="submit" name="question_button" value="Fråga"><br>
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
        <input type="submit" name="reload_button" value="Ladda om"><br>
        </form>
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
    roll = request.args.get("roll", None)
    print(f"Name: {name}")
    print(f"Dice: {dice}")
    print(f"Question: {question}")
    print(f"Modifier: {modifier}")
    print(f"Kaos Factor: {kaos_factor}")
    print(f"Kaos Modifier: {kaos_modifier}")

    if name:
        session['name'] = name
    
    roll_dice = False
    if request.args.get('dice_button') is not None:
        roll_dice = True

    dice_list = ['100', '20', '12', '10', '8', '6', '4', '2']
    for d in dice_list:
        if request.args.get(f'd{d}_button') is not None:
            roll_dice = True
            dice = d


    if not name:
        name = session.get('name', 'Anonym')
    elif request.args.get('question_button') is not None and question is not None and question != "" \
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
    elif request.args.get('roll_button') is not None and roll is not None and roll != "":
        session['roll'] = roll
        result = parse_roll(roll)
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} slog {roll}, resultat: {result}\n")
    elif roll_dice and dice is not None and dice.isdigit():
        session['dice'] = dice
        result = random.randint(1,(int(dice)))
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} slog 1T{dice}, resultat: {result}\n")
        return redirect(url_for('index'))

    return generate_page(name, dice, roll)

@app.route('/')
def index():
    name = session.get('name', 'Anonym')
    dice = session.get('dice', '20')
    roll = session.get('roll', '')
    return generate_page(name, dice, roll)

if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app)