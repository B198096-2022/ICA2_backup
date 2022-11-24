
#!/bin/python3
#This function will print a list of the motifs found given the genus/species/taxon label
#Here I realized that taxon was not a clear variable name and used label instead
#Ideally I would have done the same in every other function, but did not want
#To miss something or risk a typo that broke the code
#But it takes in the label, same as taxon elsewhere, and uses that to specify files
def motiflist(label):
    #The function needs os to work
    import os
    #creating the varaible allmotifs
    allmotifs = ''
    #Now opening up every file made from the motiffunc
    #Which are stored in a directory named with the label
    #So this opens every file within this directory
    for filename in os.listdir("{}_patmatmotifs".format(label)):
        with open("./{}_patmatmotifs/".format(label)+filename) as file:
            #For each motif result file it scans for every line
            #That has 'Motif:' in it and pulls it
            #Then adds it to the motifs varaible
            motifs = ''
            for line in file:
                if "Motif:" in line:
                    motif = line
                    motifs = motifs +"  "+motif
            #If a given sequence had no motifs found
            #It prints "no motifs found\n"
            if motifs == '':
                motifs = "no motifs found\n"
            #Making a varaible with the accession number from the file name
            accession = filename[:-13]
            #This will print the results to the screen
            print('Accession number: '+accession)
            print(motifs)
            #Then this makes a big string with all of the results from above
            allmotifs = allmotifs + 'Accession number: '+accession+"\n"+motifs+"\n"
    #And lastly creates a file with all of the motifs found
    #So it can be accessed by the user later if they want
    with open("{}_motifs.txt".format(label),"w") as my_file:
        my_file.write(allmotifs)







#This function pulls all of the patmatmotifs files for a given subgroup
#And makes a new file with JUST the motif names found for each sample

