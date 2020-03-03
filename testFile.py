import os
import time
import playsound
import random
import speech_recognition as sr
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang="en")
    fileName = "voice.mp3"
    tts.save(fileName)
    print(text)
    playsound.playsound(fileName)
    os.remove(fileName)

def getAudio() :
      r = sr.Recognizer()
      with sr.Microphone() as source:
          r.adjust_for_ambient_noise(source)
          print("Listening.......")
          audio = r.listen(source)
          said = ""
          try:
              said = r.recognize_google(audio)
              print(said)
          except Exception as e:
              print("Exception : ", e)
          return said

def generateRandomPlaylist(genre):
    availableSongs = os.listdir("Songs\\{}".format(genre))
    randomPlaylist = [availableSongs[x] for x in random.sample(range(1, len(availableSongs)), 7)]
    return randomPlaylist


def play():
    text  = "Hi, This is Stan. What's your name."
    speak(text)
    userName = getAudio()
    text = "Hi There, " + userName + ". These are list of genres you can select : "
    speak(text)
    genreList = os.listdir("Songs")
    for i in genreList:
        print(i, end = "\t")
    print()
    text = "For example if you want to choose Hip Hop, just say, Hip Hop"
    speak(text)
    print("Choose Genre...")
    genre = getAudio()
    text = "Great! Now let me tell you about the scoring. For each song played, you have to guess the name of the song correctly for 10 points, and if you get the name of the artist as well you get a bonus 10."
    speak(text)
    randomPlaylist = generateRandomPlaylist(genre)
    playerScore = 0
    # print(randomPlaylist[0])
    for i in range(len(randomPlaylist)):
        text = "Here is song number " + str(i)
        speak(text)
        playsound.playsound("Songs\\{}\\{}".format(genre, randomPlaylist[i]))
        print("Your Response..")
        response = getAudio()
        songName = randomPlaylist[i].split("-")[0];
        artistName = randomPlaylist[i].split("-")[1].split(",");

        response = response.split("by")
        if response[0] in songName or response[1] in artistName:
            text = "Correct! "
        else:
            text = "Wrong! "

        text += "The song is " + songName + " by " + artistName
        speak(text)

play()
