'''
 *  tracker.py    Azam Shoaib     Virginia Tech       Last update: 12/7/2022
 *  (Required)
 *  In the tracker.py we extract the visit count numbers from a sqlite3 database
 *  The main domains we are extracting from right now is Apple Music, Spotify and Netflix
 *  After extraction adn correct formatting we can use this file in Budget.py to update the
    aws database so we can use the values in the graph for subscription tracking
'''
import os
import sqlite3
import json


printGood = False # global variable to help validate if a string should be printed

'''
The following convert function will take the given data tuple and convert it to a string.
Index 0 of the tuple will contain the url which we are going to disregard in the function.
Index 1 of the tuple will contain the domain name of the url, which we will use to help filter
    out what we want to look at.
Index 2 of the tuple will contain the count the url was visited.
We will also be changing a global variable to check if we can print the string because it is valid.
'''
def convertTuple(tup):
    global printGood
    st = '' # initialize an empty string
    first = True
    second = True
    valid = False
    for item in tup:
        if first:
            first = False
            continue
        elif second and (item == "netflix" or item == "music.apple" or item == "open.spotify"):
            st = st + str(item) + " "
            second = False
            valid = True
            printGood = True
        elif second == False and valid:
            st = st + str(item) + " "
            first = True
            second = True
            valid = False
        else:
            printGood = False
            continue
    return st
 
 
# updates the new2.db file with updated
# needs to be adjusted for different os system
os.chdir("/Users/azamshoaib/Library/Safari")
os.system("sqlite3 History.db '.recover' | sqlite3 new2.db")

# would need to be adjusted for different os and different browser engines
con = sqlite3.connect("/Users/azamshoaib/Library/Safari/new2.db")
cur = con.cursor()

if os.path.exists("subscription.txt") == False:
    os.chdir("/Users/azamshoaib/Desktop")
    file = open("subscription.txt","w")
    file.write("Subscriptions:\n")
    file.close()

file = open("subscription.txt","a")

keywords_url = ["watch", "songs","playlist", "albums", "album", "station", "genre"]
thisdict = {}
for row0 in cur.execute("SELECT url, domain_expansion, visit_count FROM history_items"):
    if row0[1] == "netflix" or row0[1] == "music.apple" or row0[1] == "open.spotify":
        for key in keywords_url:
            url_str = str(row0[0])
            if (url_str.find(key) > -1):
                # print(url_str.find(key)) # will keep for testing purpose
                line = convertTuple(row0)
                if printGood == True:
#                    map_res = map(row0[1], row0[2])
                    if row0[1] in thisdict.keys():
                        val = thisdict[row0[1]]
                        update_val = val + row0[2]
                        thisdict[row0[1]] = update_val
                    else:
                        thisdict.update({row0[1]: row0[2]})
                    print(thisdict)

file.write(json.dumps(thisdict))
                    #file.write(line + "\n")
file.close()
# Be sure to close the connection
con.close()
