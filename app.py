# app.py
from rollparser import parse_roll
from flask import Flask, request, redirect, url_for, session
from flask_socketio import SocketIO
from pool import *
from dicestatistics import add_stat, read_stats, write_stats, get_stats
from randomtable import *
from detailcheck import *
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['transports'] = 'websocket'
socketio = SocketIO(app)

def format_pool_roll(pool_roll):
    formatted_roll = ""
    rolls = pool_roll.split(' ')
    artifact_rolls = ""
    for roll in rolls:
        i = 0
        if roll == '':
            continue
        elif roll[i] == 'B':
            i += 1
            if roll[i] == '1' or roll[i] == '6':
                formatted_roll += f'''<strong style="font-size: x-large; background-color: yellow;">{roll[i]} </strong>'''
            else:
                formatted_roll += f'''<text style="background-color: yellow;">{roll[i]} </text>'''
        elif roll[i] == 'S':
            i += 1
            if roll[i] == '6':
                formatted_roll += f'''<strong style="font-size: x-large; background-color: green; color: white">{roll[i]} </strong>'''
            else:
                formatted_roll += f'''<text style="background-color: green; color: white">{roll[i]} </text>'''
        elif roll[i] == 'I':
            i += 1
            if roll[i] == '1' or roll[i] == '6':
                formatted_roll += f'''<strong style="font-size: x-large; background-color: black; color: white">{roll[i]} </strong>'''
            else:
                formatted_roll += f'''<text style="background-color: black; color: white">{roll[i]} </text>'''
        elif roll[i] == 'A':
            i += 1
            artifact_dice_and_roll = roll[i:].split(':')
            artifact_dice = int(artifact_dice_and_roll[0])
            artifact_roll = int(artifact_dice_and_roll[1])
            artifact_rolls += f"T{artifact_dice}={artifact_roll} "
            if artifact_roll > 11:
                formatted_roll += f'''<strong style="font-size: x-large; background-color: red; color: white">6666 </strong>'''
            elif artifact_roll > 9:
                formatted_roll += f'''<strong style="font-size: x-large; background-color: red; color: white">666 </strong>'''
            elif artifact_roll > 7:
                formatted_roll += f'''<strong style="font-size: x-large; background-color: red; color: white">66 </strong>'''
            elif artifact_roll > 5:
                formatted_roll += f'''<strong style="font-size: x-large; background-color: red; color: white">6 </strong>'''
            else:
                formatted_roll += f'''<text style="background-color: red; color: white">- </text>'''

    if artifact_rolls != "":
        formatted_roll += "<text>  " + artifact_rolls + "</text>"

    return formatted_roll


