#!/bin/python3
#This function doesn't need the first block of code to make the library, since
#This code is already in the pipeline
#However, one of the other professors said that functions should be as self sufficient as possible
#So I figured I should included it within the function here as well


#The motiffunc function performs the patmatmotifs analysis
#And then makes a directory for all of the .patmatmotifs output files
#It takes the taxon label as its argument for file names
def motiffunc(taxon):
    #It needs os and shutil to worj
    import os
    import shutil
    #Same as for the sampleorg function
    #It makes a new file with the fasta headers as well as the sequences
    #This time specified for the filtered label if applicable
    headercommand = "grep '>' "+taxon+".fa > "+taxon+"_headers.txt"
    seqscommand = "awk '/^>/ { print '_'; next; }; {print; }' "+taxon+".fa > "+taxon+"_seqs.txt"
    os.system(headercommand)
    os.system(seqscommand)
    #This section below is making a dictionary from the headers and seqs files
    #It is the same as the sampleorgfunc
    #But uses the dictionary as is instead of turning it into a dataframe
    #the commented code for how this works is in sampleorgfunc.py
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
    if seqlist[-1] == '\n':
        seqlist = seqlist[0:-1] #This removes an extra '\n' at the end if its there
    if headerlist[0] == '':
        headerlist = headerlist[1:] #This does nothing
    if headerlist[-1] == '':
        headerlist = headerlist[0:-1] #This cuts off the final empty space
    dictlen = len(seqlist)
    seqdict = {}
    seqdict[headerlist[0]] = seqlist[0]
    for i in range(dictlen):
        seqdict[headerlist[i]] = seqlist[i]
    #Now that I have a dictionary with every sequence and its fasta header
    #Its time to run patmatmotifs
    #I first need to make a directory for the outputs
    #And I also need to make individual fasta files to run patmatmotifs on
    #So for the sake of organization I also made a directory for those
    #If the directories already exist then the program crashes, so this will
    #Try to make it, and if it already exists will inform the user and cary on
    try:
        os.mkdir("./"+taxon+"_patmatmotifs")
    except:
        print("directory "+taxon+"_patmatmotifs already exists, adding files to directory" )
    try:
        os.mkdir("./"+taxon+"_indifasta")
    except:
        print("directory "+taxon+"_indifasta already exists, adding files to directory" )
    #I am now making the individual fasta files
    for head, seq in seqdict.items():
        #The variable fasta just pastes the header and sequence together
        #Which will be the contents of the fasta file created
        fasta = head+seq
        #I am now taking the accession of each entry from its header
        #Which is saved as the variable code
        headline = head.split()
        code = (headline[0])
        code = code[1:-2]
        #This is just updating the user on what the program is doing
        print("Identifying motifs for "+head)
        #Now the program creates a new file for each accession
        #and puts its fasta file contents into it
        with open("{}.fa".format(code),"w") as my_file:
             my_file.write(fasta)
        #The patmatmotifs command, specifying the input and output files
        #And specifying to do full analysis, sequence is proteiin, format is fasta
        #Then using os.system() to execute the command
        command = "patmatmotifs -full -sequence "+code+".fa -sprotein1 YES -sformat1 fasta -outfile "+code+".patmatmotifs"
        os.system(command)
        #Lastly I am moving the patmatmotifs file and the fasta file to their directories
        shutil.move("./"+code+".patmatmotifs", "./"+taxon+"_patmatmotifs/"+code+".patmatmotifs")
        shutil.move("./"+code+".fa", "./"+taxon+"_indifasta/"+code+".fa")

