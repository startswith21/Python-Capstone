""" 
This module imports all modules and functionalities required for the project. First, the SMKAPItoJSONstr
module saves artwork data from the National Gallery of Denmark (SMK) as JSON file. Second, the module 
JSONtoMySQL connects to the MySQL server, creates a SMK database and stores data from the JSON file in 
the database. Third, the module SMKinteraction interacts with the MySQL database and allows the user to
manage and view artwork entries.
"""

import pymysql
from SMKAPItoJSONstr import APItoJSON
from SMKinteraction import Menu, User
from JSONtoMySQL import JSONtoMySQL

# calling the modules
APItoJSON()
connection = JSONtoMySQL()
user_name = input("Please enter your name: ")
user_menu = Menu(User(user_name), connection)   
