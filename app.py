import os
from final_script import *
import time
from flask import Flask, render_template, request
import csv
import datetime
import urllib.request
import codecs

def readData():
    now = datetime.datetime.now()
    arr = []
    url = 'http://maps.waterloo.ca/OpenData/events.csv'
    ftpstream = urllib.request.urlopen(url)
    csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
    next(csvfile)
    for line in csvfile:
        category = line[5].replace('<p>', "").replace('</p>',"").replace("&quot","")
        description = line[7].replace('<p>', "").replace('</p>',"").replace("&quot","")
        name = line[13].replace('<p>', "").replace('</p>',"").replace("&quot","")
        date = line[2]
        date = date[:10]
        dateArr = date.split("/")
        eventMonth = int(dateArr[0])
        eventDay = int(dateArr[1])
        eventYear = int(dateArr[2])
    
        if (eventYear>= now.year and eventMonth>=now.month and eventDay>=now.day): 
            arr.append({"Name": name, "EndDate": line[2], "Category": category, "Details": description})
            
    return(arr)
    
#Filler Data
data = readData();

for var in data: 
    if var['Details'] =="": 
        continue
    str = var['Details']
    mini_dic = eventPersonality(str)
    result = (max(mini_dic.keys(), key=(lambda k: mini_dic[k])))
    var["Personality"] = result

print(data)

app = Flask(__name__)
#app.conf.broker_url = 'redis://localhost:6379/0'
@app.route('/')
def hello():
    return render_template ("index.html")
    
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=="POST": 
        personality = main_func(request.form["twittername"])
        return render_template ("results.html", data=data, personality=personality)

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

    