#!/bin/bash/python3

#I can't import within a function
#So I think I just need to import everything at the beginning of the big script?

#Improvements, if directory already exists then skip this
#Ask user if they want to continue, if no just type exit()
#Do you want partial sequences Yes/No
#Check any user input (is genera in list?)
#Do a while loop to ask would you like to do more analysis?
#Put my sample sorting stuff in a script
#Run those scripts while the answer is yes
#taxon = 'txid4890'
#pyruvate dehydrogenase

#This needs imported scripts:
#bashfuncs
#whichanalyses
#Sampleorgfunc
#filterfunc

#These are all of the modules I will need
import os
import shutil
import requests
import pandas as pd
#Asking the user to input the taxonid and protien name
taxon = input("Enter desired taxonid:") #txid4890
proteinfam = input("Enter desired protein name:") #pyruvate dehydrogenase
#I am then generating my esearch command that will be stored in a varaible
#It is an esearch wihin the protein database
#Specifying the taxonid and protein name based on the user input
#I specified not partial to remove any entires that are protein fragments
#I then used efectch to grab the sequence data for each of these protein entries
#Within efetch I also specified to output the data into a file in msf format for the next step
#This output file is named based on the taxonid
partial = input("Would you like to include partial sequences? (yes/no):")
while partial.upper() != 'YES' and partial.upper() != 'NO':
    print("Answer not yes or no value")
    partial = input("Would you like to include partial sequences? (yes/no):")
if partial.upper() == 'NO':
    searchcommand = "esearch -db protein -query '"+taxon+"[Organism:exp] AND "+proteinfam+"[Protein Name] NOT Partial' | efetch -format fasta > "+taxon+".fa"
    print("Now pulling NCBI entries based on the followng search command:")
    print(searchcommand)
    #Now using os.system to run the searchcommand in bash
    os.system(searchcommand)
if partial.upper() == 'YES':
    searchcommand = "esearch -db protein -query '"+taxon+"[Organism:exp] AND "+proteinfam+"[Protein Name]' | efetch -format fasta > "+taxon+".fa"
    print("Now pulling NCBI entries based on the followng search command:")
    print(searchcommand)
    #Now using os.system to run the searchcommand in bash
    os.system(searchcommand)

with open("{}.fa".format(taxon)) as file:
        contents = file.read()



if contents == '':
    print("Search has failed")
    print("Cause of failure is presented above")
    print("Exiting program, please try new search")
    exit()


#This defines three of the analysis functions
#Which clusters the sequences with clustalo and puts them into an msf file
#Then uses this to make a conservation plotconcon
#And finally generates a summary of the alignemnt
#I then run this function with the input taxon

def clusterfunc(taxon):
    import os
    clustercommand = "clustalo -i "+taxon+".fa -threads=16 -t protein --outfmt=msf -o "+taxon+"align.msf"
    os.system(clustercommand)

def plotconfunc(taxon):
    #This makes the conservation plot
    import os
    plotconcommand = "plotcon -sformat msf "+taxon+"align.msf -winsize 4 -graph cps -goutfile "+taxon+"_plotcon"
    os.system(plotconcommand)

def aligninfofunc(taxon):
    #This generates a file with the alignment info for each protein
    import os
    infocommand = "infoalign "+taxon+"align.msf -outfile "+taxon+"_aligninfo.txt -only -heading -name -seqlength -idcount -simcount -diffcount -change"
    os.system(infocommand)

def prettyplotfunc(taxon):
    #pretty plot shows the alignments visually
    import os
    prettycommand = "prettyplot "+taxon+"align.msf -sformat1 msf -docolour -graph cps -goutfile "+taxon+"_prettyplot"
    os.system(prettycommand)

#running the cluster function is case we need it for later
#clusterfunc(taxon)

#This just extracts the prosite database
#import extract


#Making the headers and sequences file
#Then putting them into a dictionary

#Using grep to make a file of fa headers for all of the samples by pulling lines with ">"
#Then using awk to pull every line that doesn't have ">", which will be the sequences
#And inserting a "_" in the place of the fa header line to be used to split later
headercommand = "grep '>' "+taxon+".fa > headers.txt"
seqscommand = "awk '/^>/ { print '_'; next; }; {print; }' "+taxon+".fa > seqs.txt"
os.system(headercommand)
os.system(seqscommand)
#Opening the headers.txt file
with open("headers.txt") as file:
    headers = file.read()
#Opening the seqs.txt file
with open("seqs.txt") as file:
    seqs = file.read()

