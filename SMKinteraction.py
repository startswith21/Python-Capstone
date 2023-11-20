""" 
This module interacts with the MySQL database containing information on artworks of the National Gallery 
of Denmark (SMK) to retrieve data of two artists. It gives the user options to change artwork entries, 
and view and manipulate images of their artworks based on user input.
  
Use module SMKAPItoJSONstr.py to get the data from the SMK API 
Use module JSONtoMySQL.py to store SMK JSON data in MySQL database
Use module interface.py to import this module, SMKAPItoJSONstr.py and JSONtoMySQL.py

Classes: Artist, Artwork, User, Menu 
""" 

import sys
import webbrowser
import pymysql
import re
import requests
import urllib.request 
from PIL import Image, ImageEnhance
import os


class Artist():
  """ 
  A class representing an artist. 

  Attributes:
    name: name of artist
    artworks_dictionary: stores all artworks of an artist with Menu __init__

  Methods: 
    __init__        : Initializes an Artist object and its artworks
    add_artworks    : Adds new artwork to artworks_dictionary
    delete_artworks : Deletes artwork of the artist from list of artworks
    display artworks: Prints all artworks of the artist to the user
  """

  def __init__(self, name):
    """Initializes an Artist object and its artworks."""
    self.name = name
    self.artworks_dictionary = {}


  def add_artworks(self, new_artworkslist):
    """Adds new artwork to list of artworks."""
    for i in range(len(new_artworkslist)):
      self.artworks_dictionary[len(self.artworks_dictionary) + i] = new_artworkslist[i]
      
        
  def delete_artwork(self, artwork_name):  
    """Deletes artwork of the artist from list of artworks."""
    print(f"You have deleted the artwork entry: {artwork_name}")
    
    for key in self.artworks_dictionary:
      if self.artworks_dictionary[key].artwork_name == artwork_name:
          del self.artworks_dictionary[key]
          break
    
    newvalue_list = list(self.artworks_dictionary.values())

    self.artworks_dictionary = {}
    for i in range(len(newvalue_list)):
        self.artworks_dictionary[i] = newvalue_list[i]

    self.display_artworks()


  def display_artworks(self):
    """Prints all artworks of the artist to the user."""
    print(f"These are the artworks by {self.name}:")  
    for key in self.artworks_dictionary.keys():
      print("{}: {}".format(key, self.artworks_dictionary[key].artwork_name))


