#!/bin/python3
import os
import shutil

taxon = "txid4890"

#The awk command doesn't work in this format
headercommand = "grep '>' "+taxon+".prot.fa > headers.txt"
seqscommand = "awk '/^>/ { print '_'; next; }; {print; }' "+taxon+".prot.fa > seqs.txt"
os.system(headercommand)
os.system(seqscommand)


with open("headers.txt") as file:
    headers = file.read()

with open("seqs.txt") as file:
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


#Thinking I'll need to make an actual fasta file and then read in the file
os.mkdir("./patmatmotifs")
os.mkdir("./indifasta")

for head, seq in seqdict.items():
    fasta = head+seq
    headline = head.split()
    code = (headline[0])
    code = code[1:-3]
    with open("{}.fa".format(code),"w") as my_file:
         my_file.write(fasta)
    command = "patmatmotifs -full -sequence "+code+".fa -sprotein1 YES -sformat1 fasta -outfile "+code+".patmatmotifs"
    os.system(command)
    shutil.move("./"+code+".patmatmotifs", "./patmatmotifs/"+code+".patmatmotifs")
    shutil.move("./"+code+".fa", "./indifasta/"+code+".fa")
