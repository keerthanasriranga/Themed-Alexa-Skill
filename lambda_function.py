"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

import random
import Queue

memoryList = []
checkQueue = Queue.Queue(maxsize=20)
flag = 0
answerQueue = Queue.Queue(maxsize=2)
scoreQueue = Queue.Queue(maxsize=2)


countryDetails = {
    "Delhi"     : "The national capital of our country was, originally, a walled city! This city had 14 gates of which only 5 are remaining namely Turkman Gate, Ajmeri Gate, Delhi Gate, Lahori Gate, and Kashmiri Gate." +
                  "It is the world's second most bird-rich capital city after Nairobi in Kenya.",
    "Mumbai" : "This city was given away by the Portuguese to England when King Charles II of England married Princess Catherine de Braganza of Portugal.", 
    "Hyderabad" : "This city, which is also known as the city of pearls, is home to the world famous Biriyani, world's biggest monolithic Buddha statue, film studio and snow themed park, and the rarest of rare - Kohinoor diamond!" + 
                  " It is considered as one of the oldest rock formations on the planet, around 2500 million years old, and boasts of an opulent heritage. The last Nizam of Hyderabad is considered to be the all time richest Indian; he had a diamond paperweight worth 50 million pounds!! " ,
    "Mysore"    : "Palace capital of Karnataka. ",
    "Bangalore" : "IT Capital of India. ",
    "Ahmedabad" : "Gets its name from Ahmedshah Badshah who ruled the city in the 14th Century. Has been ruled by  Mughals, Marathas and  British empire before Independence. ",
    "Kolkota"   : "It was this city which was India's capital till 1912!? This city is one of the few rail tram cities in the world. " + 
                  "It is also a heaven for bookworms with this city's book fair being recognised as one of the world's largest conglomeration of books and is also the most-attended book fair in the world! ",
    "Pune"      : "Pune lies in earthquake prone region. Renowned for its educational institutes, it is called Oxford Of The East. " + 
                  " It was once the base of the Peshwas (prime ministers) of the Maratha Empire, which lasted from 1674 to 1818. ",
    "Chennai" : "Capital of Tamil Nadu. "
}


countryList = [
    "Delhi",
    "Mumbai",
    "Hyderabad",
    "Mysore",
    "Bangalore",
    "Ahmedabad",
    "Kolkata",
    "Pune",
    "Chennai"
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
    speech_output = "Welcome to the Alexa Memory Game. Begin the game by saying My word is and an Indian city name. For example, my word is Bangalore. " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = False
    memoryList = []
    flag = 1
    scoreQueue.put(0)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Word' in intent['slots']:
        players_word = intent['slots']['Word']['value']
        memoryList.append(players_word)
        checkQueue.put(players_word)
        session_attributes = create_favorite_color_attributes(players_word)
        speech_output = "I now know your word is " + \
                        players_word + \
                        ". " + \
                        "The list of words are "
        for element in memoryList:
            speech_output = speech_output + element + ","
        while True : 
            alexa_word = countryList[random.randint(0,len(countryList)-1)]
            if alexa_word not in memoryList :
                break
        speech_output = speech_output + " and " + alexa_word +". Fact about this city : "
        speech_output = speech_output + countryDetails[alexa_word] 
        speech_output = speech_output + "Now repeat the list of words. "
        memoryList.append(alexa_word)
        checkQueue.put(alexa_word)
        reprompt_text = None
    else:
        speech_output = "Error"
        reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_list_prompt(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = "Go on"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def check_answer(intent, session):
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
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def check_this_word(intent, session):
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
                    speech_output = speech_output +  countryDetails[memoryList[qst_no]] + " . "
                    answerQueue.put(memoryList[qst_no])
                    speech_output = speech_output + "Begin your answer with My answer is . "
                for element in memoryList:
                    checkQueue.put(element)
            else:
                speech_output = speech_output + "Go on. "
        else:
            speech_output = speech_output + "Incorrect. Correct answer is " + correct_word + " Game ended with a score" + str(len(memoryList)) + ". "
            should_end_session = True
    else:
        speech_output = speech_output + "Word unchecked"
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
        return set_color_in_session(intent, session)
    elif intent_name == "TheListIsIntent":
        return get_list_prompt(intent, session)
    elif intent_name == "MyAnswerIsIntent":
        return check_answer(intent, session)
    elif intent_name == "WordFromMemoryIntent":
        return check_this_word(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
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