class Artwork():
  """ 
  A class representing an artwork. 

  Attributes:
    artist: name of artist
    artwork_name: name of artwork
    id_number: id_number unique for each artwork
    year: year of production
    url: url for image of artwork

  Methods: 
    __init__        : Initializes an Artwork object
    update_entry    : Updates data of an attribute of an artwork 
    delete_entry    : Calls delete_artwork from artist that this artwork belongs to
    display         : Prints artwork attribute data to the user
    view_image      : Opens the url for the image of the artwork in a browser
    manipulate_entry: Downloads the image of an artwork, opens the original image, changes the contrast 
                      value based on user input and opens the modified image
  """

  def __init__(self, artist, artwork_name, id_number, year, url = "no url entered"):
    """Initializes an Artwork object."""
    self.artist = artist
    self.artwork_name = artwork_name
    self.id_number = id_number
    self.year = year
    self.url = url 


  def update_entry(self): 
    """Updates data of an attribute of an artwork."""
    print()
    print(f"The artwork you want to update is '{self.artwork_name}'")
    
    update_options = ["artist", "artwork_name", "id_number", "year"]

    def update_input():
        """Lets user select the attribute to be updated."""
        while True:
            update_choice = input("What information would you like to update? Please type 'artist',\
                                  'artwork_name', 'id_number' or 'year': ") 
            if update_choice in update_options:
                return update_choice
            elif not update_choice:
                print("Your input was empty")
                continue
            else:
                print("Your choice is not available")
                continue
    
    choice = update_input()

    def validate_update(category):
        """Validates correct user input for the attribute 'year'."""
        while True:
            category_input = input(f"Please enter new {category}: ")
            if category_input != "":
                if choice != "year":
                    return category_input  
                if choice == "year":
                    if category_input.isdigit() and len(str(category_input)) == 4:
                        return category_input
                    elif category_input.isdigit() == False:
                        year_input = re.search(r'[a-zA-Z]+', category_input)
                        if year_input:
                            print("Please enter numbers only")
                    else:
                        print("Please enter the year in four digit format")
    
    update_info = validate_update(choice)

    if choice == "artist":
        self.artist.name = update_info
    if choice == "artwork_name":
        self.artwork_name = update_info
    if choice == "id_number":
        self.id_number = update_info
    if choice == "year":
        self.year = update_info
    
    print(                               
      f"Artwork information has been updated to: Artist = {self.artist.name}, \n"
      f" artwork = {self.artwork_name}, ID = {self.id_number}, year = {self.year}"
      )
    

  def delete_entry(self):
    """Calls delete_artwork from artist that this artwork belongs to."""
    self.artist.delete_artwork(self.artwork_name) 


  def display(self):
    """Prints artwork attribute data to the user."""
    print("")
    print(
      f"Artwork information: \nArtist: {self.artist.name} -- Name of artwork: {self.artwork_name} \n"
      f" -- ID: {self.id_number} -- Year: {self.year}"
    )  


  def view_image(self):
    """Opens the url for the image of the artwork in a browser."""
    webbrowser.open(self.url)


  def manipulate_entry(self):  
    """
    Downloads the image of an artwork, opens the original image, changes the contrast value based
    on user input and opens the modified image. 
    """
    dl_urldict = {
        "Ursula Christiansen - Artwork 1": "https://iip-thumb.smk.dk/iiif/jp2/0k225f76j_kms8918.tif.jp2/full/!1024,/0/default.jpg",
         "Ursula Christiansen - Artwork 2": "https://iip-thumb.smk.dk/iiif/jp2/jd4731021_kms8920.tif.jp2/full/!1024,/0/default.jpg", 
         "Ursula Christiansen - Artwork 3": "https://open.smk.dk/artwork/image/kms8919",
         "Ulrik Heltoft - Artwork 1": "https://iip-thumb.smk.dk/iiif/jp2/4x51hp371_kks2019_96.tif.jp2/full/!1024,/0/default.jpg"}
    
    print(self.artwork_name)
    
    dl_url = dl_urldict.get(self.artwork_name)
    
    if dl_url == None:    
      print(f'Sorry, this method is not available for the image you selected. Available images are: {dl_urldict.keys()}')
    else:
      print("The image that will open now is the orginal image.")
    
      try:
        urllib.request.urlretrieve(dl_url, 
        "SMKimage.jpg")
        print("The image was downloaded into: ", os.getcwd())
      except Exception as e:
        print("An error occurred retrieving the image.", e)
        
      image = Image.open("SMKimage.jpg")
      image.show()

    

      def contrast():
        """Changes the contrast value of an image of an artwork and opens the modified image."""
        while True:
            user_val = input("Please enter a contrast value between -255 and 255: ")
            if user_val == "":
                print("Your input was empty. Please enter a number.")
                continue
            elif (user_val.strip('-')).isdecimal():
                user_val = int(user_val)
                if -255 <= user_val <= 255: 
                    print(f"The contrast value of the image will be changed to: {user_val}")
                    return user_val
                else:
                    print("Your number was out of range. Please enter a number between -255 and 255.")
                    continue
            else:
                print("Please enter a number using decimals only.")
      
      contr_user = contrast()

      mod_contr = ImageEnhance.Contrast(image)
      newimage = mod_contr.enhance(contr_user)
      print("The image that will now open is the modified image.")
      newimage.show()
    

class User(object):
  """"
  A class representing a user. 

  Attributes:
    name: name of user
    favorite_artists: list of two Artist objects
   
  Methods: 
    __init__ : Initializes a User and Artist object
  """

  def __init__(self, name):
    """Initializes a User and Artist object."""
    self.name = name
    self.favorite_artists = ['Ulrik Heltoft', 'Ursula Christiansen']
    print(
    f"\nWelcome {self.name} to the Danish Art Gallery. \n" 
   f"You can manage the art collection and view and modify artwork images. \n"
   f"Please enter the information to connect to the MySQL server:"
)

 

