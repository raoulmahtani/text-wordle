from xmlrpc.client import DateTime
import requests
import logging
from flask import Flask
from datetime import datetime

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
app = Flask(__name__)

#if the app is going to be client side - client will retrieve word, and handle guesses in webapp
@app.route("/word")
def get_word():
    r = requests.get("https://random-word-api.herokuapp.com/word?number=100")
    words = r.json()
    logging.debug("testing if http response contained any 5 letter words")
    word = [x for x in words if len(x) == 5]
    if len(word) == 0:
        logging.error("response did not contain any 5 letter words, retrying")
        get_word()
    else:
        logging.debug("5 letter word found - "+  word[0])
        return word[0]

#if the app is going to be server-side - client will hit guess endpoint and receive json object back
""" 
where 'x' is the index of the letter between 0 and 4
{
    "x": "correct|wrong_place|not_in_word"
}
"""
@app.route("/word/<guess>")
def guess_word(guess):
    response = {}
    #weed out attempts to break app - invalid length
    if len(guess) != len(word):
        logging.error("guess length is not equal to word length")
        response["error"] = "Guess length invalid"
        return response ,400
    #if not a word - exit
    elif guess.isalpha() != True:
        logging.error("guess is not alpha")
        response["error"] = "Guess not a word"
        return ["error"],400
    #we can carry on from here
    else:
        logging.debug("valid guess submitted - checking against word")
        for i in range(len(guess)):
            if guess[i] == word[i]:
                response[i] = "correct"
            elif guess[i] in word:
                response[i] = "wrong_place"
            else:
                response[i] = "not_in_word"
    return response

word = get_word()
print(word)

