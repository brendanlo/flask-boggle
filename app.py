from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.post("/api/score-word")
def check_if_word_is_valid():
    """checks if word is valid and returns a JSON string of 
    "ok" if it is, returns "not-word" if the word isn't in the dictionary
    returns not-on-board if the word can't be found on the 
    board identified by gameId"""

    game_id = request.json["gameId"]

    breakpoint()

    word = request.json["word"]
    game = games[game_id]

    word_in_wordlist = game.is_word_in_word_list(word)
    word_on_board = game.check_word_on_board(word)

    if not word_in_wordlist:
        return jsonify({"result": "not-word"})
    elif not word_on_board:
        return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "ok"})
