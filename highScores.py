import pygame
import sqlite3, csv
from sqlite3 import Error

class HighScores():

    def __init__(self, newScore, usersInitial):
        self.newScore = newScore
        self.usersInitial = usersInitial

        self.connectDatabase()

        connection = sqlite3.connect('HighScores.db')
        # create cursor object
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM highScores")

        idCheck = cursor.fetchall()
        # if there is nothing in the database, then id is 1
        if idCheck is None:
            idCount = 1
        # otherwise, increment id by 1
        else:
            idCount = 0
            for id in idCheck:
                idCount = int(id[0])
            idCount += 1

        self.scoresTuple = (idCount, self.usersInitial, self.newScore)
        self.scoresArray = []
        self.scoresArray.append(self.scoresTuple)

    def connectDatabase(self):
        # Start DB connection
        connection = sqlite3.connect('HighScores.db')
        # create cursor object
        cursor = connection.cursor()

        # determine if data tables have already been created
        exists = False
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='highScores' ''')

        # if there is a table, then the data has already been loaded
        if cursor.fetchone()[0] == 1:
            exists = True

        # Prep the database by cleaning it
        cursor.execute("CREATE TABLE IF NOT EXISTS highScores (id VARCHAR(64), userInitials VARCHAR(64), scores VARCHAR(64))")

        # commit databases
        connection.commit()

    def addScoreToDB(self):
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()

        # add user's initials and score to the database
        cursor.executemany("INSERT INTO highScores (id, userInitials, scores) VALUES (?, ?, ?);", self.scoresArray)
        connection.commit()

    def determineNewHighScore(self):
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()

        # sort database so that highest scores are at the top
        cursor.execute("SELECT * FROM highScores ORDER BY scores DESC")
        orderedData = cursor.fetchall()
        idCount = 1

        # update the database to be in order (with the highest score at the top)
        for data in orderedData:
            # get the user's initials
            value1 = data[1]
            # get the user's score
            value2 = data[2]
            # update the database with new id
            updateData = ('''UPDATE highScores SET userInitials = ?, scores = ? WHERE id = ?''')
            cursor.execute(updateData, (value1, value2, idCount))

            # increase the id count
            idCount += 1
            # commit to database
            connection.commit()

    def getTop5HighScores(self):
        # connect to the database
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()

        # get the scores from the database
        cursor.execute("SELECT * FROM highScores")
        scoresData = cursor.fetchall()

        # high score 1
        highScore1 = scoresData[0]
        # high score 2
        highScore2 = scoresData[1]
        # high score 3
        highScore3 = scoresData[2]
        # high score 4
        highScore4 = scoresData[3]
        # high score 5
        highScore5 = scoresData[4]

        return highScore1
