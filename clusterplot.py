#!bin/bash/python3

#This clusters the sequences into msf format
clustercommand = "clustalo -i "+taxon+".fa -threads=16 -t protein --outfmt=msf -o "+taxon+"align.msf"
os.system(clustercommand)

#This makes the conservation plot
plotconcommand = "plotcon -sformat msf "+taxon+"align.msf -graph cps"
os.system(plotconcommand)

#This generates a file with the alignment info for each protein
infocommand = "infoalign "+taxon+"align.msf -outfile "+taxon+"aligninfo.txt -only -heading -name -seqlength -idcount -simcount -diffcount -change"
os.system(infocommand)

def clusterplotfunc(taxon):
    #This clusters the sequences into msf format
    clustercommand = "clustalo -i "+taxon+".fa -threads=16 -t protein --outfmt=msf -o "+taxon+"align.msf"
    os.system(clustercommand)

    #This makes the conservation plot
    plotconcommand = "plotcon -sformat msf "+taxon+"align.msf -graph cps"
    os.system(plotconcommand)

    #This generates a file with the alignment info for each protein
    infocommand = "infoalign "+taxon+"align.msf -outfile "+taxon+"aligninfo.txt -only -heading -name -seqlength -idcount -simcount -diffcount -change"
    os.system(infocommand)
