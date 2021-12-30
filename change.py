#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import os
import subprocess
import sys
import urllib
import urllib2
import re
from datetime import datetime

f= open("./error.log", "a")

#nur fürs loggen: schreibe die Zeit
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
f.write("\nLogging-time = "+ current_time)

#connect to a random URL
random.seed()
random_url = str(random.randint(1,26))
website = urllib2.urlopen("https://esahubble.org/images/archive/wallpapers/page/" + random_url +"/")

#read html code
html = website.read()

#use re.findall to get all the links
#beachte dass der Regex für Zahlen erst bei 2 beginnt [2-9] und mindestens vierstellig sein muss
#dadurch wird sichergestellt, dass keine der Bilder verwendet werden, die sehr niedrig aufgelöst sind
#vielleicht könnte man, das auch noch höher einstellen
#
#wenn du die regex besser verstehen möchtest dann unkommentiere folgende Zeile
#print (html)
#und schau dir das Array "images" an
links = re.findall("title: '.*',[\r\n].*width: [2-9]{4},[\r\n].*height: [2-9]{4},[\r\n].*src: .*[\r\n].*url: '\/[a-zA-Z0-9]*\/[a-zA-Z0-9]*", html)

link = random.choice(links)

#we will change the link-string but first we extract the title:
title = link.split(",")[0].split("'")[1]
#beachte, dass re.replace keine regex akzeptiert -> deswegen re.sub
title = re.sub(r"[^0-9A-Za-z]+","-", title)
title = title +".jpg"

#now get only the relevant part of the link string
link = link.split(",")[4].split("/")[2]

if not os.path.exists('./hubble-pictures'):
    os.makedirs('./hubble-pictures')

dir = "./hubble-pictures/"   # Bilderverzeichnis

#falls jpgs im Ordner sind, dann löschen
for item in os.listdir(dir):
    if item.endswith(".jpg"):
        path = os.path.join(dir,item)
        os.remove(path)

url = "https://cdn.spacetelescope.org/archives/images/wallpaper1/" + link + ".jpg"

path = os.path.dirname(os.path.abspath(__file__))+"/hubble-pictures/" + title

#urlretrieve wird benutzt um ein Bild herunterzuladen und unter dem angegeben Pfad zu speichern
urllib.urlretrieve(url, path)

#os.system führt den eigentlichen Befehl zum wechseln des Bildes aufgelöst
#zum loggen speichern wir das resultat von os.system
#falls es keine Probleme gibt, liefert os.system 0 zurück
#command = "'file://" + dir + title +"'"
#subprocess.call(["gsettings","set","org.gnome.desktop.background", "picture-uri", command ],stdout = open( 'error.log', 'w') )

result = os.system("gsettings set org.gnome.desktop.background picture-uri 'file://" + path +"'")  # ab Ubuntu 11.04
if result == 0:
    f.write("\nEverything Ok")
else:
    f.write("\nSomething went wrong trying to execute gsettings set org.gnome.desktop.background picture-uri 'file://" + dir + title +"'")
