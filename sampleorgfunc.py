#!/bin/python3

#Like the other functions, it takes the taxon variable in as its argument
#Which is the label used for file naming

def sampleorg(taxon):  #sampleorg('txid4890')
    #The function needs pandas, os, and shutil
    import pandas as pd
    import os
    import shutil
    #This makes the dictionary
    #It starts by taking the fasta file and pulling every line with
    #a ">" as the header line and putting them in a new headers file
    #Then it takes all of the other lines and puts them in a seqs file
    headercommand = "grep '>' "+taxon+".fa > "+taxon+"_headers.txt"
    seqscommand = "awk '/^>/ { print '_'; next; }; {print; }' "+taxon+".fa > "+taxon+"_seqs.txt"
    os.system(headercommand)
    os.system(seqscommand)
    #Opening the headers and seqs files into python
    with open(taxon+"_headers.txt") as file:
        headers = file.read()
    with open(taxon+"_seqs.txt") as file:
        seqs = file.read()
    #This splits the headers and seqs files into lists
    #The seqs list had to remove the \n then rejoin and split again
    #This was because within a sequence there are \n but then between
    #Sequences there are two \n, but the naturally occuring \n within
    #and at the ends of the sequences are needed so I had to split, then
    #Rejoin with a space between sequences, then split again
    seqlist1 = seqs.split("\n\n")
    seqstr = " \n".join(seqlist1)
    seqlist = seqstr.split(" ")
    headerlist = headers.split("\n")
    #This is just checking to make sure that there are no blank spaces
    #At the beginning or end of the list and if so removing them
    if seqlist[0] == '':
        seqlist = seqlist[1:] #This DOES cut off first empty space
    if seqlist[-1] == '':
        seqlist = seqlist[0:-1] #This does nothing
    if headerlist[0] == '':
        headerlist = headerlist[1:] #This does nothing
    if headerlist[-1] == '':
        headerlist = headerlist[0:-1] #This cuts off the final empty space
    #Specifying that the dictionary length will be the number of sequences
    dictlen = len(seqlist)
    #Making the empty dictionary
    seqdict = {}
    seqdict[headerlist[0]] = seqlist[0]
    #Now for every position in the range spanning the total number of Sequences
    #The for loop will go through and add the corresponding header and sequence
    for i in range(dictlen):
        seqdict[headerlist[i]] = seqlist[i]
    #Now that we have the dictionary the next chunk puts it into a dataframe
    #Starting counter
    counter = 0
    #Now for every header and sequence in the dictionary
    for head, seq in seqdict.items():
        #Make a lits of every part of the header line
        headline = head.split()
        #save the accession as id variable
        #Removing the ">" and ".1" from beginning and end
        #This just helps the file names be usable
        id = (headline[0])
        id = id[1:-2]
        #this is simply checking for the position in the list of header elements
        #Where the genus starts and then that plus one for the species
        count = 0
        taxstart = 0
        #The '[' denotes the start of the genus label
        #And then one after the genus is the species
        for pos in headline:
            if '[' in pos:
                taxstart = count
            else:
                count = count + 1
        taxend = taxstart + 1
        genus = headline[taxstart]
        #Removing the bracket from the start of the genus name
        genus = genus[1:]
        species = headline[taxend]
        #The length of the sequence is recorded as seqlen to put into the dataframe
        seqlen = len(seq)
        #Remove the bracket after the species
        #The reason it is an if is that some entries have extra numbers after
        #The species that get cut out here, but also cut out the bracket
        if "]" in species:
            species = species[:-1]
        #Now we make a dataframe with the id, genus, species, sequence, fasta header, taxon, and sequence length
        #For the first entry in the seqdict make a new series for each category
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
        #this is done by makeing an intermediate series (with app at the end of the name)
        #And then appending the existing series wtih the intermediate series
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
            #And finally make the dictionary with all of the columns as the series
            #And return the dataframe
    seqdf = pd.DataFrame( { 'ID' : idser, 'Genus' : genusser, 'Species' : speciesser, 'Header' : headser, 'Sequence' : seqser, 'Taxon' : taxser, 'SeqLength' : seqlength} )
    return(seqdf)

