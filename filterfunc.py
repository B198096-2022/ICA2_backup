#!/bin/python3

#This function is what I spent most of my time making and fixing
#It is serving as my main "additional" feature, consideirng tha the
#pretty plot analysis is not very intensive
#It allows the user to perform the analyses on any subset of the results
#Based on any desired sequence length filters, genus, species, or all of the above

#I need to import the whichanalysis function from whichanalyses.property
#Also need to import os
from whichanalyses import *
import os


#The arguments of the function are the taxon variable, which has the txid and protein name
#This gets used to make file labels
#It also takes in the seqdf dataframe created by sampleorgfunc in the pipeline
#This dataframe gets used as the starting point data frame that gets subsequently filteres
def filterfunc(taxon, seqdf):  #filterfunc('txid4890')
    #Reset the dataframe as the full dataframe
    seqdfnew = seqdf
    #Then specify what seqdf is
    seqdf = seqdf
    #This is setting all of the default values
    #They are used if the user chooses to not perform the given filter
    #without these defaults the program fails since the variables are not definted
    #but if they are needed they get overwritted by the desired content
    minlen=0
    maxlen='all'
    oneseq = 'no'
    lengthfilter='no'
    lengthcriteria = 'none'
    #Now the program asks the user if they would like to filter by length
    #And does and error check to make sure answer is yes/no
    lengthfilter = input("would you like to filter by sequence length? (yes/no):")
    while lengthfilter.upper() != 'YES' and lengthfilter.upper() != 'NO':
        print("Answer not yes or no value")
        lengthfilter = input("would you like to filter by sequence length? (yes/no):")
    #If yes, the program asks if they want to filter by min, max, or BOTH
    #And does an error check to make sure their input is one of those options
    if lengthfilter.upper() == "YES":
        lengthcriteria = input("would you like to filter by sequence length maximum, minimum, or both?:")
        while lengthcriteria.upper() != 'MAXIMUM' and lengthcriteria.upper() != 'MINIMUM' and lengthcriteria.upper() != 'BOTH':
            print("Answer not one of the options")
            lengthcriteria = input("would you like to filter by sequence length maximum, minimum, or both?")
        #If they answer maximum then it will run the maxfunc
        #Which filters the dataframe based on the input maximum cutoff
        if lengthcriteria.upper() == "MAXIMUM":
            seqdfnew,maxlen,oneseq = maxfunc(seqdfnew)
        #If they answer minumum then it will run the minfunc
        #Which filters the dataframe based on the input minimum cutoff
        if lengthcriteria.upper() == "MINIMUM":
            seqdfnew,minlen,oneseq = minfunc(seqdfnew)
        #If they answer both then it will run both maxfunc and minfunc
        #maxfunc will run first, produce a filtered dataframe called seqdfnew
        #minfunc will then take in this new dataframe and filter it further
        if lengthcriteria.upper() == "BOTH":
            seqdfnew,maxlen,oneseq = maxfunc(seqdfnew)
            seqdfnew,minlen,oneseq = minfunc(seqdfnew)
    #The maxfunc and minfunc check the number of remaining sequences
    #If the number of remaining sequences is only 1 then the value of oneseq is 'yes'
    #If there is only one sequence then there is no point in filtering by Taxa
    #So the program goes straight into the onlylengthfunc which will make a label
    #and aks the user if they want to continue with only one sample
    if oneseq == 'yes':
        onlylengthfunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen,taxon,oneseq)
    #If there are more than one sequences then the program continues
    #It asks the user if they want to filter gy genera, species, both, or None
    #Then error checks to make sure their answer is one of the options
    if oneseq == 'no':
        taxfilter = input("Would you like to filter by genera, species, both, or none?:")
        while taxfilter.upper() != 'GENERA' and taxfilter.upper() != 'SPECIES' and taxfilter.upper() != 'BOTH' and taxfilter.upper() != 'NONE':
            print("Answer not one of options: genera, species, both, or none")
            taxfilter = input("Would you like to filter by genera, species, both, or none?:")
        #If they say filter by genera then it runs the generafunc
        if taxfilter.upper() == 'GENERA':
            generafunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen,oneseq,taxon)
        #If they say filter by species then it runs the speciesfunc
        if taxfilter.upper() == 'SPECIES':
            speciesfunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen,oneseq,taxon)
        #If they say filter by both then it runs the taxafunc
        if taxfilter.upper() == 'BOTH':
            taxfunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen,oneseq,taxon)
        #If they say filter by none then it runs the onlelengthfunc
        if taxfilter.upper() == 'NONE':
            onlylengthfunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen,taxon,oneseq)
        #All of these functions call the whichanalysis function
        #With the generated label as the argument and the oneseq specifying if
        #There are multiple sequences






