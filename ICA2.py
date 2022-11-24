#!/bin/bash/python3

#These are all of the modules I will need
import os
import shutil
import requests
import pandas as pd

#The program begins by asking the user to input the taxonid and protien name
#It will now allow the user to input a blank space in the txid as this will
#cause problems for writing the file named with this txid
#All of these input error checks have a similar structure, using a while looping
#That will continue to output the error message and prompt the user to renter
#The input until the input is acceptable
taxonid = input("Enter desired taxonid:") #txid4890
while 'txid' not in taxonid:
    print("taxonid must begin with 'txid'")
    taxonid = input("Enter desired taxonid:")
while ' ' in taxonid:
    print("You can not enter blank spaces in the taxonid")
    taxonid = input("Enter desired taxonid:")
    while 'txid' not in taxonid:
        print("taxonid must begin with 'txid'")
        taxonid = input("Enter desired taxonid:")

#Asking the user to add a protein family name
proteinfam = input("Enter desired protein name:") #pyruvate dehydrogenase

#This is making a label with "_" in place of spaces if they appear
proteinlabel = proteinfam
if ' ' in proteinfam:
    proteinlabel = proteinfam.replace(" ","_")

#Now I am using the variable taxon as the label for any files generted from this search
#I honestly should have used a clearer varaible name, but I realized at the very end that I forgot
#To include protein name in the file labels, and had to add this after writing all of the code
#And did not want to risk cuasing errors my incorrectly changing or missing changing
#the variable name somewhere down below
taxon = taxonid+"_"+proteinlabel

#I am then generating my esearch command that will be stored in a varaible
#It is an esearch wihin the protein database
#Specifying the taxonid and protein name based on the user input
#I specified not partial to remove any entires that are protein fragments
#I then used efectch to grab the sequence data for each of these protein entries
#Within efetch I also specified to output the data into a file in msf format for the next step
#This output file is named based on the taxonid


#I am now asking the user if they would like to include partial sequences
#Error check for if yes and no are input
#This simply changes the presence of 'NOT partial' in the esearch command
partial = input("Would you like to include partial sequences? (yes/no):")
while partial.upper() != 'YES' and partial.upper() != 'NO':
    print("Answer not yes or no value")
    partial = input("Would you like to include partial sequences? (yes/no):")

#The next two blocks of if statements are identical except for presence of "NOT partial"
#Then perform an esearch using the input txid and protein
#I first grep the "count" data from the esearch and save that to a file called count.txt
#Then open that file and extarct the integer of counts and display that to the user
#If the search returned no results I tell the user and exit the program
#If there is at least one result I ask the user if they would like to proceed
#And error check their response appropriately, exiting if they say no
#If they say yes I continue to the efetch command
#I am suing the -db protein to specify a protein database, taxon input as organism,
#The protein input as Protein Name, then efetching with fasta format specified
#And sending the results to a file named using the input txid
if partial.upper() == 'NO':
    ecountcommand = "esearch -db protein -query '"+taxonid+"[Organism:exp] AND "+proteinfam+"[Protein Name] NOT Partial' | grep 'Count' > count.txt"
    os.system(ecountcommand)
    count = open("count.txt").read()
    count = count.replace('  <Count>','').replace('</Count>\n','')
    print("Your search returned "+count+" results")
    if int(count) == 0:
        print("your search returned no results. Now exiting")
        exit()
    keep = input("Would you like to continue with your analysis? (yes/no):")
    while keep.upper() != 'YES' and keep.upper() != 'NO':
        print("Answer not yes or no value")
        keep = input("Would you like to continue with your analysis? (yes/no):")
        if keep.upper() == 'NO':
            exit()
    searchcommand = "esearch -db protein -query '"+taxonid+"[Organism:exp] AND "+proteinfam+"[Protein Name] NOT Partial' | efetch -format fasta > "+taxon+".fa"
    print("Now pulling NCBI entries based on the followng search command:")
    print(searchcommand)
    #Now using os.system to run the searchcommand in bash
    os.system(searchcommand)

#All the same as above except for partial sequences will be included here
if partial.upper() == 'YES':
    ecountcommand = "esearch -db protein -query '"+taxonid+"[Organism:exp] AND "+proteinfam+"[Protein Name]' | grep 'Count' > count.txt"
    os.system(ecountcommand)
    count = open("count.txt").read()
    count = count.replace('  <Count>','').replace('</Count>\n','')
    print("Your search returned "+count+" results")
    if int(count) == 0:
        print("your search returned no results. Now exiting")
        exit()
    keep = input("Would you like to continue with your analysis? (yes/no):")
    while keep.upper() != 'YES' and keep.upper() != 'NO':
        print("Answer not yes or no value")
        keep = input("Would you like to continue with your analysis? (yes/no):")
        if keep.upper() == 'NO':
            exit()
    searchcommand = "esearch -db protein -query '"+taxonid+"[Organism:exp] AND "+proteinfam+"[Protein Name]' | efetch -format fasta > "+taxon+".fa"
    print("Now pulling NCBI entries based on the followng search command:")
    print(searchcommand)
    #Now using os.system to run the searchcommand in bash
    os.system(searchcommand)

#This is just another check to make sure that the esearch and efetch pipe worked
#If it has not worked then the contnets of the fasta file will be empty
#So this opens the fasta file
with open("{}.fa".format(taxon)) as file:
        contents = file.read()

#And then checks to make sure that the contents are not empty. If they are it tells
#The user and exits
if contents == '':
    print("Search has failed")
    print("Exiting program, please try new search")
    exit()



