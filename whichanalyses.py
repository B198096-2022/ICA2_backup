#!/bin/python3

#All of the modules I need to import
#Importing all of the functiosn from the other scripts in the pipeline
import os
from bashfuncs import *
from motiffunc import *
from motiflist import *

#The function takes the taxon label as an argument,
# which is the label used to specify which files to work with
#It also has the argument oneseq, which specifies if the
#Incoming files have a single sequece,
#and first which specifies if the file is the full search results or not
def whichanalysisfunc(taxon, oneseq = 'no',first='no'):
    #If there are multiple sequences in the file then everything is fine
    #And all analysis tools will work fine and the analysis continues
    if oneseq == 'no':
        #Begin by clustering the sequences since this is needed for most of the analysis
        clusterfunc(taxon)
        #Now we ask if the user wants to do all the analyses or a select few
        analysisall = input("Would you like to perform all analyses on the data? (yes/no):")
        #Error check yes/no
        while analysisall.upper() != "YES" and analysisall.upper() != "NO":
            print("Answer not yes or no value")
            analysisall = input("Would you like to perform all analyses on the data? (yes/no):")
        #If they say yes then call all of the analysis functions
        if analysisall.upper() == "YES":
            plotconfunc(taxon)
            aligninfofunc(taxon)
            prettyplotfunc(taxon)
            #Generating seperate motif files for all of the entries
            motiffunc(taxon)
            #Pulling the
            motiflist(taxon)
        if analysisall.upper() == "NO":
            #If they say no then the program asks one at a time if they
            #Want to do each of the analyses individually
            #Does an error check on the yes/no Answer
            #And if yes calls the function and executes it
            analysis1 = input("Would you like to produce a conservation plot of the sequences? (yes/no):")
            while analysis1.upper() != "YES" and analysis1.upper() != "NO":
                print("Answer not yes or no value")
                analysis1 = input("Would you like to produce a conservation plot of the sequences? (yes/no):")
            if analysis1.upper() == "YES":
                plotconfunc(taxon)
            analysis4 = input("Would you like to view alignment information on the sequences? (yes/no):")
            while analysis4.upper() != "YES" and analysis1.upper() != "NO":
                print("Answer not yes or no value")
                analysis4 = input("Would you like to view alignment information on the sequences? (yes/no):")
            if analysis4.upper() == "YES":
                aligninfofunc(taxon)
            analysis2 = input("Would you like to see a pretty plot of alignments for the sequences? (yes/no):")
            while analysis2.upper() != "YES" and analysis2.upper() != "NO":
                print("Answer not yes or no value")
                analysis2 = input("Would you like to see a pretty plot of alignments for the sequences? (yes/no):")
            if analysis2.upper() == "YES":
                prettyplotfunc(taxon)
            analysis3 = input("Would you like to scan for PROSITE motifs in the sequences? (yes/no):")
            while analysis3.upper() != "YES" and analysis3.upper() != "NO":
                print("Answer not yes or no value")
                analysis3 = input("Would you like to scan for PROSITE motifs in the sequences? (yes/no):")
            if analysis3.upper() == "YES":
                #Generating seperate motif files for all of the entries
                motiffunc(taxon)
                #Pulling the
                motiflist(taxon)
    if oneseq == 'yes' and first == 'no':
        #If the user has filtered down to a single sequence
        #(specified by oneseq being yes, and first being no, meaning the user has applied a filter)
        #Under these conditions the program has alreadt told the user
        #That they have filtered to a single sequence
        #And now asks if they woudl like to still do motif analysis
        stillmotif = input("Would you still like to perform motif analysis on your single selected sequence? (yes/no):")
        #Error check on input
        while stillmotif.upper() != "YES" and stillmotif.upper() != "NO":
            print("Answer not yes or no value")
            stillmotif = input("Would you still like to perform motif analysis on your single selected sequence? (yes/no):")
        #If they would like to still do motif analysis then the motif functions are called
        #If they say no then this function ends and goes back to the full pipeline
        #Where the user is asked if they want to do another filter
        if stillmotif.upper() == "YES":
            #Generating seperate motif files for all of the entries
            motiffunc(taxon)
            #Pulling the
            motiflist(taxon)
    if oneseq == 'yes' and first == 'yes':
        #This is the worst case scenario for this function
        #The original search only returned one sequence
        #So only motif analysis can be performed and no furtehr filtering is possible
        #The user was already asked if they wanted to still do motif analysis
        #So they motif functions are called and the program exits
        motiffunc(taxon)
        #Pulling the
        motiflist(taxon)
        print("Motif analysis is complete and is the only analysis available for one sequence")
        print("now exiting program")
        exit()











#

