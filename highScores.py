import pygame
import sqlite3
from sqlite3 import Error


class HighScores():

    def __init__(self, newScore, usersInitial):
        self.newScore = newScore
        self.usersInitial = usersInitial

        # initially connect to the database and create table
        # (if it hasn't already been created)
        self.connectDatabase()

        try:
            # create connection to database
            connection = sqlite3.connect('HighScores.db')
            # create cursor object
            cursor = connection.cursor()

            # get all data from the database
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

            # add info to tuple, then array
            self.scoresTuple = (idCount, self.usersInitial, self.newScore)
            self.scoresArray = []
            self.scoresArray.append(self.scoresTuple)

            connection.close()

        except Error as error:
            print('Cannot connect to database. The following error occurred: ', error)

    def connectDatabase(self):
        try:
            # Start DB connection
            connection = sqlite3.connect('HighScores.db')
            # create cursor object
            cursor = connection.cursor()

            # create highScores table in the database
            cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='highScores' ''')

            # add the id, userInitials, and scores columns to the table
            cursor.execute("CREATE TABLE IF NOT EXISTS highScores (id VARCHAR(64), userInitials VARCHAR(64), scores VARCHAR(64))")

            # commit databases
            connection.commit()

            connection.close()

        except Error as error:
            print('Cannot connect to database. The following error occurred: ', error)

    def addScoreToDB(self):
        try:
            # create connection to database
            connection = sqlite3.connect('HighScores.db')
            cursor = connection.cursor()

            # add user's initials and score to the database
            cursor.executemany("INSERT INTO highScores (id, userInitials, scores) VALUES (?, ?, ?);", self.scoresArray)
            connection.commit()
            connection.close()

        except Error as error:
            print('Cannot connect to database. The following error occurred: ', error)

    def determineNewHighScore(self):
        try:
            # create connection to database
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
                connection.close()
        except Error as error:
            print('Cannot connect to database. The following error occurred: ', error)

    def getTop5HighScores(self):
        try:
            # connect to the database
            connection = sqlite3.connect('HighScores.db')
            cursor = connection.cursor()

            # dictionary of high scores
            top5HighScores = {}

            # get the scores from the database
            cursor.execute("SELECT * FROM highScores")
            scoresData = cursor.fetchall()

            # get how many rows there are in the database
            sizeOfArray = len(scoresData)
            # if there is nothing in the database, then say "no scores"
            if sizeOfArray == 0:
                top5HighScores["No Scores"] = 0

            elif sizeOfArray == 1:
                # high score 1
                highScore1 = scoresData[0]
                # add to dictionary
                top5HighScores["1"] = highScore1

            elif sizeOfArray == 2:
                # high score 1
                highScore1 = scoresData[0]
                # high score 2
                highScore2 = scoresData[1]
                # add to dictionary
                top5HighScores["1"] = highScore1
                top5HighScores["2"] = highScore2

            elif sizeOfArray == 3:
                # high score 1
                highScore1 = scoresData[0]
                # high score 2
                highScore2 = scoresData[1]
                # high score 3
                highScore3 = scoresData[2]

                # add to dictionary
                top5HighScores["1"] = highScore1
                top5HighScores["2"] = highScore2
                top5HighScores["3"] = highScore3

            elif sizeOfArray == 4:
                # high score 1
                highScore1 = scoresData[0]
                # high score 2
                highScore2 = scoresData[1]
                # high score 3
                highScore3 = scoresData[2]
                # high score 4
                highScore4 = scoresData[3]

                # add to dictionary
                top5HighScores["1"] = highScore1
                top5HighScores["2"] = highScore2
                top5HighScores["3"] = highScore3
                top5HighScores["4"] = highScore4

            else:
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

                # add to dictionary
                top5HighScores["1"] = highScore1
                top5HighScores["2"] = highScore2
                top5HighScores["3"] = highScore3
                top5HighScores["4"] = highScore4
                top5HighScores["5"] = highScore5

            return top5HighScores
        
        except Error as error:
            print('Cannot connect to database. The following error occurred: ', error)
