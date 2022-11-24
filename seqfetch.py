#!/bin/python3

#Alright let's get this thing started!
#I will be callinig bash code for the esearch so that requires os
import os
#Asking the user to input the taxonid and protien name
taxon = input("Enter desired taxonid:")
proteinfam = input("Enter desired protein name:")
#I am then generating my esearch command that will be stored in a varaible
#It is an esearch wihin the protein database
#Specifying the taxonid and protein name based on the user input
#I specified not partial to remove any entires that are protein fragments
#I then used efectch to grab the sequence data for each of these protein entries
#Within efetch I also specified to output the data into a file in msf format for the next step
#This output file is named based on the taxonid
searchcommand = "esearch -db protein -query '"+taxon+"[Organism:exp] AND "+proteinfam+"[Protein Name] NOT Partial' | efetch -format fasta > "+taxon+".prot.fa"
print(searchcommand)
#Now using os.system to run the searchcommand in bash
os.system(searchcommand)
