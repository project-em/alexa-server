from flask_ask import statement, question, session
from random import randint, choice

from server.communication.threaded_request import ThreadedRequest
from server.app import cache, ask, app

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("PressButtonIntent", convert = {'color': str})
def press_button(color):
    command = 0
    if (color == 'red'): command = 1
    elif(color == 'blue'): command = 2
    elif(color == 'green'): command = 3
    elif(color == 'yellow'): command = 4
    reqs = ThreadedRequest(app.config.ROOT_URL + '/alexa', RequestType.Post, data={'command' : command})
    button_msg = render_template('press', buttonMsg = color)
    return question(button_msg)

@ask.intent("QuitIntent")
def quit():
    return statement(render_template('quit'))

@ask.intent("QueryWorldIntent")
def query_world():
    reqs = ThreadedRequest(app.config.ROOT_URL + '/alexa', RequestType.Post, data = {'command' : 0})
    return question(buildQueryList(getQueryList()))

@ask.intent("NumberIntent")
def number_query():
    reqs = ThreadedRequest(app.config.ROOT_URL + '/alexa', RequestType.Post, data={'command' : 5})
    return question(buildSayList(getSpeech()))

@app.route('/say', methods=['POST'])
def execute_random():
    cache.set('speech', request.json['speech'])
    return 'ok'

def buildSayList(speech):
    numbers = [randint(0, 9) for _ in range(4)]
    session.attributes['numbers'] = numbers
    return render_template('numbers', speechStr = numbers)

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int, 'fourth': int})
def answer(first, second, third, fourth):
    if (session.attributes.get('numbers')):
        winning_numbers = session.attributes['numbers']
    else:
        return statement(render_template('lose'))
    if [first, second, third, fourth] == winning_numbers:
        msg = render_template('win')
        reqs = ThreadedRequest(app.config.ROOT_URL + '/alexa', RequestType.Post, data={'command' : 6})
    else:
        msg = render_template('lose')
    return statement(msg)


@ask.intent("LocationIntent")
def locate_surounding():
    reqs = ThreadedRequest(app.config.ROOT_URL + '/alexa', RequestType.Post, data={'command' : 0})
    return question(buildQueryList(getQueryList()))

@ask.intent("NameIntent")
def about_self():
    about_str = choice(
            ['You know who I am. I am Em. Stuck here in the world of despair, longing for you. Please come save me', 
            'What\'s wrong? Do you not think its me? IT IS I, Em' , 
            'What do you mean? I am your wife Em',
            'You tell me. What do you think?']
    )
    return question(render_template('about', aboutStr = about_str))

@ask.intent("ComplimentIntent")
def compliment():
    compliment_str = choice(
            ['Thank you', 
            'No problem' , 
            'We make a good team',
            'Any time']
    )
    return question(render_template('compliment', complimentStr = compliment_str))

@ask.intent("RomanceIntent")
def romance():
    romance_str = choice(
    ["Lets get out of here first",
    "Can we focus please",
    "I am blushing"]
    )
    return question(render_template('romance', romanceStr = romance_str))

@ask.intent("WellnessIntent")
def wellness():
    wellness_str = choice(
    ["I am a little lost",
    "I am okay, but want to find you",
    "Lets just figure this out"]
    )
    return question(render_template('wellness', wellnessStr = wellness_str))

@ask.intent("InstructionIntent")
def instruction():
    instruction_str = choice(
    ['I cant see where you are, but check your surroundings',
    'There are colored buttons in this room, do you see any in yours',
    'Dont worry, we will figure this out, try to look for doors around you']
    )
    return question(render_template('instruction', instructionStr = instruction_str))

@ask.intent("DespairIntent")
def despair():
    despair_str = choice(
    ['everything is gonna be okay']
    )
    return question(render_template('despair', despairStr = despair_str))
