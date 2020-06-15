from game import Game
from player import Player


def play():

    newGame = Game()
    text = "Hi, This is Stan. Let's start by knowing your name."
    Game.speak(text)

    print("Tell us your name.")
    userName = Game.getAudio()

    text = "Hi There, " + userName + ". Let's get started."
    Game.speak(text)

    lang = newGame.getLang()

    genre = newGame.getGenre()

    noOfQuestions = newGame.getNoOfQues()

    currPlayer = Player(userName, lang, genre, noOfQuestions)

    text = "Great! Now let me tell you about the scoring system. For each song played, you have to guess the name of the song correctly for 10 points, and if you get the name of the artist as well, you get a bonus 10."
    Game.speak(text)

    newGame.start(currPlayer)

    text = "Do you want to play again?"
    Game.speak(text)

    userResponse = Game.getAudio()

    if userResponse.lower() in ("yes", "ya", "yo", "sure", "of course"):
        play()
    else:
        text = f"OK, Thank You {userName} for playing."
        Game.speak(text)


play()