def generate_page(nameValueDict):
    page = \
        '''
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js"></script>
        <script type="text/javascript" charset="utf-8">
            var socket = io();
            socket.on('connect', function() {
                socket.emit('message', 'connected!');
            });
            socket.on('reload', function() { location.reload();})
        </script>        
        '''      
    read_stats()  
    d6_statistics = get_stats()

    combination = ""
    if nameValueDict['combination'] == "":
        combination = f'''<label for="combination">Kombination:</label><input type="text" id="combination" name="combination" value="{nameValueDict['combination']}"><input type="submit" name="hide_button" value="Dölj"><br>'''
    else:
        combination = f'''<label for="combination">Kombination: {nameValueDict['combination']}</label><input type="submit" name="show_button" value="Visa"><br>'''

    page = page + \
        f'''
        <h1>Ödestärningar</h1>
        <form action="/cmd/" method="get">
        <input type="submit" name="reload_button" value="Ladda om"><br>
        <label for="name">Namn:</label><input type="text" id="name" name="name" value="{nameValueDict['name']}"><br>
        <label for="dice">Tärning:</label><input type="text" id="dice" name="dice" value="{nameValueDict['dice']}">
        <input type="submit" name="dice_button" value="Tärning"><br>

        <input type="submit" name="d100_button" value="1T100">
        <input type="submit" name="d20_button" value="1T20">
        <input type="submit" name="d12_button" value="1T12">
        <input type="submit" name="d10_button" value="1T10">
        <input type="submit" name="d8_button" value="1T8">
        <input type="submit" name="d6_button" value="1T6">
        <input type="submit" name="d4_button" value="1T4">
        <input type="submit" name="d2_button" value="1T2"><br>

        <label for="roll">Slag:</label><input type="text" id="roll" name="roll" value="{nameValueDict['roll']}">
        <input type="submit" name="roll_button" value="Slag"><br>

        <label for="question">Fråga:</label><input type="text" id="question" name="question" value="">
        <input type="submit" name="fate_question_button" value="Ödesfråga">
        <input type="submit" name="detail_question_button" value="Detaljfråga"><br>
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
        <input type="submit" name="random_event_button" value="Slumpmässig händelse">
        <input type="submit" name="meaning_table_action_button" value="Handling">
        <input type="submit" name="meaning_table_description_button" value="Beskrivning"><br>
        <label for="random_table">Slumpa:</label><input type="text" id="random_table" name="random_table" value="">
        <input type="submit" name="random_table_button" value="Slumpa"><br>
        <!--<h2>Mutant</h2>-->
        <!--{d6_statistics}<br>-->
        <!--<input type="submit" name="junk_button" value="Vad är det jag hittar?"><input type="submit" name="who_button" value="Vem är det där?"><br><br>-->
        {combination}
        '''

    no_of_combinations = int(nameValueDict['no_of_combinations'])
    for i in range(1, no_of_combinations + 1):
        page = page + \
            f'''
            <label for="roll">Namn:</label><input type="text" size=8 min=0 id="tag{i}" name="tag{i}" value="{nameValueDict['tag' + str(i)]}">
            <label for="roll">Grund:</label><input type="text" size=2 min=0 id="base{i}" name="base{i}" value="{nameValueDict['baseValue' + str(i)]}">
            <label for="roll">Färdighet:</label><input type="text" size=2 min=0 id="skill{i}" name="skill{i}" value="{nameValueDict['skillValue' + str(i)]}">
            <label for="roll">Pryl:</label><input type="text" size=2 min=0 id="item{i}" name="item{i}" value="{nameValueDict['itemValue' + str(i)]}">
            <label for="roll">Artefakt:</label><input type="text" size=2 id="artifact{i}" name="artifact{i}" value="{nameValueDict['artifactValue' + str(i)]}">
            <input type="submit" name="pool_button{i}" value="Slå"><br>
            '''
    page = page + \
        f'''
        <label for="roll">Antal tärningskombinationer:</label><input type="text" id="no_of_combinations" name="no_of_combinations" value="{nameValueDict['no_of_combinations']}"><input type="submit" name="no_of_combinations_button" value="Ändra"><br>
        '''


    line = ""
    page += "<table border=10><tr><td><h3>Tärningspölen</h3>"
    try:
        print("Open pool file")
        with open("pool.txt", "r+") as f:
            print("Reading pool file")
            line = f.readline()
            if line != "":
                if line[0:4].find("POOL") == 0:
                    line = line[4:]
                    idx = line.find(":")+2
                    pool_roll = line[idx:]
                    tag = ""
                    tag_idx = line[4:].find("slog för")
                    if tag_idx != -1:
                        tag_idx += 9
                        tag = line[tag_idx:idx]
                        print(f"tag: {tag}")
                    line = line[0:idx]
                    print(pool_roll)
                    print(line)
                    formatted_pool_roll = format_pool_roll(pool_roll)
                    line += formatted_pool_roll
                    push_button = f'''<input type="hidden" name="pool_tag" id="pool_tag" value="{tag}">
                                      <input type="hidden" name="pool_roll" id="pool_roll" value="{pool_roll}">
                                      <input type="submit" name="push_button" value="Pressa">
                                      <input type="submit" name="no_push_button" value="Pressa inte">'''
                    print(line)
                    page += line + push_button
    except IOError:
        print("No pool file")
    page += "</td></tr></table>"

    page += "<h3>Tärningsslag</h3>"
    lines = ""
    line = ""

    try:
        with open("rolls.txt", "r+") as f:
            while True:
                line = f.readline()
                if line == "":
                    break
                if line[0:4].find("POOL") == 0:
                    line = line[4:]
                    pool_roll = line[line.find(":"):]
                    line = line[0:line.find(":")+2]
                    pool_roll = format_pool_roll(pool_roll)
                    line += pool_roll
                lines = line + "<br>" + lines
    except IOError:
        print("No rolls file")

    page = page + lines + "</form>"

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
    random_table = request.args.get("random_table", None)
    print(f"Name: {name}")
    print(f"Dice: {dice}")
    print(f"Question: {question}")
    print(f"Modifier: {modifier}")
    print(f"Kaos Factor: {kaos_factor}")
    print(f"Kaos Modifier: {kaos_modifier}")
    print(f"Random table: {random_table}")

    random.seed()

    read_stats()

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
    elif request.args.get('fate_question_button') is not None and question is not None and question != "" \
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
        socketio.emit('reload')
    
    elif request.args.get('detail_question_button') is not None and question is not None and question != "" \
            and kaos_modifier.lstrip('-').isnumeric():
        result1 = random.randint(1,10)
        result2 = random.randint(1,10)
        kaos_modifier_number = int(kaos_modifier)
        result = result1 + result2 + kaos_modifier_number
        answer = detail_check(result)
        with open("rolls.txt", "a+") as f:
            f.write("\n")
            f.write(f"Svar: {answer}!\n")
            f.write(f"Resultat: {result1} + {result2} + {kaos_modifier_number} = {result}\n")
            f.write(f"{name} frågade: {question}\n")
            f.write("\n")
        socketio.emit('reload')

    elif request.args.get('random_event_button') is not None:
        with open("rolls.txt", "a+") as f:
            focus = random_list(["event_focus"])[0]
            meaning_action1 = random_list(["meaning_action1"])[0]
            meaning_action2 = random_list(["meaning_action2"])[0]
            f.write(f"Händelse: {focus}, {meaning_action1} av {meaning_action2}\n")
        socketio.emit('reload')

    elif request.args.get('meaning_table_action_button') is not None:
        with open("rolls.txt", "a+") as f:
            meaning_action1 = random_list(["meaning_action1"])[0]
            meaning_action2 = random_list(["meaning_action2"])[0]
            f.write(f"{meaning_action1} av {meaning_action2}\n")
        socketio.emit('reload')

    elif request.args.get('meaning_table_description_button') is not None:
        with open("rolls.txt", "a+") as f:
            meaning_description1 = random_list(["meaning_descriptor1"])[0]
            meaning_description2 = random_list(["meaning_descriptor2"])[0]
            f.write(f"{meaning_description1} {meaning_description2}\n")
        socketio.emit('reload')        

    elif request.args.get('roll_button') is not None and roll is not None and roll != "":
        session['roll'] = roll
        result = parse_roll(roll)
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} slog {roll}, resultat: {result}\n")
        socketio.emit('reload')

    elif roll_dice and dice is not None and dice.isdigit():
        session['dice'] = dice
        result = random.randint(1,(int(dice)))
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} slog 1T{dice}, resultat: {result}\n")
        socketio.emit('reload')

    elif request.args.get('random_table_button') is not None:
        items = random_list(random_table.split())
        with open("rolls.txt", "a+") as f:
            f.write("\n")
            for item in reversed(items):
                f.write(item + "\n")
            f.write("\n")
        socketio.emit('reload')

    elif request.args.get('no_push_button') is not None:
        tag = request.args.get("pool_tag", "")
        pool_roll = request.args.get("pool_roll", None)
        with open("rolls.txt", "a+") as f:
            tag_text = ":"
            if tag != "":
                tag_text=f" för {tag}:"
            f.write(f"POOL {name} slog{tag_text} {pool_roll}")
        with open("pool.txt", "w+") as f:
            f.write("")
        socketio.emit('reload')

    elif request.args.get('push_button') is not None:
        tag = request.args.get("pool_tag", "")
        pool_roll = request.args.get("pool_roll", None)
        pool_roll = push_roll(pool_roll)
        with open("rolls.txt", "a+") as f:
            tag_text = ":"
            if tag != "":
                tag_text=f" för {tag}:"
            f.write(f"POOL {name} pressade och slog{tag_text} {pool_roll}\n")
        with open("pool.txt", "w+") as f:
            f.write("")
        socketio.emit('reload')

    elif request.args.get('junk_button') is not None:
        item = random_list(["skrot"])[0]
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} hittar: {item}\n")
        socketio.emit('reload')

    elif request.args.get('who_button') is not None:
        items = random_list("mutantnamn mutantsyssla egenhet egenhet".split())
        with open("rolls.txt", "a+") as f:
            f.write("\n")
            for item in reversed(items):
                f.write(item + "\n")
            f.write("\n")
        socketio.emit('reload')
    elif request.args.get('hide_button') is not None:
        session['combination'] = request.args.get('combination')
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} har dolt en kombination\n")
        socketio.emit('reload')
    elif request.args.get('show_button') is not None:
        with open("rolls.txt", "a+") as f:
            f.write(f"{name} visar kombination: {session['combination']}\n")
        session['combination'] = ""
        socketio.emit('reload')

    no_of_combinations = int(session.get('no_of_combinations', '3'))
    tag = ""
    base = ""
    skill = ""
    item = ""
    for i in range(1, no_of_combinations+1):
        if request.args.get(f'pool_button{i}') is not None:
            tag = request.args.get(f"tag{i}", None)
            base = request.args.get(f"base{i}", None)
            skill = request.args.get(f"skill{i}", None)
            item = request.args.get(f"item{i}", None)
            artifact = request.args.get(f"artifact{i}", None)
            break

    if base != "" and skill != "" and item != "":
        print(f"tag: {tag}")
        print(f"base: {base}")
        print(f"skill: {skill}")
        print(f"item: {item}")
        print(f"artifact: {artifact}")
        if base.isnumeric() and skill.isnumeric() and item.isnumeric():
            for i in range(1, no_of_combinations+1):
                session[f'tag{i}'] = request.args.get(f"tag{i}", None)
                session[f'baseValue{i}'] = request.args.get(f"base{i}", None)
                session[f'skillValue{i}'] = request.args.get(f"skill{i}", None)
                session[f'itemValue{i}'] = request.args.get(f"item{i}", None)
                session[f'artifactValue{i}'] = request.args.get(f"artifact{i}", None)
            baseValue = int(base)
            skillValue = int(skill)
            itemValue = int(item)
            artifactList = artifact.split(' ')
            artifactDice = []
            for a in artifactList:
                if a.isnumeric() and (a == "8" or a == "10" or a == "12"):
                    artifactDice.append(int(a))
            if baseValue >= 0 and skillValue >= 0 and itemValue >= 0:
                result = roll_pool(baseValue, skillValue, itemValue, artifactDice)
                print(f"pool roll: {result}")
                try:
                    with open("pool.txt", "r+") as f:
                        line = f.readline()
                        if line != "":
                            with open("rolls.txt", "a+") as f2:
                                f2.write(line)
                except IOError:
                    print("No pool file")
                with open("pool.txt", "w+") as f:
                    tag_text = ":"
                    if tag != "":
                        tag_text=f" för {tag}:"
                    f.write(f"POOL {name} slog{tag_text} {result}\n")
                socketio.emit('reload')
        print("not a numeric value")

    no_of_combinations = 3
    if request.args.get('no_of_combinations_button') is not None:
        no_of_combinations = request.args.get("no_of_combinations", "3")
        if no_of_combinations.isnumeric() and int(no_of_combinations) < 20:
            session['no_of_combinations'] = no_of_combinations

    write_stats()

    return redirect(url_for('index'))

@app.route('/')
def index():
    nameValueDict = {}
    nameValueDict['name'] = session.get('name', 'Anonym')
    nameValueDict['dice'] = session.get('dice', '20')
    nameValueDict['roll'] = session.get('roll', '')
    nameValueDict['combination'] = session.get('combination', '')
    nameValueDict['no_of_combinations'] = session.get('no_of_combinations', '3')
    no_of_combinations = int(nameValueDict['no_of_combinations'])
    for i in range(1, no_of_combinations + 1):
        nameValueDict[f'tag{i}'] = session.get(f'tag{i}', '')
        nameValueDict[f'baseValue{i}'] = session.get(f'baseValue{i}', '0')
        nameValueDict[f'skillValue{i}'] = session.get(f'skillValue{i}', '0')
        nameValueDict[f'itemValue{i}'] = session.get(f'itemValue{i}', '0')
        nameValueDict[f'artifactValue{i}'] = session.get(f'artifactValue{i}', '0')
    return generate_page(nameValueDict)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)