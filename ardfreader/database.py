# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>


import sqlite3
from ardfreader.pixel import Pixel


class ARDFDatabase:

    CREATE_TABLE_PIXEL = """
        CREATE TABLE Pixels (
            Line int NOT NULL,
            Pixel int NOT NULL,
            Step int NOT NULL,
            Ch1 double NOT NULL,
            Ch2 double NOT NULL,
            Ch3 double NOT NULL,
            CONSTRAINT PK_Pixel PRIMARY KEY (Line,Pixel,Step)
        )
    """

    def __init__(self, file="ardf.db"):
        self.file = file
        self.conn = None
        self.cursor = None

    def connect(self):
        self.cursor = None

        try:
            self.conn = sqlite3.connect(self.file)
            self.cursor = self.conn.cursor()
            print(f"Starting SQLite {sqlite3.version} with db: {self.file}")
            
            self.cursor.execute(self.CREATE_TABLE_PIXEL)
            print("Pixels table created\n")
        except sqlite3.Error as e:
            print(e)

    #def put_pixel(self, pix: Pixel):
     #   pass

    def put_pixel(self, pix: Pixel):
        x = pix.x
        y = pix.y

        for i in range(0, len(pix.channels[0])):
            ch1 = pix.channels[0][i]
            ch2 = pix.channels[1][i]
            ch3 = pix.channels[2][i]

            self.cursor.execute(f'INSERT INTO Pixels VALUES ({x}, {y}, {i}, {ch1}, {ch2}, {ch3})')

    def close(self):
        if self.cursor:
            print(f'Database {self.file} closing...\n')
            self.conn.commit()
            self.conn.close()