#This function only needs the seqdf dataframe as its argument
#It is specified as x here, but I really should have called it seqdf
def maxfunc(x):
    #Start by asking the user their desired maximum length
    #Store input as maxlen
    maxlen = input("Maximum desired sequence length:")
    #Test if the input is an integer
    #If not tell the user and prompt the input again
    try:
        maxlen = int(maxlen)
    except ValueError:
        print("maximum length not an integer")
        maxlen = input("Maximum desired sequence length:")
        maxlen = int(maxlen)
    #This tests if the input is larger than any sequence in the dataframe
    #If it it outside of the range it tells the user and prompts again
    while maxlen > int(x.describe().max()):
        print("Maximum length input is larger than any sequence in your results")
        print("The longest sequence in your results has a length of "+str(int(x.describe().max())))
        maxlen = input("Maximum desired sequence length:")
        #Doing the error check on if the input is an integer
        try:
            maxlen = int(maxlen)
        except ValueError:
            print("maximum length not an integer")
            maxlen = input("Maximum desired sequence length:")
            maxlen = int(maxlen)
    #Now this is checking that the input is larger than the smallest sequence
    #Because if the maximum is below the smallest sequence it will remove all Sequences
    #And it does the same logic and error check as the above check
    while maxlen < int(x.describe().min()):
        print("Maximum length input is smaller than any sequence in your results")
        print("The shortest sequence in your results has a length of "+str(int(x.describe().min())))
        maxlen = input("Maximum desired sequence length:")
        try:
            maxlen = int(maxlen)
        except ValueError:
            print("maximum length not an integer")
            maxlen = input("Maximum desired sequence length:")
            maxlen = int(maxlen)
    #This defines the new data frame seqdfnew as the original seqdf filtered by maxlength
    seqdfnew = x[x['SeqLength'] < maxlen]
    #Default oneseq as no
    oneseq = 'no'
    #If they return only one sample then inform user, change oneseq to yes
    #Then return the new filtered dataframe, value of maxlen, and the value of oneseq
    if seqdfnew.shape[0] <= 1:
        print("You have filtered to a single sequence, alignment analysis is not possible")
        oneseq = 'yes'
    return(seqdfnew,maxlen,oneseq)


#This runs exactly the same as maxlen excpet for the minimum length
#Checking that the input is an integer and is within the range of the results
#Then filtering the dataframe and returining the new dataframe, minlenm value, and oneseq
def minfunc(x):
    minlen = input("Minimum desired sequence length:")
    try:
        minlen = int(minlen)
    except ValueError:
        print("minimum length not an integer")
        minlen = input("Minimum desired sequence length:")
        minlen = int(minlen)
    while minlen < int(x.describe().min()):
        print("Minimum length input is smaller than any sequence in your results")
        print("The shortest sequence in your results has a length of "+str(int(x.describe().min())))
        minlen = input("Minimum desired sequence length:")
        try:
            minlen = int(minlen)
        except ValueError:
            print("minimum length not an integer")
            minlen = input("Minimum desired sequence length:")
            maxlen = int(minlen)
    while minlen > int(x.describe().max()):
        print("Minimum length input is larger than any sequence in your results")
        print("The longest sequence in your results has a length of "+str(int(x.describe().max())))
        minlen = input("Minimum desired sequence length:")
        try:
            minlen = int(minlen)
        except ValueError:
            print("minimum length not an integer")
            minlen = input("Minimum desired sequence length:")
            maxlen = int(minlen)
    seqdfnew = x[x['SeqLength'] > minlen]
    oneseq = 'no'
    if seqdfnew.shape[0] <= 1:
        print("You have filtered to a single sequence, alignment analysis is not possible")
        oneseq = 'yes'
    return(seqdfnew,minlen,oneseq)


#The generafunc, speciesfunc, and taxfunc are nearly identical
#The first argument is the newseqdf data frame filtered by length if that was selected
#They all take in lengthfilter as second argument to know whether length is included in the label
#This is coded as y, which I ideally would have changed, but now that it works I will leave
#lengthcriteria is the third argument and if the lengthfilter is YES
#It is used to know which length criteria to include in the label
#The minlen and maxlen values are then used as arguments to make these labels
#This is why the defaults are specified in the filterfunc
#oneseq is provided as an argument to serve as a default if the filter is still more than one
#And lastly it takes in the taxon label, which will come in as the txid and protein family
#from the original search, and gets appended to make the new label


