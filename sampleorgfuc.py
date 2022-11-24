#!/bin/python3

#Doesn't display summary

def sampleorg(taxon):  #sampleorg('txid4890')
    import pandas as pd
    import os
    import shutil
    #This makes the dictionary
    headercommand = "grep '>' "+taxon+".fa > "+taxon+"_headers.txt"
    seqscommand = "awk '/^>/ { print '_'; next; }; {print; }' "+taxon+".fa > "+taxon+"_seqs.txt"
    os.system(headercommand)
    os.system(seqscommand)
    with open(taxon+"_headers.txt") as file:
        headers = file.read()
    with open(taxon+"_seqs.txt") as file:
        seqs = file.read()
    seqlist1 = seqs.split("\n\n")
    seqstr = " \n".join(seqlist1)
    seqlist = seqstr.split(" ")
    headerlist = headers.split("\n")
    if seqlist[0] == '':
        seqlist = seqlist[1:] #This DOES cut off first empty space
    if seqlist[-1] == '':
        seqlist = seqlist[0:-1] #This does nothing
    if headerlist[0] == '':
        headerlist = headerlist[1:] #This does nothing
    if headerlist[-1] == '':
        headerlist = headerlist[0:-1] #This cuts off the final empty space
    dictlen = len(seqlist)
    seqdict = {}
    seqdict[headerlist[0]] = seqlist[0]
    for i in range(dictlen):
        seqdict[headerlist[i]] = seqlist[i]
    #This makes the dataframe
    counter = 0
    for head, seq in seqdict.items():
        headline = head.split()
        id = (headline[0])
        id = id[1:-2]
        count = 0
        taxstart = 0
        for pos in headline:
            if '[' in pos:
                taxstart = count
            else:
                count = count + 1
        taxend = taxstart + 1
        genus = headline[taxstart]
        genus = genus[1:]
        species = headline[taxend]
        seqlen = len(seq)
        if "]" in species:
            species = species[:-1]
        #Now we make a dataframe with the id, genus, species, and sequence
        #For the first entry in the seqdict make a new series for the four categories
        if counter == 0:
            idser = pd.Series([id])
            genusser = pd.Series([genus])
            speciesser = pd.Series([species])
            seqser = pd.Series([seq])
            headser = pd.Series([head])
            taxser = pd.Series([genus +" "+ species])
            seqlength = pd.Series([seqlen])
            counter = counter + 1
        #Then for all other entries append those series with this entry in the seqdict
        #Also specifying that the index should be the counter
        else:
            idserapp = pd.Series([id], index=[counter])
            idser = idser.append(idserapp)
            genusserapp = pd.Series([genus], index=[counter])
            genusser = genusser.append(genusserapp)
            speciesserapp = pd.Series([species], index=[counter])
            speciesser = speciesser.append(speciesserapp)
            seqserapp = pd.Series([seq], index=[counter])
            seqser = seqser.append(seqserapp)
            headserapp = pd.Series([head], index=[counter])
            headser = headser.append([headserapp])
            taxserapp = pd.Series([genus +" "+ species], index=[counter])
            taxser = taxser.append([taxserapp])
            seqlengthapp = pd.Series([seqlen], index=[counter])
            seqlength = seqlength.append([seqlengthapp])
            counter = counter + 1
            #And finally make the dictionaries, with and without sequences
    seqdf = pd.DataFrame( { 'ID' : idser, 'Genus' : genusser, 'Species' : speciesser, 'Header' : headser, 'Sequence' : seqser, 'Taxon' : taxser, 'SeqLength' : seqlength} )
    return(seqdf)

