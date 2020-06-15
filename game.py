import os
import time
from playsound import playsound
import random
from string import capwords
import speech_recognition as sr
import pyttsx3
from player import Player
from song import Song


class Game():

    availableLang = ("English", "Hindi")
    availableNoOfQ = (3, 4, 5)
    availableGenres = tuple(os.listdir("Songs"))

    @staticmethod
    def speak(text):
        engine = pyttsx3.init()
        print(text)
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def getAudio():
        r = sr.Recognizer()
        said = ""

        with sr.Microphone() as source:
            print("Adjusting sound for Ambient Noise...")
            r.adjust_for_ambient_noise(source, duration=1)

            print("Listening...")
            audio = r.listen(source)

            try:
                print("Sending sound to google servers")
                said = r.recognize_google(audio)
                print(said)
            except:
                print("Sorry, Didn't get that one. Let's go again...")
                said = Game.getAudio()

            return said

    def __init__(self):
        pass

    def getLang(self):
        while True:
            text = "These are the list of LANGUAGES you can choose from"
            Game.speak(text)

            for lang in Game.availableLang:
                print(f"{Game.availableLang.index(lang)+1}. {lang}")

            print("Choose Your Language...")
            self.lang = Game.getAudio()

            if self.lang in Game.availableLang:
                break
            else:
                text = "Sorry, This Option is not available. Choose a valid option."
                Game.speak(text)

        return self.lang

    def getGenre(self):
        while True:
            text = "These are the list of GENRES you can choose from"
            Game.speak(text)

            for genre in Game.availableGenres:
                print(f"{Game.availableGenres.index(genre)+1}. {genre}")

            text = "For example if you want to choose Hip Hop just say, 'Hip Hop'"
            Game.speak(text)

            print("Choose Your Genre...")
            self.genre = Game.getAudio()

            if self.genre in Game.availableGenres:
                break
            else:
                text = "Sorry, This Option is not available. Choose a valid option."
                Game.speak(text)

        return self.genre

    def getNoOfQues(self):
        text = "Now, tell me how many questions do you want to answer.\nYou can say 3, 4 or 5"
        Game.speak(text)

        while True:
            print("Choose Number of Questions")
            self.noOfQuestions = Game.getAudio()
            if self.noOfQuestions.isdigit() and int(self.noOfQuestions) in Game.availableNoOfQ:
                self.noOfQuestions = int(self.noOfQuestions)
                break
            else:
                text = "Sorry, This option is not available. Choose a valid option."
                Game.speak(text)

        return self.noOfQuestions

    def generateRandomPlaylist(self):
        self.availableSongs = os.listdir(
            f"Songs\\{self.genre}\\{self.lang}\\")
        randNos = random.sample(
            range(len(self.availableSongs)), self.noOfQuestions)
        self.randomPlaylist = [
            self.availableSongs[x].replace(".mp3", "") for x in randNos]

    def start(self, player):

        QPosition = {
            '1': "first",
            '2': "second",
            '3': "third",
            '4': "fourth",
            '5': "fifth",
            '6': "sixth",
            '7': "seventh"
        }

        QPosition[self.noOfQuestions] = "last"

        self.generateRandomPlaylist()

        for i in range(len(self.randomPlaylist)):
            text = f"Here's the {QPosition[str(i+1)]} song."
            Game.speak(text)

            playsound(
                f"Songs\\{self.genre}\\{self.lang}\\{self.randomPlaylist[i]}.mp3")

            songName = self.randomPlaylist[i].split("-")[0]
            artistName = self.randomPlaylist[i].split("-")[1]
            currSong = Song(songName, artistName)

            print("Your Response: ")

            response = Game.getAudio()

            text = self.chkAns(currSong, response)

            player.updateScore(currSong.getPoints())

            text += f" The song is '{capwords(songName)}' by '{capwords(artistName)}'. You scored {currSong.getPoints()} points on this question. Your current score is '{player.getScore()}'"

            Game.speak(text)

    def chkAns(self, song, response):
        songResponse = ""
        artistResponse = ""

        response = response.split(" by ")

        if len(response) > 1:
            songResponse = response[0].lower()
            artistResponse = response[1].lower()
        else:
            songResponse = response[0].lower()
            artistResponse = response[0].lower()

        if songResponse in song.getName() and artistResponse in song.getArtist():
            song.setPoints(20)
            text = "Wow! You get the song as well as the artist correct. "
        elif songResponse in song.getName():
            song.setPoints(10)
            text = "Great! You get the song correct. "
        elif artistResponse in song.getArtist():
            song.setPoints(10)
            text = "Wonderful! You get the artist correct. "
        else:
            text = "Sorry!"

        return text
