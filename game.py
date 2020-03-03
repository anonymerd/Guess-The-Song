import random
import speech_recognition as sr
import os
from string import capwords
from playsound import playsound
from gtts import gTTS


def speak(text):
    tts = gTTS(text=text, lang = 'en')
    fileName = "voice.mp3"
    tts.save(fileName)
    print(text)
    playsound(fileName)
    os.remove(fileName)


def getAudio() :
      r = sr.Recognizer()

      with sr.Microphone() as source:
          print("Adjusting sound for ambient noise...")
          r.adjust_for_ambient_noise(source)

          print("Listening...")
          audio = r.listen(source)
          said = ""

          try:
              print("Sending sound to Google Servers...")
              said = r.recognize_google(audio)
              print("Your Response : " + said)
          except Exception as e:
              print("Sorry, didn't get that one. Let's go again")
              said = getAudio()

          return said

def generateRandomPlaylist(genre, noOfQuestions):
    availableSongs = os.listdir("Songs\\{}".format(genre))
    randomPlaylist = [availableSongs[x] for x in random.sample(range(0, len(availableSongs)), noOfQuestions)]
    return randomPlaylist


def play():
    availableLang = ("English", "Hindi")
    validNoOfQues = ('3', '5', '7')

    text  = "Hi, This is Stan. Let's start by knowing your name."
    speak(text)
    print("Tell us your name.")
    userName = getAudio()

    text = "Hi There, " + userName + ". Let's get started.\nChoose your language."
    speak(text)

    while True:
        print("Choose your language")
        lang = getAudio()
        if lang in availableLang:
            break
        else:
            text = "Sorry, This option is not available. Choose a valid option."
            speak(text)

    if lang == "English":
        lang = 'en'
        text = "These are list of genres you can select : "
        speak(text)

        genreList = os.listdir("Songs")
        for i in genreList:
            print("{}".format(capwords(i)), end="")
        print()

        text = "For example if you want to choose Hip Hop, just say 'Hip Hop'"
        speak(text)

        while True:
            print("Choose your Genre")
            genre = getAudio()
            if genre in genreList:
                break
            else:
                text = "Sorry, This option is not available. Choose a valid option."
                speak(text)

        text = "Now, tell me how many questions do you want to answer.\nYou can say 3, 5 or 7"
        speak(text)

        while True:
            print("Choose Number of Questions")
            noOfQuestions = getAudio()
            if noOfQuestions in validNoOfQues:
                break
            else:
                text = "Sorry, This option is not available. Choose a valid option."
                speak(text)


        text = "Great! Now let me tell you about the scoring system. For each song played, you have to guess the name of the song correctly for 10 points, and if you get the name of the artist as well, you get a bonus 10."
        speak(text)

        # genre = "hip hop"

        randomPlaylist = generateRandomPlaylist(genre, int(noOfQuestions))
        playerScore = 0
        quesScore = 0

        position = {
            '1' : "first",
            '2' : "second",
            '3' : "third",
            '4' : "fourth",
            '5' : "fifth",
            '6' : "sixth",
            '7' : "seventh"
        }

        position[noOfQuestions] = "last"
        # print(randomPlaylist[0])

        for i in range(len(randomPlaylist)):
            text = "Here is the {} song.".format(position[str(i+1)])
            speak(text)

            playsound("Songs\\{}\\{}".format(genre, randomPlaylist[i]))
            songName = randomPlaylist[i].split("-")[0];
            artistName = randomPlaylist[i].split("-")[1].replace(".mp3", "").split(",");

            # print("Your Response : ")

            # response = input("Enter response : ")

            # print(songName)
            # print(artistName)

            response = getAudio()

            songResponse = ""
            artistResponse = ""

            response = response.split(" by ")
            if len(response) > 1:
                songResponse = response[0].lower()
                artistResponse = response[1].lower()
            else:
                songResponse = response[0].lower()
                artistResponse = response[0].lower()

            if songResponse in songName and artistResponse in artistName:
                quesScore = 20
                text = "Wow! You get the song as well as the artist correct."
            elif songResponse in songName:
                quesScore = 10
                text = "Great! You get the song correct."
            elif artistResponse in artistName:
                quesScore = 10
                text = "Wonderful! You get the artist correct."
            else:
                text = "Sorry!"

            playerScore += quesScore
            text += "The song is '" + capwords(songName) + "' by '" + capwords(artistName[0]) + "'. You scored " + str(quesScore) + " points on this question. Your current score is '" + str(playerScore) + "'"
            speak(text)

        text = "Thank you for playing."
        speak(text)


    elif lang == 'Hindi':
        lang = 'hi'
        text = "Sorry, Hindi language is not functional yet.....\nPlease select English"
        speak(text)

# playsound.playsound("Songs\\hip hop\\.mp3")
play()
