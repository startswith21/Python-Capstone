"""
This module
1. fetches information on 2000 artworks from the Statens Museum for Kunst/SMK (National Gallery of Denmark)
via the SMK API as a JSON file
2. selects artwork id, name of artist, production date and image url for each artwork from the JSON file
and stores the list of dictionaries as a JSON file and 
3. converts all values of the dictionaries to string type and save them as a JSON file for import into a 
MySQL database.
"""
import requests 
import json
import codecs


def APItoJSON():

    try:
        """Requesting a response from the SMK server/API using the HTTP library requests."""
        response = requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&offset=0&rows=2000&lang=en")
    except requests.exceptions.HTTPError as http:
        print ("Http error:",http)
    except requests.exceptions.ConnectionError as conn:
        print ("Connection error:",conn)
    except requests.exceptions.Timeout as time:
        print ("Timeout error:",time)
    except requests.exceptions.RequestException as other:
        print ("Another error",other)


    # store artwork information provided by the SMK as a list of dictionaries as JSON file
    response = response.json()
    with open("SMK.json", "w") as f1out:
        json.dump(response, f1out)

    with open("SMK.json", "r") as f1in:
        SMKdict = json.load(f1in)


    # select name of artist, id, image url and production date for each artwork from JSON file and store as 
    # list of dictionaries
    SMKselkeys = []
    for dictionary in SMKdict["items"]:
        SMKselkeys.append({"id":dictionary["id"], "artist":dictionary["artist"], "frontend_url":dictionary["frontend_url"],
        "production_date":dictionary["production_date"][0]["period"]})  
    print(SMKselkeys) 


    # write artwork information to JSON file
    with codecs.open("SMKsel.json", "w", "utf8") as f2out:
        f2out.write(json.dumps(SMKselkeys, sort_keys = True, ensure_ascii=False))

    with codecs.open("SMKsel.json", "r") as f2in:
        data = json.load(f2in)
    print(data)
    

    # convert values in dictionaries to strings (keys are always strings)
    for i in data:
        for key, value in i.items():
            i.update({key: str(value)})


    # write string converted items of list of dictionaries to JSON file
    with codecs.open("SMKselstr.json", "w", "utf8") as f2out:
        f2out.write(json.dumps(data, sort_keys = True, ensure_ascii=False))

    with codecs.open("SMKselstr.json", "r") as f2in:
        data = json.load(f2in)
    print(data)  

    