#Now using the headers and seqs files I am splitting them into lists
#I need to split up the seqs with split, then rejoin, putting a space between the seqs,
#Then split again based on the space
#this is not very elegant but it solved other problems I was having and it works
#so I'm sticking with it
seqlist1 = seqs.split("\n\n")
seqstr = " \n".join(seqlist1)
seqlist = seqstr.split(" ")
headerlist = headers.split("\n")
#Now this just scans and ensures that there are no blank spaces
#At the beginning or end of the lists that could offset the two lists
if seqlist[0] == '':
    seqlist = seqlist[1:] #This DOES cut off first empty space

if seqlist[-1] == '':
    seqlist = seqlist[0:-1] #This does nothing

if headerlist[0] == '':
    headerlist = headerlist[1:] #This does nothing

if headerlist[-1] == '':
    headerlist = headerlist[0:-1] #This cuts off the final empty space

#Now I am making a dictionary with all of the sequences. Defining the length of the dict
dictlen = len(seqlist)

#Now I can making a dictionary, and for all numbers in the range of dictlen
#I am looping through and adding the headerlist enrty for that position as the key and
#seqlist entry for that position position as the value
seqdict = {}
seqdict[headerlist[0]] = seqlist[0]
for i in range(dictlen):
    seqdict[headerlist[i]] = seqlist[i]


#Telling the user how many results the search returned




#Now we make a dfto organize the samples
from sampleorgfunc import *
seqdf = sampleorg(taxon)

oneseq = 'no'
if seqdf.shape[0] == 1:
    oneseq = 'yes'
    print("Your results only returned one sequence")
    print("Alignment analyses can not be performed, but you can still idenitfy motifs")
    oneseqcontinue = input("Would you like to conitnue? (yes/no):")
    while oneseqcontinue.upper() != "YES" and continue1.upper() != "NO":
        print("Answer not yes or no value")
        oneseqcontinue = input("Would you like to conitnue? (yes/no):")

if oneseqcontinue.upper() == 'NO':
    print("You have chosen to exit the program")
    exit()


if oneseqcontinue.upper() == 'YES':
    first = 'yes'
    from whichanalyses import *
    whichanalysisfunc(taxon,oneseq,first)



#Now we tell the user the number of genera and species
#Output for the user to see how many results they got
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
continue1 = input("Would you like to perform analyses on all results? (yes/no):")
while continue1.upper() != "YES" and continue1.upper() != "NO":
    print("Answer not yes or no value")
    continue1 = input("Would you like to continue analysis on all results? (yes/no):")

#If they say that they would like to analyze this full list of results
#Then we initiate the whichanalysis function
#Which will go through and ask them which analyses to perform
if continue1.upper() == 'YES':
    from whichanalyses import *
    whichanalysisfunc(taxon,oneseq)

#If they do not
continue2 = input("Would you like to perform analysis on a subset of the results? (yes/no):")
while continue2.upper() != "YES" and continue2.upper() != "NO":
    print("Answer not yes or no value")
    continue2 = input("Would you like to perform analysis on a subset of the results? (yes/no):")
if continue2.upper() == "NO":
    print("It sounds like there's nothing more to be done then. Now exiting")
    exit()
if continue2.upper() == "YES":
    print("You can sort the samples based on genus, species, genus+species, or sequence length")
    print("Taxon filter can be by genera, species, or both")
    print("length filter can specify minimum, maximun, or both")
    print("The sequence length statistics for your results are provided below:")
    print(seqdf.describe())

#This will ask them what subset they want and then it calls the whichanalysis within it
#So it will go through and do the analyses the user desired on the subset they desire
from filterfunc import *
filterfunc(taxon, seqdf)

#Then this will ask them if they would like to do another filtered analysis
again = input("Would you like to perform more analyses? (yes/no):")
while again.upper() != "YES" and again.upper() != "NO":
    print("Answer not yes or no value")
    again = input("Would you like to perform more analyses? (yes/no):")
if again.upper() == "NO":
    print("I suppose that you would like to exit the program then. Now exiting")
    exit()
while again.upper() == 'YES':
    filterfunc(taxon, seqdf)
    again = input("Would you like to perform more analyses? (yes/no):")
    while again.upper() != "YES" and again.upper() != "NO":
        print("Answer not yes or no value")
        again = input("Would you like to perform more analyses? (yes/no):")
if again.upper() == "NO":
    print("I suppose that you would like to exit the program then. Now exiting")
