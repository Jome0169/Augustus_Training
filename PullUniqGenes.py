from sys import argv
import os




"""
The purpose of this file is to take the blast file created when all isolated
proteins are blasted against one another. The idea behind this being that in
order to create the best training set possible we must remove redundent genes
and only give the highest quality possible training sets

this program takes in a blast file that containts the following output fmt

6 qseqid sseqid qlen slen length pident qcovs

The input arguments should be the Blast table of possible consvd seq as arg 1m
and the Possible consvd seqBlast table of possible consvd seq as arg 1m and the
tas argument 2 

"""




def FilterOutSelfVSelf(FileName):
    BadBois = []
    with open(FileName, 'r') as f:
        for line in f:
            Clean = line.strip("\n").split("\t")
            if Clean[0] == Clean[1]:
                pass
            else:
                BadBois.append(Clean)
    return BadBois
    
def FilterOut80s(ListofNonSelf):
    FuckedUpIndividuals = set()
    for item in ListofNonSelf:
        TakeCovLen = TakeCovLen = (float(item[4]) / float(item[2]))

        if float(item[5]) > 70.0 and int(item[6]) > 70:
            if int(item[2]) > int(item[3]):
                FuckedUpIndividuals.add(item[1])

            elif int(item[2]) < int(item[3]):
                FuckedUpIndividuals.add(item[0])

            elif int(item[2]) == int(item[3]):
                if item[0] not in FuckedUpIndividuals and item[1] not in FuckedUpIndividuals:
                   FuckedUpIndividuals.add(item[1])
                else:
                    pass
        else:
            pass
    return FuckedUpIndividuals

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
    with open("ConsvdSeq.fasta", 'a') as f:
        f.write(item1)
        f.write('\n')
        f.write(item2)
        f.write('\n')


def FindBadAssmble(Nonpass, ProtDict):
    try:
        os.remove("ConsvdSeq.fasta")
    except OSError:
        pass

    for key, item in ProtDict.iteritems():
        FixKey = key.replace(">",'').split(' ')
        if FixKey[0] in Nonpass:
            pass
        else:
            WriteDictSeq(key, item)


Filter1 = FilterOutSelfVSelf(argv[1])
Filter2 = FilterOut80s(Filter1)
ProtFile = LoadProtFiles(argv[2])
FindBadAssmble(Filter2,ProtFile)

