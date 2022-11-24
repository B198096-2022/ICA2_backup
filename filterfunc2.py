#!/bin/python3

#Put error if you only put one sequence in (can't align!)
#Makesure max and min are not too big and too small, respectively
#For pipe do try and except for if the search doesn't work is os.system returns 0 or 1

from whichanalyses import *
import os


def filterfunc(taxon, seqdf):  #filterfunc('txid4890')
    seqdfnew = seqdf
    seqdf = seqdf
    minlen=0
    maxlen='all'
    lengthfilter = input("would you like to filter by sequence length? (yes/no):")
    while lengthfilter.upper() != 'YES' and lengthfilter.upper() != 'NO':
        print("Answer not yes or no value")
        lengthfilter = input("would you like to filter by sequence length? (yes/no):")
    if lengthfilter.upper() == "YES":
        lengthcriteria = input("would you like to filter by sequence length maximum, minimum, or both?:")
        while lengthcriteria.upper() != 'MAXIMUM' and lengthcriteria.upper() != 'MINIMUM' and lengthcriteria.upper() != 'BOTH':
            print("Answer not one of the options")
            lengthcriteria = input("would you like to filter by sequence length maximum, minimum, or both?")
    if lengthcriteria.upper() == "MAXIMUM":
        seqdfnew,maxlen = maxfunc(seqdfnew)
    if lengthcriteria.upper() == "MINIMUM":
        seqdfnew,minlen = minfunc(seqdfnew)
    if lengthcriteria.upper() == "BOTH":
        seqdfnew,maxlen = maxfunc(seqdfnew)
        seqdfnew,minlen = minfunc(seqdfnew)
    taxfilter = input("Would you like to filter by genera, species, both, or none?:")
    while taxfilter.upper() != 'GENERA' and taxfilter.upper() != 'SPECIES' and taxfilter.upper() != 'BOTH' and taxfilter.upper() != 'NONE':
        print("Answer not one of options: genera, species, both, or none")
        taxfilter = input("Would you like to filter by genera, species, both, or none?:")
    if taxfilter.upper() == 'GENERA':
        generafunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen)
    if taxfilter.upper() == 'SPECIES':
        speciesfunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen)
    if taxfilter.upper() == 'BOTH':
        taxfunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen)
    if taxfilter.upper() == 'NONE':
        onlylengthfunc(seqdfnew,lengthfilter.upper(),lengthcriteria.upper(),maxlen,minlen,taxon)








def maxfunc(x):
    maxlen = input("Maximum desired sequence length:")
    try:
        maxlen = int(maxlen)
    except ValueError:
        print("maximum length not an integer")
        maxlen = input("Maximum desired sequence length:")
        maxlen = int(maxlen)
    while maxlen > int(x.describe().max()):
        print("Maximum length input is larger than any sequence in your results")
        print("The longest sequence in your results has a length of "+str(int(x.describe().max())))
        maxlen = input("Maximum desired sequence length:")
        try:
            maxlen = int(maxlen)
        except ValueError:
            print("maximum length not an integer")
            maxlen = input("Maximum desired sequence length:")
            maxlen = int(maxlen)
    seqdfnew = x[x['SeqLength'] < maxlen]
    return(seqdfnew,maxlen)



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
    seqdfnew = x[x['SeqLength'] > minlen]
    return(seqdfnew,minlen)



def generafunc(x,y,lencrit,maxlen,minlen):
    print(x['Genus'].value_counts().to_string())
    print('These are the genera returned by your search')
    generastr = x['Genus'].value_counts().to_string()
    print("Which genus or genera would you like to filter for? \n enter desired genera as Genus1 or Genus1,Genus2,GenusN:")
    genusin = input("Desired genus:")  #Penicillium,Wilcoxina
    genusinput = genusin.split(",")
    for genus in genusinput:
        while genus not in generastr:
            print ('Genus input: '+genus+' not in results')
            genusin = input("Desired genus:")
            genusinput = genusin.split(",")
            for genus in genusinput:
                genus = genus
    genuslabel = '_and_'.join(genusinput)
    if y == "YES":
        if lencrit == "MINIMUM":
            lengthlabel = genuslabel+"_minlen_"+str(minlen)
        if lencrit == "MAXIMUM":
            lengthlabel = genuslabel+"_maxlen_"+str(maxlen)
        if lencrit == "BOTH":
            lengthlabel = genuslabel+"_"+str(minlen)+"-"+str(maxlen)
    des_gen_df = x[x['Genus'].isin(genusinput)]
    des_gen_fa_df = des_gen_df.iloc[:, 3:5]
    des_gen_fa_df.to_csv("{}bad.fa".format(lengthlabel), header=None, index=None, sep=' ')
    with open("{}bad.fa".format(lengthlabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(lengthlabel),"w") as my_file:
             my_file.write(new)
    whichanalysisfunc(lengthlabel)


def speciesfunc(x,y,lencrit,maxlen,minlen):
    print(x['Species'].value_counts().to_string())
    print('These are the species returned by your search')
    specstr = x['Species'].value_counts().to_string()
    print("Which species would you like to filter for? \n enter desired species as Spescies1 or Spescies1,Spescies2,SpesciesN:")
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
    with open("{}bad.fa".format(lengthlabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(lengthlabel),"w") as my_file:
             my_file.write(new)
    whichanalysisfunc(lengthlabel)


def taxfunc(x,y,lencrit,maxlen,minlen):
    print(x['Taxon'].value_counts().to_string())
    print('These are the taxa returned by your search')
    taxstr = x['Taxon'].value_counts().to_string()
    print("Which taxa would you like to filter for? \n enter desired taxa as Genus1 Spescies1 or Genus1 Spescies1,Genus2 Spescies2,GenusN SpesciesN:")
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
    with open("{}bad.fa".format(lengthlabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(lengthlabel),"w") as my_file:
             my_file.write(new)
    whichanalysisfunc(lengthlabel)


def onlylengthfunc(x,y,lencrit,maxlen,minlen,taxon):
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
        with open("{}bad.fa".format(lengthlabel)) as file:
            new = ''
            for line in file:
                newline = line.replace("\"", '')
                new = new + newline
            with open("{}.fa".format(lengthlabel),"w") as my_file:
                 my_file.write(new)
        whichanalysisfunc(lengthlabel)

