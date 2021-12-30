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

#just for logging
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
f.write("\nLogging-time = "+ current_time)

#connect to a random URL
random.seed()
random_url = str(random.randint(1,26))
website = urllib2.urlopen("https://esahubble.org/images/archive/wallpapers/page/" + random_url +"/")

#read html code
html = website.read()

#note that the reg-Expression for numbers start with 2 and is at least 4 digits long [2-9]{4}
#that way we can ensure that no pictures with a low resolution are downloaded
links = re.findall("title: '.*',[\r\n].*width: [2-9]{4},[\r\n].*height: [2-9]{4},[\r\n].*src: .*[\r\n].*url: '\/[a-zA-Z0-9]*\/[a-zA-Z0-9]*", html)

link = random.choice(links)

#we will change the link-string but first we extract the title:
title = link.split(",")[0].split("'")[1]
title = re.sub(r"[^0-9A-Za-z]+","-", title)
title = title +".jpg"

link = link.split(",")[4].split("/")[2]

if not os.path.exists('./hubble-pictures'):
    os.makedirs('./hubble-pictures')

dir = "./hubble-pictures/"

#if there are any pictures in the folder, delete them first
for item in os.listdir(dir):
    if item.endswith(".jpg"):
        path = os.path.join(dir,item)
        os.remove(path)

url = "https://cdn.spacetelescope.org/archives/images/wallpaper1/" + link + ".jpg"
path = os.path.dirname(os.path.abspath(__file__))+"/hubble-pictures/" + title
urllib.urlretrieve(url, path)

result = os.system("gsettings set org.gnome.desktop.background picture-uri 'file://" + path +"'")
if result == 0:
    #just for logging
    f.write("\nEverything Ok")
else:
    f.write("\nSomething went wrong trying to execute gsettings set org.gnome.desktop.background picture-uri 'file://" + dir + title +"'")
