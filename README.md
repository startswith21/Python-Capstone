# Capstone-Project
## "Artwork Gallery"

### Description

This interactive project enables the user to manage artwork information stored in a MySQL database and to view and manipulate artwork images. Data on 2000 artworks are retrieved from the National Gallery of Denmark (Statens Museum for Kunst; https://www.smk.dk/en/) API and the information are imported from the JSON file into a MySQL database. Because a url for the artwork image and image download is not yet available for all artworks, artworks of two artists have been selected for non-destructive user operations. The PC and software used for the project were: macOS Monterey Version 12.5.1 & Ventura Version 13.4, Python 3.9.6, MySQL 8.0.32 and Visual Studio Code 1.59.0.

### Requirements

**Python standard library modules:**
- codecs
- JSON
- re
- sys
- urllib
- venv (recommended)
- webbrowser
 
  


**External packages:**
- Pillow 10.0.1
- PyMySQL 1.1.0
- requests 2.31.0
- tabulate 0.9.0  
  

  

**Modules:**  
<br>1. SMKAPItoJSONstr.py:<br> 
This module fetches information on 2000 artworks from the Statens Museum for Kunst/SMK (National Gallery of Denmark) via the SMK API as a JSON file.

<br>2. JSONtoMySQL.py:<br> 
This module connects to the MySQL server and creates a SMK database and table containing selected artwork information and imports string validated artwork information as JSON file to MySQL SMK table.

<br>3. SMKinteraction.py:<br> 
This module interacts with the MySQL database containing information on artworks of the National Gallery of Denmark (SMK) to retrieve data of two artists. It gives the user options to change artwork entries, and view and manipulate images of their artworks based on user input.

<br>4. interface.py:<br> 
This module imports all modules and functionalities required for the project.


### Set up
- Install Python (https://www.python.org/downloads/)
- Install MySQL (https://dev.mysql.com/downloads/installer/)
- Recommended to create a virtual environment (https://docs.python.org/3/library/venv.html)
- Install external packages preferably in the virtual environment; for example by using the requirements.txt file and running the command: pip install -r requirements.txt in the -terminal
- Save modules SMKAPItoJSONstr.py, JSONtoMySQL.py, SMKinteraction.py and interface.py


### Usage
- Start MySQL server
- Activate virtual environment if created (https://docs.python.org/3/library/venv.html)
- Run module interface.py preferably in a virtual environment
- Follow user input prompts in interface.py and select options
