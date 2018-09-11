"""
This is a game that not only enriches your memory but also teaches you about the rich history of various Indian cities.
Begin by saying an Indian city, and alexa will add another Indian city and also tell you a fact about it. Each time you say a new word, you must repeat the previous word in order. 
You get a point for saying the list of cities n the right order in each round. 
Randomly, alexa could also state a fact about a city and ask you the corresponding city name. On giving the right answer, you get awarded 10 bonus points.
Once you have learnt about all the cities, or get the order of cities wrong, the game ends..
"""

from __future__ import print_function

import random
import Queue

memoryList = []
checkQueue = Queue.Queue(maxsize=20)
flag = 0
answerQueue = Queue.Queue(maxsize=2)
scoreQueue = Queue.Queue(maxsize=2)


cityDetails = {
    "Delhi"     : "The national capital of our country was, originally, a walled city! This city had 14 gates of which only 5 are remaining namely Turkman Gate, Ajmeri Gate, Delhi Gate, Lahori Gate, and Kashmiri Gate. " +
                  "It is the world's second most bird-rich capital city after Nairobi in Kenya. ",
    "Mumbai" : "This city was given away by the Portuguese to England when King Charles II of England married Princess Catherine de Braganza of Portugal. ", 
    "Hyderabad" : "This city, which is also known as the city of pearls, is home to the world famous Biriyani, world's biggest monolithic Buddha statue, film studio and snow themed park, and the rarest of rare - Kohinoor diamond!" + 
                  " It is considered as one of the oldest rock formations on the planet, around 2500 million years old, and boasts of an opulent heritage. " ,
    "Bangalore" : "Founded by Kempe Gowda of Vijayanagara empire, this comparatively younger city has many sobriquets like 'The Silicon Valley of India', 'The Garden City of India' etc. " +
                    " It's not just cats and dogs, here, you could also see raining engineers! The IT hub has the highest percentage of engineers in the world and houses 212 software companies in its heart.",
    "Ahmedabad" : "Gets its name from Ahmedshah Badshah who ruled the city in the 14th Century. Has been ruled by  Mughals, Marathas and  British empire before Independence. ",
    "Kolkota"   : "It was this city which was India's capital till 1912!? This city is one of the few rail tram cities in the world. " + 
                  "It is also a heaven for bookworms with this city's book fair being recognised as one of the world's largest conglomeration of books and is also the most-attended book fair in the world! ",
    "Surat"     : "The East India Company started docking in here from 1608 for trade. The port city is situated on the banks of Tapi river. Known for diamonds. ninety percent of the world's rough cut diamonds are polished and cut here. ",
    "Jaipur"    : "The city was painted pink under the rule of Sawai Ram Singh to welcome Prince Edward of Wales. This city holds worlds world's larg literary festival. ",
    "Lucknow"   : "Is famous for its embroidery work called Chikankari. The Awadhi cuisine of this city has a unique place in the history of Indian cuisine. ",
    "Nagpur"    : "This city is known as Orange City. The city was founded by Bakht Buland Shah and later became part of Maratha Empire under Bhonsale dynasty. ",
    "Indore"    : "This city is the largest consumer of Poha in the world. One of the 100 cities to be developed as part of Smart Cities Mission. "
}


cityList = [
    "Delhi",
    "Mumbai",
    "Hyderabad",
    "Bangalore",
    "Ahmedabad",
    "Kolkata",
    "Surat",
    "Jaipur",
    "Lucknow",
    "Nagpur",
    "Indore"
]

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
   
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Indialogy. Let's learn a few things about India today. Begin the game by saying My word is and an Indian city name. For example, my word is Bangalore. " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = False
    memoryList = []
    flag = 1
    scoreQueue.put(0)
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for your interest in India. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    '''for element in memoryList :
        memoryList.remove(element)
    while True:
        if checkQueue.empty() :
            break
        removed_element = checkQueue.get()
    '''
    reprompt_text = speech_output
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_word_attributes(players_word):
    return {"players_word": players_word}


