#!/bin/python3
#This code will go through and extract the genus and species for every entry
#For every header in the dictionary it splits the header into a list
#Extracts the id, removes the > and .1 and saves it as id
#Then it looks at all of the items in the header list and determines where the
#Genus starts based on the presence of the [ and stores this as taxstart
#Then taxend is just the taxstart plus one
#Finally we remove the [ from genus and test to see if a ] after species needs removing
import pandas as pd
import os
import shutil
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
        counter = counter + 1

#And finally make the dictionaries, with and without sequences
seqdf = pd.DataFrame( { 'ID' : idser, 'Genus' : genusser, 'Species' : speciesser, 'Header' : headser, 'Sequence' : seqser, 'Taxon' : taxser } )
noseqdf = pd.DataFrame( { 'ID' : idser, 'Genus' : genusser, 'Species' : speciesser } )

#Output for the user to see how many results they got
entries = str(seqdf.shape)
entries = entries.split(",")[0]
entries = entries[1:]
genuscount = str(len(seqdf['Genus'].value_counts()))
speccount = str(len(seqdf['Species'].value_counts()))
print("Your query returned "+entries+" results")
print("This includes "+genuscount+" unique genera")
print("And "+speccount+" unique species")


#provide genus and species
seqdf['Genus'].value_counts()
seqdf['Species'].value_counts()
seqdf["Taxon"].value_counts()

#Ask user if they want a subgroup
genusin = input("Desired genus:")  #Penicillium,Wilcoxina
genusinput = genusin.split(",")
genuslabel = '_and_'.join(genusinput)
speciesin = input("Desired species:")  #ucsense
speciesinput = speciesin.split(",")
specieslabel = '_and_'.join(speciesinput)
taxin = input("Desired taxon:")  #Penicillium brasilianum,Penicillium ucsense
taxinput = taxin.split(",")
taxlabel_intermediate = '_and_'.join(taxinput)
taxlabel = taxlabel_intermediate.replace(' ', '-')

#This makes a new data frame with only the desired genus or species
#Then makes a fasta format file for that subset
#Then does a clustalo on the fasta file
if genusinput != ['']:
    des_gen_df = seqdf[seqdf['Genus'].isin(genusinput)]
    des_gen_fa_df = des_gen_df.iloc[:, 3:5]
    des_gen_fa_df.to_csv("{}bad.fa".format(genuslabel), header=None, index=None, sep=' ')
    with open("{}bad.fa".format(genuslabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(genuslabel),"w") as my_file:
             my_file.write(new)
        cluscommand = "clustalo -i "+genuslabel+".fa -threads=16 -t protein --outfmt=msf -o "+genuslabel+".msf"
        os.system(cluscommand)


if speciesinput != ['']:
    des_spec_df = seqdf[seqdf['Species'].isin(speciesinput)]
    des_spec_fa_df = des_spec_df.iloc[:, 3:5]
    des_spec_fa_df.to_csv("{}bad.fa".format(specieslabel), header=None, index=None, sep=' ')
    with open("{}bad.fa".format(specieslabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(specieslabel),"w") as my_file:
             my_file.write(new)
        cluscommand = "clustalo -i "+specieslabel+".fa -threads=16 -t protein --outfmt=msf -o "+specieslabel+".msf"
        os.system(cluscommand)


if taxinput != ['']:
    des_tax_df = seqdf[seqdf['Taxon'].isin(taxinput)]
    des_tax_fa_df = des_tax_df.iloc[:, 3:5]
    des_tax_fa_df.to_csv("{}bad.fa".format(taxlabel), header=None, index=None, sep=' ')
    with open("{}bad.fa".format(taxlabel)) as file:
        new = ''
        for line in file:
            newline = line.replace("\"", '')
            new = new + newline
        with open("{}.fa".format(taxlabel),"w") as my_file:
             my_file.write(new)
        cluscommand = "clustalo -i "+taxlabel+".fa -threads=16 -t protein --outfmt=msf -o "+taxlabel+".msf"
        os.system(cluscommand)


#Performing the patmatmotifs for a subgroup
if genusinput != ['']:
    motiffunc(genuslabel)
if speciessinput != ['']:
    motiffunc(specieslabel)
if taxinput != ['']:
    motiffunc(taxlabel)


