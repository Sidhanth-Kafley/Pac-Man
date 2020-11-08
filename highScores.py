import pygame
import sqlite3, csv
from sqlite3 import Error

class HighScores():

    def __init__(self, newScore, usersInitial):
        self.newScore = newScore
        self.usersInitial = usersInitial
        self.scoresArray = []
        self.scoresArray.append(usersInitial)
        self.scoresArray.append(newScore)

    def connectDatabase(self):
        # Start DB connection
        connection = sqlite3.connect('HighScores.db')
        # create cursor object
        cursor = connection.cursor()

        # determine if data tables have already been created
        exists = False
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='scores' ''')

        # if there is a table, then the data has already been loaded
        if cursor.fetchone()[0] == 1:
            exists = True

        # Prep the database by cleaning it
        cursor.executescript("""DROP TABLE IF EXISTS "scores";
                                CREATE TABLE "highScores" (userInitials VARCHAR(64),
                                                           scores VARCHAR(64));""")
        # put array into database
        cursor.executemany("INSERT INTO scores (userInitials, scores) VALUES (?, ?);", self.scoresArray)

        # commit databases
        connection.commit()

