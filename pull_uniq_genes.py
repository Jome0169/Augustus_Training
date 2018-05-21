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


def WriteDictSeq(item1, item2, output):
    with open(output, 'a') as f:
        f.write(item1)
        f.write('\n')
        f.write(item2)
        f.write('\n')


def FindBadAssmble(Nonpass, ProtDict, output):
    output_final = str(output) + '.fasta'

    try:
        os.remove(output_final)
    except OSError:
        pass

    for key, item in ProtDict.iteritems():
        FixKey = key.replace(">",'').split(' ')
        if FixKey[0] in Nonpass:
            pass
        else:
            WriteDictSeq(key, item, output_final)


def get_parser():
    parser = argparse.ArgumentParser(description='After blasting possible genes \
            versus themselves, this file takes in both the BLAST output in \
            fmt6, and the fasta file, and only reports genes that are unique. \
            In this way we avoid biasiing the training set.')

    parser.add_argument('-f','--fasta', help='PASA gene file ', \
            required=True, dest='f')
    parser.add_argument('-b','--blast', help='concatenated BLAST file in outfmt 6',\
            required=False,dest='b') 
    parser.add_argument('-o','--output', help='Base output file name',\
            required=False,dest='o') 

 


   
if __name__ == "__main__":
    args = get_parser().parse_args()
    StartTime = datetime.now()
    
    print("reading in blast")
    Filter1 = FilterOutSelfVSelf(args.b)
    Filter2 = FilterOut80s(Filter1)
    print("Reading in fasta")
    ProtFile = LoadProtFiles(args.f)

    print("Writing output file %s" % args.o)
    FindBadAssmble(Filter2,ProtFile, args.o)


 
endtime = datetime.now()
finaltime = endtime - StartTime 
print ("Total Time %s" % (finaltime))

     