#Now I am importing and calling the sample organization function
#This will take all of the results from the fasta file
#And put them into a dataframe, which gets returned into the seqdf variable
#The function also makes the headers.txt and seqs.txt files which get used later
from sampleorgfunc import *
seqdf = sampleorg(taxon)

#This is making sure that there are more than one sequence from the results
#Setting the oneseq variable to 'no' by default
oneseq = 'no'
#If there is only one row in the seqdf then the value of oneseq gets changed to 'yes'
#This gets used as a trigger later on to avoid doing the clustalo command, which will crash
#If provided a single sequence as input,
#I thereby use it to only allow the user to do the motif analysis
if seqdf.shape[0] == 1:
    oneseq = 'yes'
    #I am asking the user if they want to continue given that they only got one result
    #Error check the input is yes or no
    #If they say no then I exit the program
    print("Your results only returned one sequence")
    print("Alignment analyses can not be performed, but you can still idenitfy motifs")
    oneseqcontinue = input("Would you like to conitnue? (yes/no):")
    while oneseqcontinue.upper() != "YES" and continue1.upper() != "NO":
        print("Answer not yes or no value")
        oneseqcontinue = input("Would you like to conitnue? (yes/no):")
    if oneseqcontinue.upper() == 'NO':
        print("You have chosen to exit the program")
        exit()
    #If they say yes then I send the program into a special circumstance
    #Where oneseq is yes BEFORE any filtering has been applied
    #This is because if the user filters down to one sample you should still allow them
    #To refilter and do other analyses on a different filtered subset
    #But if their initial search only returned one result there's no point in filtering
    #So this calls the analysis function and specifies to only do motif analyses then exit
    if oneseqcontinue.upper() == 'YES':
        first = 'yes'
        from whichanalyses import *
        whichanalysisfunc(taxon,oneseq,first)



#Now we tell the user the number of genera and species
#Output for the user to see how many results they got
#This is just from pulling the lengths of the value counts
#for the genus and species columns
entries = str(seqdf.shape)
entries = entries.split(",")[0]
entries = entries[1:]
genuscount = str(len(seqdf['Genus'].value_counts()))
speccount = str(len(seqdf['Species'].value_counts()))
print("Your query returned "+entries+" results")
print("This includes "+genuscount+" unique genera")
print("And "+speccount+" unique species")


#Now ask the user if they would like to perform analyses on all of these results
#Or if they would like to filter
#Doing an error check to make sure they input yes or no
print("You can perform analyses on all of these results or instead on a smaller subset")
continue1 = input("Would you like to perform analyses on all results? (yes/no):")
while continue1.upper() != "YES" and continue1.upper() != "NO":
    print("Answer not yes or no value")
    continue1 = input("Would you like to perform analyses on all results? (yes/no):")

#If they say that they would like to analyze this full list of results
#Then we initiate the whichanalysis function
#Which will go through and ask them which analyses to perform
if continue1.upper() == 'YES':
    from whichanalyses import *
    whichanalysisfunc(taxon,oneseq)

#If they do not want to perform analysis on the full set of results
#I then ask if they would like to filter for a subset of results
#If they say no then we are done here and it exists
continue2 = input("Would you like to perform analysis on a subset of the results? (yes/no):")
while continue2.upper() != "YES" and continue2.upper() != "NO":
    print("Answer not yes or no value")
    continue2 = input("Would you like to perform analysis on a subset of the results? (yes/no):")
if continue2.upper() == "NO":
    print("It sounds like there's nothing more to be done then. Now exiting")
    exit()
#If they say yes then we let them know they different ways that they can filter
#Being length, genus, and species
#Then also print out the number of genera, species, and length statistics for their results
#Since length is the only numeric value in seqdf the .describe() function simply displays
#The statistics about the lengths
if continue2.upper() == "YES":
    print("As a reminder,")
    print("Your query returned "+entries+" results")
    print("This includes "+genuscount+" unique genera")
    print("And "+speccount+" unique species")
    print("You can sort the samples based on genus, species, genus+species, or sequence length")
    print("Taxon filter can be by genera, species, or both")
    print("length filter can specify minimum, maximun, or both")
    print("The sequence length statistics for your results are provided below:")
    print(seqdf.describe())

#This will ask them what subset they want
#It will ask them if they want to filter by length or taxa or both
#Then based on their input will trim the dataframe to their desired sequences
#And then takes the trimmed dataframe and makes a new fasta file from it
#Then this new filtered fatsa file gets put into the whichanalyses function
#Which will go through and do the analyses the user desired on the subset they desire
from filterfunc import *
filterfunc(taxon, seqdf)

#Then this will ask them if they would like to do another filtered analysis
#Asking if they want to do more analyses, error checking, then if no it exits
again = input("Would you like to perform more analyses? (yes/no):")
while again.upper() != "YES" and again.upper() != "NO":
    print("Answer not yes or no value")
    again = input("Would you like to perform more analyses? (yes/no):")
if again.upper() == "NO":
    print("I suppose that you would like to exit the program then. Now exiting")
    exit()
#Now if the user says yes it will go through the filterfunc again,
#Which, as described above will filter the dataframe as desired then
#As the user which analyses they want performed
#And within this while loop the user gets asked again if they would like to do more analysis
#They can say yes which will keep them in the loop, but once they say no it will exit the loop
#And the program will terminate
while again.upper() == 'YES':
    filterfunc(taxon, seqdf)
    again = input("Would you like to perform more analyses? (yes/no):")
    #doing an error check within the loop so that a non-yes/no answer doesn't exit it
    while again.upper() != "YES" and again.upper() != "NO":
        print("Answer not yes or no value")
        again = input("Would you like to perform more analyses? (yes/no):")
if again.upper() == "NO":
    print("I suppose that you would like to exit the program then. Now exiting")
    exit()

