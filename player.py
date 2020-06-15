class Player():

    '''
    This is Player Class which represents the user which is playing the game.
    '''

    def __init__(self, name, lang, genre, noOfQues):
        self.name = name
        self.lang = lang
        self.genre = genre
        self.noOfQues = noOfQues
        self.score = 0

    def getScore(self):
        return self.score

    def updateScore(self, currScore):
        self.score += currScore
