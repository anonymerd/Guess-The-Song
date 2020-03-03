import os
import time
import playsound
import random
import speech_recognition as sr
from gtts import gTTS
import mysql.connector
import datetime
 
db=mysql.connector.connect(host="localhost", user="root", passwd="1234", database="stan")
cursor=db.cursor(buffered=True)

def speak(text):
    tts = gTTS(text=text, lang="en")
    fileName = "voice.mp3"
    tts.save(fileName)
    print(text)
    playsound.playsound(fileName)
    os.remove(fileName)


def change_lastplayed(userName):
    currentDT = datetime.datetime.now()
    current_DT=currentDT.strftime("%Y-%m-%d %H:%M:%S")
    update_datetime="update user_info set last_played ='{}' where name='{}';".format(current_DT,userName)
    cursor.execute(update_datetime)
    db.commit()


def player(userName):
   

    user_retrieval="select * from user_info where name= '{}';".format(userName)
    cursor.execute(user_retrieval)
    x=cursor.fetchone()    
    if x==None:
        text="ah! a new player. Welcome to the game {}".format(userName)
        speak(text)
    if x !=None:
        text="glad to have you back {}.".format(userName)
        speak(text)
        text="wanna know your highscore!"
        speak(text)
        said = getAudio()

        if said == 'yes' or said == 'Yes':
            get_highscore="select high_score from user_info where name = '{}';".format(userName)
            cursor.execute(get_highscore)
            x=cursor.fetchone()
            speak(x[0])

        else:
            text="Sorry to bother mate. contnue with the game! hope you enjoy the game."
            speak(text)    
        change_lastplayed(userName)    
    db.commit()
    return x

def database(userName,genre,playerScore):
    current_DT=change_lastplayed(userName)
   
    new_user="insert into user_info values('{}','{}','{}','{}');".format(userName,genre,current_DT,playerScore)
    cursor.execute(new_user)
    change_lastplayed(userName)
    db.commit() 

def update_highscore(userName,playerScore):
    get_highscore="select high_score from user_info where name='{}'".format(userName)
    cursor.execute(get_highscore)
    x=cursor.fetchone()
    if(int(playerScore)>int(x[0])):
        playerScore=str(playerScore)
        update_highscore="update user_info set high_score ='{}' where name='{}';".format(playerScore,userName)
        cursor.execute(update_highscore)
        db.commit()
    else:
        return    
    
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
              print(said)
          except Exception as e:
              print("Sorry, didn't get that one. Let's go again")
              said = getAudio()

          return said

def generateRandomPlaylist(genre):
    availableSongs = os.listdir("Songs\\{}".format(genre))
    randomPlaylist = [availableSongs[x] for x in random.sample(range(0, len(availableSongs)), 3)]
    return randomPlaylist


def play():
    text  = "Hi, This is Stan. Let's start by knowing your name."
    speak(text)
    print("Tell us your name.")
    userName = getAudio()
    x=player(userName)
    text="these are the genres you can choose to play:"
    speak(text)
    genreList = os.listdir("Songs")
    for i in genreList:
        print(i.capitalize(), end = " \t ")
    print()

    text = "For example if you want to choose Hip Hop, just say Hip Hop"
    speak(text)

    while True:
        print("Choose your Genre")
        genre = getAudio()
        if genre in genreList:
            if x==None:
                database(userName,genre,'0')
            break
        else:
            text = "Sorry, This option is not available. Choose a valid option."
            speak(text)

    text = "Great! Now let me tell you about the scoring system. For each song played, you have to guess the name of the song correctly for 10 points, and if you get the name of the artist as well, you get a bonus 10."
    speak(text)

    # genre = "hip hop"

    randomPlaylist = generateRandomPlaylist(genre)
    playerScore = 0

    position = {
        '1' : "first",
        '2' : "second",
        '3' : "last",
        '4' : "fourth",
        '5' : "fifth",
        '6' : "sixth",
        '7' : "last"
    }
    # print(randomPlaylist[0])

    for i in range(len(randomPlaylist)):
        text = "Here is {} song.".format(position[str(i+1)])
        speak(text)

        playsound.playsound("Songs\\{}\\{}".format(genre, randomPlaylist[i]))
        songName = randomPlaylist[i].split("-")[0];
        artistName = randomPlaylist[i].split("-")[1].replace(".mp3", "").split(",");

        print("Your Response : ")

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

        print(response)

        if songResponse in songName and artistResponse in artistName:
            playerScore += 20
            text = "Wow! You get the song as well as the artist correct."
        elif songResponse in songName:
            playerScore += 10
            text = "Great! You get the song correct."
        elif artistResponse in artistName:
            playerScore += 10
            text = "Wonderful! You get the artist correct."

        text += "The song is '" + songName.capitalize() + "' by '" + artistName[0].capitalize() + "'. Your current score is '" + str(playerScore) + "'"
        speak(text)
       

    update_highscore(userName,playerScore)
    text = "Thank you for playing."
    speak(text)


# playsound.playsound("Songs\\hip hop\\.mp3")
play()