def generafunc(x,y,lencrit,maxlen,minlen,oneseq,taxon):
    #Print all of the genera in the results
    #Then ask the user which genera they want
    print(x['Genus'].value_counts().to_string())
    print('These are the genera returned by your search')
    #This makes a string of all of the genera in the results
    generastr = x['Genus'].value_counts().to_string()
    print("Which genus or genera would you like to filter for? \n enter desired genera as Genus1 or Genus1,Genus2,GenusN:")
    genusin = input("Desired genus:")  #Penicillium,Wilcoxina
    #If they input multiple genera this splits them into a list
    genusinput = genusin.split(",")
    #Now this goes through for each genera from the input and checks to make sure the
    #genera appears within the list of all genera
    #If it is not it tells the user and is stuck in a while loop
    #Until they input genera that are in the list
    for genus in genusinput:
        while genus not in generastr:
            print ('Genus input: '+genus+' not in results')
            genusin = input("Desired genus:")
            genusinput = genusin.split(",")
            for genus in genusinput:
                genus = genus
    #This makes the label by joining all specified genera with "_and_"
    #Then adding this to the taxon label
    genuslabel = '_and_'.join(genusinput)
    genuslabel = taxon+"_"+genuslabel
    #By default assigning lengthlabel this label
    lengthlabel = genuslabel
    #But IF the lengthfilter is yes, then an additional length filter label is added
    if y == "YES":
        #These are the possibile length filter options
        #Based on which one was applied, the appropriate label is generated
        #Using the inputs from the minlen and maxlen arguments
        if lencrit == "MINIMUM":
            lengthlabel = genuslabel+"_minlen_"+str(minlen)
        if lencrit == "MAXIMUM":
            lengthlabel = genuslabel+"_maxlen_"+str(maxlen)
        if lencrit == "BOTH":
            lengthlabel = genuslabel+"_"+str(minlen)+"-"+str(maxlen)
    #This now makes a new dataframe pulling the entries with the desired genera
    des_gen_df = x[x['Genus'].isin(genusinput)]
    #This extracts just the fasta header and the sequence from teh dataframe
    des_gen_fa_df = des_gen_df.iloc[:, 3:5]
    #This now makes a temporary fasta file from the filtered data frame
    des_gen_fa_df.to_csv("{}bad.fa".format(lengthlabel), header=None, index=None, sep=' ')
    #Check if the filtered data frame only has one sequence
    if des_gen_df.shape[0] <= 1:
        print("You have filtered to a single sequence, alignment analysis is not possible")
        oneseq = 'yes'
    #This now goes through and cleans up the fasta file to make it readable
    #It is just removing the "\" in the file
    with open("{}bad.fa".format(lengthlabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        #And then writing the cleaned fasta to the final fasta file
        with open("{}.fa".format(lengthlabel),"w") as my_file:
             my_file.write(new)
    #Now run the whichanalysisfunc, taking the label and oneseq as arguments
    #This label will be used to open the fasta file created in the previous line
    #And oneseq determines whether to allows alignment analyses to proceed
    whichanalysisfunc(lengthlabel,oneseq)

#Speciesfunc works identically to genusfunc
#The only difference is that it uses species instead of genus
def speciesfunc(x,y,lencrit,maxlen,minlen,oneseq,taxon):
    print(x['Species'].value_counts().to_string())
    print('These are the species returned by your search')
    specstr = x['Species'].value_counts().to_string()
    print("Which species would you like to filter for? \n enter desired species as spescies1 or spescies1,spescies2,spesciesN:")
    speciesin = input("Desired species:")  #ucsense
    speciesinput = speciesin.split(",")
    for species in speciesinput:
        while species not in specstr:
            print ('Species input: '+species+' not in results')
            speciesin = input("Desired species:")
            speciesinput = speciesin.split(",")
            for species in speciesinput:
                species = species
    specieslabel = '_and_'.join(speciesinput)
    specieslabel = taxon+"_"+specieslabel
    lengthlabel = specieslabel
    if y == "YES":
        if lencrit == "MINIMUM":
            lengthlabel = specieslabel+"_minlen_"+str(minlen)
        if lencrit == "MAXIMUM":
            lengthlabel = specieslabel+"_maxlen_"+str(maxlen)
        if lencrit == "BOTH":
            lengthlabel = specieslabel+"_"+str(minlen)+"-"+str(maxlen)
    des_spec_df = x[x['Species'].isin(speciesinput)]
    des_spec_fa_df = des_spec_df.iloc[:, 3:5]
    des_spec_fa_df.to_csv("{}bad.fa".format(lengthlabel), header=None, index=None, sep=' ')
    if des_spec_df.shape[0] <= 1:
        print("You have filtered to a single sequence, alignment analysis is not possible")
        oneseq = 'yes'
    with open("{}bad.fa".format(lengthlabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(lengthlabel),"w") as my_file:
             my_file.write(new)
    whichanalysisfunc(lengthlabel,oneseq)


#Taxfunc is the same as genusfunc except it needs an extra step for generating the label
#It needs to take in the genus and species, seperated by a space, and then join them
#It joins them with a "-" and then joins subsequent genus-species pairs with "_"
#Otherwise it functions the same
def taxfunc(x,y,lencrit,maxlen,minlen,oneseq,taxon):
    print(x['Taxon'].value_counts().to_string())
    print('These are the taxa returned by your search')
    taxstr = x['Taxon'].value_counts().to_string()
    print("Which taxa would you like to filter for? \n enter desired taxa as Genus1 spescies1 or Genus1 spescies1,Genus2 spescies2,GenusN spesciesN:")
    print("For example, to filter for Penicillium brasilianum and Penicillium ucsense")
    print("Enter Penicillium brasilianum,Penicillium ucsense")
    taxin = input("Desired taxa:")
    taxinput = taxin.split(",")
    for taxa in taxinput:
        while taxa not in taxstr:
            print ('Taxa input: '+taxa+' not in results')
            taxin = input("Desired taxa:")
            taxinput = taxin.split(",")
            for taxa in taxinput:
                taxa = taxa
    taxlabel_intermediate = '_and_'.join(taxinput)
    taxlabel = taxlabel_intermediate.replace(' ', '-')
    taxlabel = taxon+"_"+taxlabel
    lengthlabel = taxlabel
    if y == "YES":
        if lencrit == "MINIMUM":
            lengthlabel = taxlabel+"_minlen_"+str(minlen)
        if lencrit == "MAXIMUM":
            lengthlabel = taxlabel+"_maxlen_"+str(maxlen)
        if lencrit == "BOTH":
            lengthlabel = taxlabel+"_"+str(minlen)+"-"+str(maxlen)
    des_tax_df = x[x['Taxon'].isin(taxinput)]
    des_tax_fa_df = des_tax_df.iloc[:, 3:5]
    des_tax_fa_df.to_csv("{}bad.fa".format(lengthlabel), header=None, index=None, sep=' ')
    if des_tax_df.shape[0] <= 1:
        print("You have filtered to a single sequence, alignment analysis is not possible")
        oneseq = 'yes'
    with open("{}bad.fa".format(lengthlabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(lengthlabel),"w") as my_file:
             my_file.write(new)
    whichanalysisfunc(lengthlabel,oneseq)


#The onlylengthfunc is simply a truncated version of the above three functions
#It does not apply any additional filtering based on taxa
#It just goes straight to the label generation step,
#Using the lengthcriteria and the maxlen and minlen values
#It generates the appropriate length filtering label and appends it to the
#Original taxon label
#It then checks that there is more than one sequence
#And initiates the whichanalysisfunc
def onlylengthfunc(x,y,lencrit,maxlen,minlen,taxon,oneseq):
    if y == "NO":
        print("You did not specified any filters to apply")
    if y == "YES":
        if lencrit == "MINIMUM":
            lengthlabel = taxon+"_minlen_"+str(minlen)
        if lencrit == "MAXIMUM":
            lengthlabel = taxon+"_maxlen_"+str(maxlen)
        if lencrit == "BOTH":
            lengthlabel = taxon+"_"+str(minlen)+"-"+str(maxlen)
        onlylen_df = x.iloc[:, 3:5]
        onlylen_df.to_csv("{}bad.fa".format(lengthlabel), header=None, index=None, sep=' ')
        if onlylen_df.shape[0] <= 1:
            print("You have filtered to a single sequence, alignment analysis is not possible")
            oneseq = 'yes'
        with open("{}bad.fa".format(lengthlabel)) as file:
            new = ''
            for line in file:
                newline = line.replace("\"", '')
                new = new + newline
            with open("{}.fa".format(lengthlabel),"w") as my_file:
                 my_file.write(new)
        whichanalysisfunc(lengthlabel,oneseq)

