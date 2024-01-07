import json
import pyodbc

def createDB():
    # Load the configuration from 'appsettings.json'
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Access the default connection string
    server_connection = config['ConnectionStrings']['DefaultConnection']

    # Establish a connection to the database
    with pyodbc.connect(server_connection, autocommit=True) as sql_connection:
        # Create a new cursor
        with sql_connection.cursor() as cursor:
            # Check if the database exists and create it if it does not
            cursor.execute("""
                IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'GazaDb')
                CREATE DATABASE GazaDb;
            """)

def create_tables():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    server_connection = config['ConnectionStrings']['GazaDb']

    with pyodbc.connect(server_connection) as sql_connection:
        with sql_connection.cursor() as cursor:
            # Check if the 'feedbackIds' table exists and create it if not
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.feedbackIds') AND type in (N'U'))
                CREATE TABLE dbo.feedbackIds (
                    feedbackId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
                    feedbackString NVARCHAR(MAX) NOT NULL
                );
            """)
            # Check if the 'sentiment_Table' table exists and create it if not
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.sentiment_Table') AND type in (N'U'))
                CREATE TABLE dbo.sentiment_Table (
                    sentimentId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
                    parent_feedbackId INT NOT NULL,
                    date DATETIME NOT NULL,
                    comment NVARCHAR(MAX) NOT NULL,
                    sentimentScore FLOAT NOT NULL,
                    FOREIGN KEY (parent_feedbackId) REFERENCES dbo.feedbackIds(feedbackId)
                );
            """)
            # Commit the changes
            sql_connection.commit()
#returns feedbackID or none
def get_from_feedbackIds(feedback_string):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    server_connection = config['ConnectionStrings']['GazaDb']
    
    with pyodbc.connect(server_connection) as sql_connection:
        with sql_connection.cursor() as cursor:
            cursor.execute("""
                SELECT feedbackId
                FROM dbo.feedbackIds
                WHERE feedbackString = ?;
            """, feedback_string)
            result = cursor.fetchone()
            return result[0] if result else None

def insert_into_feedbackIds(feedback_string):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    server_connection = config['ConnectionStrings']['GazaDb']
    
    with pyodbc.connect(server_connection) as sql_connection:
        with sql_connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dbo.feedbackIds (feedbackString)
                VALUES (?);
            """, feedback_string)
            sql_connection.commit()

def insert_into_sentiments(date, sentiment_score, comment, parent_feedback_id):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    server_connection = config['ConnectionStrings']['GazaDb']
    
    with pyodbc.connect(server_connection) as sql_connection:
        with sql_connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dbo.sentiment_Table (date, sentimentScore, comment, parent_feedbackId)
                VALUES (?, ?, ?, ?);
            """, date, sentiment_score, comment, parent_feedback_id)
            sql_connection.commit()

#returns list of tuples (comment,date,score)
def get_all_sentiments():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    server_connection = config['ConnectionStrings']['GazaDb']
    
    with pyodbc.connect(server_connection) as sql_connection:
        with sql_connection.cursor() as cursor:
            cursor.execute("""
                SELECT comment, date, sentimentScore
                FROM dbo.sentiment_Table;
            """)
            results = cursor.fetchall()
            return [(row.comment, row.date, row.sentimentScore) for row in results]

