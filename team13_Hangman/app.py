import os
import random
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hangman-demo-secret-change-this")

WORDS = [
    {
        "word": "PYTHON",
        "category": "Programming",
        "question": "Which programming language is named after the British comedy group Monty Python?",
        "hint": "It is often used for automation, data analysis, and web development.",
    },
    {
        "word": "DATABASE",
        "category": "Technology",
        "question": "What do we call an organized collection of information that can be stored, searched, and updated?",
        "hint": "SQL is commonly used to work with this.",
    },
    {
        "word": "KEYBOARD",
        "category": "Computer",
        "question": "Which computer input device has keys that you press to type letters and numbers?",
        "hint": "It is usually placed in front of a computer monitor.",
    },
    {
        "word": "INTERNET",
        "category": "Technology",
        "question": "What worldwide network connects computers and allows people to share information?",
        "hint": "You use it to browse websites and send email.",
    },
    {
        "word": "ALGORITHM",
        "category": "Computer Science",
        "question": "What is a step-by-step set of instructions used to solve a problem?",
        "hint": "Programmers design these before or while writing code.",
    },
    {
        "word": "JAVASCRIPT",
        "category": "Programming",
        "question": "Which programming language is widely used to make websites interactive?",
        "hint": "It runs in web browsers and is often abbreviated as JS.",
    },
    {
        "word": "ELEPHANT",
        "category": "Animals",
        "question": "Which large land animal is known for its trunk and long tusks?",
        "hint": "It is the largest living land animal.",
    },
    {
        "word": "RAINBOW",
        "category": "Nature",
        "question": "What colourful arc can appear in the sky when sunlight shines through raindrops?",
        "hint": "It is often described as having seven colours.",
    },
    {
        "word": "NOTEBOOK",
        "category": "Education",
        "question": "What do students commonly use to write notes during a class?",
        "hint": "It usually contains pages bound together.",
    },
    {
        "word": "SATELLITE",
        "category": "Science",
        "question": "What object orbits a planet, such as the Moon orbiting Earth?",
        "hint": "Some of these are used for GPS and communication.",
    },
    {
        "word": "HOSPITAL",
        "category": "Places",
        "question": "Where do people go to receive medical treatment and care?",
        "hint": "Doctors and nurses work here.",
    },
    {
        "word": "CRICKET",
        "category": "Sports",
        "question": "Which bat-and-ball sport is played between two teams of eleven players?",
        "hint": "The game can be played in T20, One Day, and Test formats.",
    },
]


def start_new_game():
    previous = session.get("answer")
    choices = [item for item in WORDS if item["word"] != previous] or WORDS
    selected = random.choice(choices)
    session["answer"] = selected["word"]
    session["category"] = selected["category"]
    session["question"] = selected["question"]
    session["hint"] = selected["hint"]
    # Automatically reveal two different letters at the start of each round.
    # Revealed letters are treated as already guessed, so they do not cost attempts.
    unique_letters = list(dict.fromkeys(selected["word"]))
    revealed_letters = random.sample(unique_letters, k=min(2, len(unique_letters)))
    session["revealed"] = revealed_letters
    session["guessed"] = revealed_letters.copy()
    session["wrong"] = 0
    session["status"] = "playing"
    session["hint_shown"] = False


def ensure_game():
    if "answer" not in session:
        session["wins"] = 0
        session["losses"] = 0
        start_new_game()


def game_state():
    ensure_game()
    answer = session["answer"]
    guessed = set(session.get("guessed", []))
    wrong = session.get("wrong", 0)
    status = session.get("status", "playing")
    display_word = [letter if letter in guessed or status == "lost" else "" for letter in answer]
    return {
        "category": session["category"],
        "question": session["question"],
        "display_word": display_word,
        "guessed_letters": sorted(guessed),
        "revealed_letters": sorted(session.get("revealed", [])),
        "wrong_guesses": wrong,
        "attempts_left": max(0, 6 - wrong),
        "status": status,
        "hint": session["hint"] if session.get("hint_shown") else None,
        "wins": session.get("wins", 0),
        "losses": session.get("losses", 0),
        "answer": answer if status in ("won", "lost") else None,
    }


@app.get("/")
def home():
    ensure_game()
    return render_template("index.html")


@app.get("/api/game")
def get_game():
    return jsonify(game_state())


@app.post("/api/guess")
def make_guess():
    ensure_game()
    data = request.get_json(silent=True) or {}
    letter = str(data.get("letter", "")).strip().upper()
    if len(letter) != 1 or not letter.isalpha() or not letter.isascii():
        return jsonify({"error": "Enter one letter from A to Z."}), 400
    if session["status"] != "playing":
        return jsonify({"error": "This game is over. Start a new game."}), 409

    guessed = set(session.get("guessed", []))
    if letter in guessed:
        return jsonify(game_state())
    guessed.add(letter)
    session["guessed"] = sorted(guessed)

    answer = session["answer"]
    if letter not in answer:
        session["wrong"] = session.get("wrong", 0) + 1
    if all(char in guessed for char in answer):
        session["status"] = "won"
        session["wins"] = session.get("wins", 0) + 1
    elif session.get("wrong", 0) >= 6:
        session["status"] = "lost"
        session["losses"] = session.get("losses", 0) + 1

    session.modified = True
    return jsonify(game_state())


@app.post("/api/hint")
def show_hint():
    ensure_game()
    session["hint_shown"] = True
    session.modified = True
    return jsonify(game_state())


@app.post("/api/new")
def new_game():
    ensure_game()
    start_new_game()
    return jsonify(game_state())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
