"""
This module
1. connects to MySQL server and creates a SMK database and table containing selected artwork information
2. imports string validated artwork information as JSON file to MySQL SMK table
3. tests import of artwork information from MySQL SMK database into the script.
  
Functions: string_valid(value)
"""
import pymysql 
import codecs
import json
from tabulate import tabulate
import sys


def JSONtoMySQL():

    try:
        """Connect to MySQL server and create SMK database."""
        host = input("Please enter MySQL host name: ")
        user = input("Please enter MySQL user: ")
        passwd = input("Please enter MySQL password: ")
        port = int(input("Please enter MySQL port: "))
        connection = pymysql.connect(host = host, user = user, passwd = passwd, port = port)
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS SMK1")
        cursor.execute("SHOW DATABASES")
        for db in cursor:
            print(db) 

    except Exception as e:
        print("Something went wrong with the database connection. Please try again.")
        sys.exit(1)

    try:
        """Connect to MySQL SMK1 database and create SMKentries table."""
        createtable = """CREATE TABLE IF NOT EXISTS SMKentries (entry INT AUTO_INCREMENT PRIMARY KEY, 
        artist VARCHAR(100), frontend_url VARCHAR(2048), id VARCHAR(50), production_date VARCHAR(20))"""
        connection = pymysql.connect(host = host, user = user, passwd = passwd, port = port, db = "SMK1")
        cursor = connection.cursor() 
        cursor.execute(createtable)
        cursor.execute("SHOW TABLES")
        for t in cursor:
            print(t)

    except Exception as e:
        print("Something went wrong with creating the table. Please try again.")


    # import JSON file containing artwork information
    with codecs.open("SMKselstr.json", "r") as f2in:
        data = json.load(f2in)


    def string_valid(value):
        """
        Convert non-strings to strings in UTF-8 format which are returned; if input is a string the string 
        is returned.
        """
        if value != None:
            if type(value) is not str:
                return str(value).encode('utf-8') 
            else:
                return value

    try: 
        """
        Take an interable object (here: list of dictionaries in JSON file) as argument, remove brackets 
        from artist name, get() get the value of the specified key which is used as argument for def string_
        valid(value), returned values are imported into MySQL database.
        """
        for i, item in enumerate(data):
            init_artist = string_valid(item.get("artist", None)) 
            artist = (init_artist.replace("[", "").replace("]", "").replace("\'", "")) 
            frontend_url = string_valid(item.get("frontend_url", None))
            id = string_valid(item.get("id", None))
            production_date = string_valid(item.get("production_date", None))

            cursor.execute("""INSERT INTO SMKentries (artist, frontend_url, id, production_date) 
                        VALUES (%s,%s,%s,%s)""", (artist, frontend_url, id, production_date))   
        connection.commit()

    except Exception as e:
        print(e)


    # test import of data from MySQL database 
    cursor.execute("SELECT artist, id, production_date FROM SMKentries")
    result = cursor.fetchall()
    print(tabulate(result, headers = ["artist", "id", "production_date"], tablefmt = "psql"))

    return connection