class Menu():
  """  
  A class representing a menu. 

  Attributes:
    user: user as defined in User class 
    current_artwork: artwork selected by the user

  Methods: 
    __init__         : Defining an Artist and Artwork object and options for the user
    edit_artwork_menu: Calls an Artwork method to view or make changes to artwork
    search_by_artist : Lets user select artist and artwork, displays artworks of the selected 
                       artist and calls edit_artwork_menu method
    main_menu        : Lets the user select main menu options by calling search_by_artist or create_artwork 
                       method
    create_artwork   : Creates a new artwork entry, adds artwork to list and displays current artworks
                       to user 
  
  """
  def __init__(self, user, connection):
      """Defining an Artist and Artwork object and options for the user."""
      
      cursor = connection.cursor()
 
      cursor.execute("SELECT frontend_url, id, production_date FROM SMKentries WHERE \
                     artist = 'Heltoft, Ulrik'")
      HU_artwork = cursor.fetchall()
      u_heltoft_artworklist = [] 
      u_heltoft = Artist("Ulrik Heltoft") 
      index = 0 

      for entry in HU_artwork:
        index += 1
        url = entry[0]  
        artwork_name = "Ulrik Heltoft - Artwork " + str(index)
        id = entry[1]
        production_date = entry[2]
        new_artwork = Artwork(u_heltoft, artwork_name, id, production_date, url) 
        u_heltoft_artworklist.append(new_artwork)
        u_heltoft.add_artworks([new_artwork])


      cursor.execute("SELECT frontend_url, id, production_date FROM SMKentries WHERE \
                     artist = 'Ursula Reuter Christiansen'")
      URC_artwork = cursor.fetchall()
      christiansen_artworklist = [] 
      u_christiansen = Artist("Ursula Christiansen") 
      index = 0 

      for entry in URC_artwork:
        index += 1
        url = entry[0]   
        artwork_name = "Ursula Christiansen - Artwork " + str(index)
        id = entry[1]
        production_date = entry[2]
        new_artwork = Artwork(u_christiansen, artwork_name, id, production_date, url) 
        christiansen_artworklist.append(new_artwork)
        u_christiansen.add_artworks([new_artwork])

      self.artworks = {u_heltoft: u_heltoft_artworklist, u_christiansen: christiansen_artworklist}
      self.artistlist = [u_heltoft, u_christiansen]

      cursor.close()  

      self.user = user
      self.edit_options = {
      1: "update artwork",
      2: "delete artwork",
      3: "view artwork",
      4: "manipulate artwork",
      5: "go back to main menu",
      }
      self.main_options = {
      1: "search artwork by artist name",
      2: "create new artwork entry",
      3: "exit program",
      } 
      self.main_menu()

      

  def edit_artwork_menu(self, current_artwork):
    """Calls an Artwork method to view or make changes to artwork."""
    for i in range(1):
      print('\n------------------Edit Artwork Menu-----------------------\n')
      menu_options = list(self.edit_options.values())
      menu_keys = list(self.edit_options.keys())
      for i in range(len(menu_options)):
        print(menu_keys[i], menu_options[i])

      try:
        print()
        choice = int(input("Please select an option and enter the number: "))
        if choice == 1:
            current_artwork.update_entry()
        
        elif choice == 2:
            print(f"Do you want to delete the selected artwork: {current_artwork.artwork_name}") 
            del_choice = input("Please enter 'yes' or 'no': ").capitalize()
            if del_choice == "Yes":
                if "Ulrik" in current_artwork.artwork_name:
                    print("You don't have permission to delete this artwork.")
                if "Ursula" in current_artwork.artwork_name:
                    current_artwork.delete_entry()           
            elif del_choice == "No":
                print("The artwork has not been deleted.")
            else:
                print("Please enter correct choice 'yes' or 'no'")

        elif choice == 3:
            current_artwork.view_image()

        elif choice == 4:
            current_artwork.manipulate_entry()

        elif choice == 5:
            print('You are being directed back to the main menu')
            break

        else:
            print("Please enter correct choice: 1, 2, 3, 4 or 5")

      except ValueError:
          print("Something went wrong. Please enter a valid number.")


  def search_by_artist(self):
    """
    Lets user select artist and artwork, displays artworks of the selected artist and calls
    edit_artwork_menu method.
    """
    print()
    print(
      "Please type artist name. For example, choose from your list of favorites."
    )
    print('Your current favorites are:')
    print(*self.user.favorite_artists, sep = " & ")
    print()
    search_input = input(
        "Which artist\'s works would you like to view? Please enter name: "
            )

    artwork_artists = self.artworks.keys() 
    found_match = False

    for artist in artwork_artists:           
      if search_input == artist.name:
        found_match = True
        artist.display_artworks()  
        
        try:
            input_index = int(      
            input(
            'Please enter artwork index number to view artwork and access the "Edit Artwork Menu": '
            ))
            current_artwork = artist.artworks_dictionary[input_index]
            current_artwork.display()    

            self.edit_artwork_menu(current_artwork)
        
        except ValueError:
            print("Something went wrong. Please enter a valid number.")  
        except KeyError:                     
            print("The index you entered does not exist. Please enter the correct index.") 


    
    if found_match == False:
      print(
        "Sorry, the artist you entered is not in the database. You are being directed to the main menu."
      )    

  def main_menu(self):
    """Lets the user select main menu options by calling search_by_artist or create_artwork method."""
    while (True):

      print('\n------------------Main Menu-----------------------\n')
      menu_options = list(self.main_options.values())
      menu_keys = list(self.main_options.keys())
      for i in range(len(menu_options)):
        print(menu_keys[i], menu_options[i])

      try: 
        print()
        choice = int(
            input('Please select an option and enter the number: '))
        if choice == 1:
            self.search_by_artist()

        elif choice == 2:  
            self.create_artwork()

        elif choice == 3:
            print("goodbye")
            sys.exit(0)

        else:
            print("Please enter correct choice: 1, 2 or 3")
    
      except ValueError:
        print("Something went wrong. Please enter a valid number")


  def create_artwork(self):
    """Creates a new artwork entry based on user input, adds artwork to list and displays current artworks
     to user.
     """
    print()
    print("You can now create a new artwork entry")
    artist_input = "1"
    while artist_input.isalpha() == False:
        artist_input = input("Please enter name of artist: ").capitalize()
        if artist_input.strip() == "":
            print("Your input was empty. Please enter name of artist.")

        elif artist_input.isalpha() == False:
          print("Please enter valid name using letters only")

    is_match = False
    matched_artist = ""
    for artistobject in self.artistlist:
      if artist_input == artistobject.name:
        matched_artist = artistobject
        is_match = True
        break
        
    if is_match == False:
      matched_artist = Artist(artist_input)
      self.artistlist.append(matched_artist)

    while True:
        artwork_name = input("Please enter name of artwork: ")   
        if artwork_name.strip() == "":
            print("Your input was empty. Please enter name of artwork.")
        if artwork_name.strip() != "":
            break

    while True:
        id_number = input("Please enter ID number: ")                
        if id_number.strip() == "":
            print("Your input was empty. Please enter ID number.")
        if id_number.strip() != "":
            break
    
    while True:                                                      
        year_production = input("Please enter year of production in four digit year format: ")
        if year_production.strip() == "":
            print("Your input was empty. Please enter year of production.")
        if year_production.isnumeric() == False:
            print("Something went wrong. Please enter a number to indicate the year of production.")
        if year_production.isnumeric() == True and len(str(year_production)) != 4:
          print("Please enter year in four digit format")
        if len(str(year_production)) == 4:
            break

    created_artwork = [Artwork(matched_artist, artwork_name, id_number, year_production)]
    self.artworks[matched_artist] = created_artwork 
    matched_artist.add_artworks(created_artwork)
    print("New entry has been created")
    matched_artist.display_artworks()  



