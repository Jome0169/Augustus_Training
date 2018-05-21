from sys import argv
import os

"""
takes a list BLAST file of all individuals from GFF3 pasa filter and the reads
the blast output when previous file was blasted against conserved known genome
proteins from melon, cucubit, etc...


It only keeps proteins from the "completed pep" file that blast to at least 1
other protein with 40% percent certainty. If this occurs then we keep the file
and firhter put it's corresponding sequence and blast data into  associted
files POSSIBLECONSVDSEQ etc...
"""



#-outfmt "6 qseqid sseqid qlen slen length pident evalue bitscore"


def ReadBlast(Filearg):
    SequencesToKee = []

    with open(Filearg, 'r') as f:
        for line in f:
            Clean = line.strip("\n").split("\t")
            if int(Clean[3]) == int(Clean[4]) and \
            int(Clean[2]) == int(Clean[3]) and \
            int(Clean[2]) == int(Clean[4]) and \
            float(Clean[5]) > 50.00 :
                SequencesToKee.append(Clean)
    return SequencesToKee



def OnlyUniqAssmbl(BlastResult):
    UniqBlast = []
    for item in BlastResult:
        if item[0] not in UniqBlast:
            UniqBlast.append(item[0])
        else:
            pass
    return set(UniqBlast)



def LoadProtFiles(FileToParse):
    GenomicFile = {}
    with open(FileToParse, "r") as f:
        for line in f:
            line = line.strip('\n')
            if line.startswith('>'):
                HeaderLine = line
                GenomicFile[HeaderLine] = ""
            else:
                GenomicFile[HeaderLine] += line
    return GenomicFile 



def WriteDictSeq(item1, item2):
    with open("StrictPossibleConsvdSeq.fasta", 'a') as f:
        f.write(item1)
        f.write('\n')
        f.write(item2)
        f.write('\n')


def WriteGoodBlast(ListofI):
    try:
        os.remove("StrictBlastPossibleConsvdSeq.blast")
    except OSError:
        pass

    with open("StrictBlastTable_PossibleConsvdSeq.blast", 'a') as Z:
        Header = "qseqid sseqid qlen slen length pident evalue bitscore"
        SplitHead = Header.split(' ')
        JoinedHead = '\t'.join(SplitHead)
        Z.write(JoinedHead)
        Z.write('\n')
        for item in ListofI:
            Q = '\t'.join(item)
            Z.write(Q)
            Z.write('\n')


def FindAssmble(passedammbl, ProtDict):
    try:
        os.remove("StrictPossibleConsvdSeq.fasta")
    except OSError:
        pass

    for key, item in ProtDict.iteritems():
        CleanKey = key.split(' ')
        Finished = CleanKey[0].replace('>', '')
        if Finished in passedammbl:
            WriteDictSeq(key, item)
        else:
            pass




KeptBlast = ReadBlast(argv[1])
AssmblyName = OnlyUniqAssmbl(KeptBlast)
Assemblies = LoadProtFiles(argv[2])
FindAssmble(AssmblyName,Assemblies)
WriteGoodBlast(KeptBlast)