def set_word_in_session(intent, session):
    """ Alexa acknowledges the user's city and adds nother city to the list with a fact on it
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Word' in intent['slots']:
        players_word = intent['slots']['Word']['value']
        if players_word not in cityList :
            speech_output = "I do not know this city. Please name another city. "
        else : 
            if players_word not in memoryList : 
                memoryList.append(players_word)
                checkQueue.put(players_word)
                session_attributes = create_word_attributes(players_word)
                speech_output = "I now know your word is " + \
                                players_word + \
                                ". " + \
                                "The list of words are "
                for element in memoryList:
                    speech_output = speech_output + element + ","
                if(len(cityList)==len(memoryList)):
                    speech_output = speech_output + "You have learnt all the cities I know about. "
                    should_end_session = True
                else : 
                    while True : 
                        alexa_word = cityList[random.randint(0,len(cityList)-1)]
                        if alexa_word not in memoryList :
                            break
                    speech_output = speech_output + " and " + alexa_word +". Fact about " + alexa_word + " : "
                    speech_output = speech_output + cityDetails[alexa_word] 
                    speech_output = speech_output + "Now repeat the list of words. "
                    memoryList.append(alexa_word)
                    checkQueue.put(alexa_word)
                    reprompt_text = None
            else:
                speech_output = "Word already used. "
                reprompt_text = None
                if(len(cityList)==len(memoryList)):
                    speech_output = speech_output + "You have learnt all the cities I know about. "
                    should_end_session = True
            
    else:
        speech_output = "Error"
        reprompt_text = None
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def make_user_word(intent, session):
    """ When the user doesn't know anymore indian city name, and calls for 'help', alexa gives a city name on behalf of the player.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if(len(cityList)==len(memoryList)):
        speech_output = speech_output + "You have learnt all the cities I know about. "
        should_end_session = True
    else : 
        while True : 
            player_alexa_word = cityList[random.randint(0,len(cityList)-1)]
            if player_alexa_word not in memoryList :
                            break
        speech_output = "Your word is " + player_alexa_word + ". "
        memoryList.append(player_alexa_word)
        checkQueue.put(player_alexa_word)
        speech_output = "Your word is " + \
                                    player_alexa_word + \
                                    ". " + \
                                    "The list of words are "
        for element in memoryList:
            speech_output = speech_output + element + ","
        if(len(cityList)==len(memoryList)):
            speech_output = speech_output + "You have learnt all the cities I know about. "
            should_end_session = True
        else : 
            while True : 
                alexa_word = cityList[random.randint(0,len(cityList)-1)]
                if alexa_word not in memoryList :
                    break
            speech_output = speech_output + " and " + alexa_word +". Fact about " + alexa_word + " : "
            speech_output = speech_output + cityDetails[alexa_word] 
            speech_output = speech_output + "Now repeat the list of words. "
            memoryList.append(alexa_word)
            checkQueue.put(alexa_word)
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_list_prompt(intent, session):
    ''' Prompts the user to start the list of cities '''
    session_attributes = {}
    speech_output = "Go on"
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def check_answer(intent, session):
    ''' checks the player's answer to the fact question'''
    session_attributes = {}
    reprompt_text = None
    speech_output = "Checking Answer. "
    answer = answerQueue.get()
    if 'Word' in intent['slots']:      
        players_answer = intent['slots']['Word']['value']
        if(players_answer==answer):
            speech_output = speech_output + "That's the right answer! "
            scoreNow = scoreQueue.get()
            scoreNow = scoreNow + 10
            scoreQueue.put(scoreNow)
            speech_output = speech_output + "Congrats! You have earned 10 bonus points. Your score is now " + str(scoreNow) + " . "
            speech_output = speech_output + "Now, tell your word. "
        else:
            speech_output = speech_output + "Sorry, that's the wrong answer! " + "Right answer is " + answer
    should_end_session = False
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def check_this_word(intent, session):
    ''' checks the user word with the list word. If all the words are right, alexa randomly asks a fact about a city '''
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = False
    card_title = intent['name']
    if(checkQueue.empty()):
        speech_output = speech_output + "You have already said all the words correctly. "
        for element in memoryList:
            checkQueue.put(element)
    elif 'Word' in intent['slots']:
        correct_word = checkQueue.get()
        current_word = intent['slots']['Word']['value']
        if(current_word == correct_word):
            speech_output = speech_output + "Correct. "
            if(checkQueue.empty()):
                scoreNow = scoreQueue.get()
                scoreNow = scoreNow + 1
                scoreQueue.put(scoreNow)
                speech_output = speech_output + "You have said all the words correctly. " + \
                "Your score is now " + str(scoreNow) + " . " + \
                "This statement reminds you of which city? "
                qst_no = random.randint(0,len(memoryList)-1)
                if(qst_no%1==0):
                    speech_output = speech_output +  cityDetails[memoryList[qst_no]] + " . "
                    answerQueue.put(memoryList[qst_no])
                    speech_output = speech_output + "Begin your answer with My answer is . "
                for element in memoryList:
                    checkQueue.put(element)
            else:
                speech_output = speech_output + "Go on. "
        else:
            speech_output = speech_output + "Incorrect. Correct answer is " + correct_word + " Game ended with a score" + str(len(memoryList)) + ". "
            should_end_session = True
            handle_session_end_request()
            
    else:
        speech_output = speech_output + "Word unchecked"
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyWordIsIntent":
        return set_word_in_session(intent, session)
    elif intent_name == "TheListIsIntent":
        return get_list_prompt(intent, session)
    elif intent_name == "MyAnswerIsIntent":
        return check_answer(intent, session)
    elif intent_name == "WordFromMemoryIntent":
        return check_this_word(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return make_user_word(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
