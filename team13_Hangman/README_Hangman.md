# Hangman Word Game

A browser-based Hangman word-guessing game built with **Python, Flask,
HTML, CSS, and JavaScript**. The Flask version uses Python for game
logic and API handling, while the frontend displays the game and sends
player guesses to the backend.

The project also includes an optional standalone HTML version that runs
its game logic in the browser without Flask.

## Features

-   Randomly selects a word from a predefined collection of 12 words.
-   Displays a category and a question for the selected word.
-   Automatically reveals **two distinct letters** at the start of each
    round.
-   Counts automatically revealed letters as already guessed, so they do
    not reduce the player's attempts.
-   Supports guesses through both the on-screen A--Z keyboard and the
    physical keyboard.
-   Shows correct and incorrect guesses using different button styles.
-   Updates the Hangman drawing after each incorrect guess.
-   Allows up to six incorrect guesses per round.
-   Provides an additional hint.
-   Tracks wins and losses during the Flask session.
-   Allows the player to start a new round.
-   Uses a responsive layout for smaller screens.

## Technologies Used

  -----------------------------------------------------------------------
  Technology                          Use
  ----------------------------------- -----------------------------------
  Python                              Implements the game rules, word
                                      selection, validation, and
                                      game-state updates

  Flask                               Runs the web server and provides
                                      backend API routes

  HTML                                Defines the game page structure

  CSS                                 Styles the interface and makes the
                                      layout responsive

  JavaScript                          Handles keyboard input, API
                                      requests, and dynamic page updates

  JSON                                Transfers game data between the
                                      browser and Flask
  -----------------------------------------------------------------------

## Project Structure

``` text
team13_Hangman/
├── app.py
├── requirements.txt
├── hangman_word_game.html
└── templates/
    └── index.html
```

### File descriptions

-   **`app.py`** -- Flask application. Contains the word bank, game
    initialization, session-based game state, guess validation, hint
    handling, and API routes.
-   **`templates/index.html`** -- Frontend used by the Flask
    application. Contains HTML, CSS, and JavaScript. JavaScript
    communicates with the Flask backend.
-   **`hangman_word_game.html`** -- Optional standalone version. It
    contains its own HTML, CSS, and JavaScript game logic and can be
    opened directly in a browser. It does not use the Flask backend.
-   **`requirements.txt`** -- Lists the Python packages required to run
    the Flask version.

> **Important:** To run the Flask application, keep
> `templates/index.html` inside a folder named `templates` at the same
> level as `app.py`. Flask loads it through
> `render_template("index.html")`.

## Getting Started -- Flask Version

### Prerequisites

-   Python 3.9 or later
-   pip (Python package installer)
-   A web browser

### 1. Clone the repository

Replace the placeholders with your GitHub username and repository name.

``` bash
git clone https://github.com/<your-username>/<your-repository-name>.git
cd <your-repository-name>
```

### 2. (Recommended) Create a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents script activation, use Command Prompt:

``` bat
venv\Scripts\activate.bat
```

**macOS / Linux:**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

The `requirements.txt` file installs Flask.

### 4. Run the application

``` bash
python app.py
```

### 5. Open the game

Open this URL in your browser:

``` text
http://127.0.0.1:5000
```

To stop the Flask development server, press `Ctrl + C` in the terminal.

## How to Play

1.  Open the application. A random word, category, and question are
    displayed.
2.  Two distinct letters are revealed automatically at the beginning of
    the round.
3.  Guess a letter by clicking an on-screen alphabet button or pressing
    a key from A to Z.
4.  Correct guesses reveal every matching occurrence of that letter in
    the word.
5.  Incorrect guesses add a part to the Hangman drawing and reduce the
    remaining attempts.
6.  Click **Show hint** to display an additional clue.
7.  Guess all letters before reaching six incorrect guesses to win.
8.  Click **New Game** to start another round.

A letter that has already been guessed, including an automatically
revealed letter, cannot be guessed again. Automatically revealed letters
do not consume attempts.

## Flask API Routes

The Flask frontend communicates with these routes:

  HTTP method   Endpoint       Purpose
  ------------- -------------- ------------------------------------------
  `GET`         `/`            Loads the game page
  `GET`         `/api/game`    Returns the current game state
  `POST`        `/api/guess`   Validates and processes a guessed letter
  `POST`        `/api/hint`    Makes the current hint available
  `POST`        `/api/new`     Starts a new round

### Example guess request

The browser sends a JSON request to `POST /api/guess`:

``` json
{
  "letter": "A"
}
```

Flask validates the input, updates the game state, and returns the
updated state as JSON.

## How the Game Logic Works

1.  Flask selects a random entry from the predefined `WORDS` list.
2.  It extracts the unique letters in the selected answer.
3.  It randomly chooses up to two distinct letters to reveal.
4.  The revealed letters are stored as already-guessed letters in the
    session.
5.  When a player submits a guess, Flask validates that it is one ASCII
    letter from A to Z.
6.  If the letter is not in the answer, the incorrect-guess count
    increases.
7.  The player wins when every character in the answer has been guessed.
8.  The player loses after six incorrect guesses.

## Run the Standalone HTML Version

The optional standalone version does not require Flask.

1.  Locate `hangman_word_game.html` in the project folder.
2.  Open the file directly in a modern web browser.
3.  Play using the on-screen keyboard or your physical keyboard.

The standalone version maintains its own game logic in JavaScript. Its
game state and scores are separate from the Flask version.

## Configuration and Security Notes

This project is intended for learning and local development.

-   The Flask app currently uses a fallback secret key for
    demonstration. Before deployment, configure a strong private
    `SECRET_KEY` environment variable and do not commit it to GitHub.
-   Flask's default session is stored in a signed browser cookie. The
    signature protects integrity but does not encrypt the cookie
    contents. For a production version, keep the answer and sensitive
    game state on the server using server-side sessions or a database.
-   The word bank is currently stored directly in `app.py`; no database
    is required.
-   `debug=True` is enabled for local development. Disable debug mode
    and use a production WSGI server when deploying.

## Possible Future Enhancements

-   Store words, categories, and hints in a database.
-   Add player accounts and persistent score history.
-   Create a leaderboard.
-   Add difficulty levels with different attempt limits.
-   Add automated unit and integration tests.
-   Improve accessibility and add more language options.

## Troubleshooting

### `TemplateNotFound: index.html`

Check that the project structure includes:

``` text
templates/
└── index.html
```

The `templates` folder must be at the same directory level as `app.py`.

### `ModuleNotFoundError: No module named 'flask'`

Install the project dependencies:

``` bash
pip install -r requirements.txt
```

### Port 5000 is already in use

Stop the other application using port 5000, or change the port in the
`app.run(...)` configuration in `app.py`.

## Project

**Team:** Team 13

Add the team members' names and their contributions here before
publishing, if required.
