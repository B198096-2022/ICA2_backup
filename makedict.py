#!/bin/python3
#This code splits up the protein seqiences into fasta headers and sequences
#Puts a "_" to deliminate the sequences
#Open the files in python then split them into a list
#Then put them into a dict with header as key and seq as value
grep ">" txid4890.prot.fa > headers.txt
awk '/^>/ { print "_"; next; }; {print; }' txid4890.prot.fa > seqs.txt

with open("headers.txt") as file:
    headers = file.read()

with open("seqs.txt") as file:
    seqs = file.read()

seqclean = seqs.replace("\n", "")
seqlist = seqclean.split("_")
headerlist = headers.split("\n")

dictlen = len(seqlist)

seqdict = {}
seqdict[header[0]] = seqlist[0]
for i in range(dictlen):
    seqdict[headerlist[i]] = seqlist[i]
