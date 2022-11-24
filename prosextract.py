#!/bin/python3
import requests
import os
import shutil

#Make the directory for the prosite files
os.mkdir("./prositedir")

#The url where these files are stored
dat_url = "https://ftp.expasy.org/databases/prosite/prosite.dat"
doc_url = "https://ftp.expasy.org/databases/prosite/prosite.doc"
#File1 is technically the website associated with the url
#But the contents of these url is just the contents of the document we want
#Then we just open a file called what we want and write in the contnets of the file1/2
file1 = requests.get(dat_url)
open("prosite.dat", "wb").write(file1.content)

file2 = requests.get(doc_url)
open("prosite.doc", "wb").write(file2.content)
#Then this is moving the files into the directory
shutil.move("./prosite.dat", "./prositedir/prosite.dat")
shutil.move("./prosite.doc", "./prositedir/prosite.doc")


#Then this runs the prosextract
os.system("prosextract -prositedir prositedir")
