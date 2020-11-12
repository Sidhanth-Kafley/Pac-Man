import pygame
import sqlite3, csv
from sqlite3 import Error

class HighScores():

    def __init__(self, newScore, usersInitial):
        self.newScore = newScore
        self.usersInitial = usersInitial
        self.scoresTuple = (self.usersInitial, self.newScore)
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
        cursor.execute("CREATE TABLE IF NOT EXISTS highScores (userInitials VARCHAR(64), scores VARCHAR(64))")
        #cursor.executescript("""DROP TABLE IF EXISTS "scores";
         #                       CREATE TABLE "scores" (userInitials VARCHAR(64),
                                                         #  scores VARCHAR(64));""")
        # put array into database
        #cursor.execute("INSERT INTO scores (userInitials, scores) VALUES ()")
        #cursor.executemany("INSERT INTO scores (userInitials, scores) VALUES (?, ?);", self.scoresArray)

        # commit databases
        connection.commit()

    def addScoreToDB(self):
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()

        # add user's initials and score to the database
        cursor.executemany("INSERT INTO highScores (userInitials, scores) VALUES (?, ?);", self.scoresArray)
        connection.commit()

    def determineNewHighScore(self):
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()

        # get the scores from the database
        cursor.execute("SELECT * FROM highScores")
        scoresData = cursor.fetchall()

        highScore = 0
        for score in scoresData:
            # if the score is greater than the current high score,
            # then it is the new high score
            convertedScore = int(score[1])
            if convertedScore > highScore:
                highScore = convertedScore
            print(score[1])

        # sort database so that highest scores are at the top
        cursor.execute("SELECT * FROM highScores ORDER BY scores DESC")
        orderedData = cursor.fetchall()
        updateData = ('''UPDATE highScores SET userInitials = ?, score = ? WHERE id = ?''')
        idCount = 1
        #for score in orderedData:
        #    cursor.execute(updateData, (score[0], score[1], idCount))
        #    idCount += 1
        connection.commit()

