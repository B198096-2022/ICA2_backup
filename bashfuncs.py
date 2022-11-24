#!/bin/python3
#I need os for doing the os.system() command
import os

#For all functions the "taxon" variable is the label used to specify a given fasta file that gets used
#For the analysis. This will wither be the fasta file from the initial search, or if it gets filtered
#By the filterfunc the filtering applied gets appended to the end of the label in the file name
#And the functiosn below get called with the appended "taxon" label as the argument to access the
#Appropriate filtered file

#The clusterfunc is running the clustalo alignment
#It takes the taxon variable in as argument
#then it uses this varaibel to specify the desired fasta file as input
#Runs on 16 threats to help speed things up
#I specify that they type of sequence is protein
#I want the output file to me msf for the subsequent anayses
#And I make an output file named appropriately
#I then run the command with os.system
def clusterfunc(taxon):
    clustercommand = "clustalo -i "+taxon+".fa -threads=16 -t protein --outfmt=msf -o "+taxon+"align.msf"
    os.system(clustercommand)


#This is the plotcon command using the taxon label like above
#The input format is msf
#The input file is the msf file with the appropriate name made from the clustalo command
#I set windowsize as 4 as this is the recommended default
#I specify the output as a png file as it is more aestheticaly pleasing when displayed
#I then give the plot a title based on the taxon label
#Then output it to a file named appropriately using the label
#I then run the command with os.system
#And display the plot using os.system and the display command
def plotconfunc(taxon):
    #This makes the conservation plot
    plotconcommand = "plotcon -sformat msf "+taxon+"align.msf -winsize 4 -graph png -gtitle "+taxon+"_conservation_plot -goutfile "+taxon+"_plotcon"
    displaycommand = "display "+taxon+"_plotcon.1.png"
    os.system(plotconcommand)
    os.system(displaycommand)


#This is the infoalign emboss function, which outputs the numerical values for the alignment
#The command specifies the input file based on the taxon label, makes an output file
#WIth an appropriate name, and then I specified that I wanted it to only show the
#heading, name, sequence length, then identity, similarity, and difference count
#Which is calculated from the consensus sequence, and then the percent change
#I then run the command with os.system
#And display the first 10 rows using os.system and the display command
def aligninfofunc(taxon):
    #This generates a file with the alignment info for each protein
    infocommand = "infoalign "+taxon+"align.msf -outfile "+taxon+"_aligninfo.txt -only -heading -name -seqlength -idcount -simcount -diffcount -change"
    displaycommand = "head -10 "+taxon+"_aligninfo.txt"
    print("The full set of alignment info is written in "+taxon+"_aligninfo.txt")
    os.system(infocommand)
    os.system(displaycommand)


#This is the prettyplot function from emboss
#When looking through the EMBOSS catalogue I was most fond of this one because it displays
#The alignment information very aestheticaly with colors and boxes drawn around conserved sequences
#So I considered it to be the most relevant function for the conservation task being done
#I specify the input format as msf and then the input and output files using the taxon label
#I specified that I wanted it to color the outputs
#And then I chose to output the file as a cps format, this is because the output is oftentimes
#Multiple pages long. In other formats that I tested, such as png, this generates a new file
#For every single page, which is a pain to display and to organize in the user's directory
#The cps format generates a single output file with multiple pages
#So eventhough it is less aestheticaly pleasing when viewed in terminal, the file that
#I am assuming that user will export is much much more manageable and looks fine when exported
#I then run the command with os.system
#And display the plot using os.system and the display command
def prettyplotfunc(taxon):
    #pretty plot shows the alignments visually
    prettycommand = "prettyplot "+taxon+"align.msf -sformat1 msf -docolour -graph cps -goutfile "+taxon+"_prettyplot"
    os.system(prettycommand)
    displaycommand = "display "+taxon+"_prettyplot.ps"
    os.system(displaycommand)


