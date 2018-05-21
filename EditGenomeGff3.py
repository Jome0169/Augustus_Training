import itertools
import time 
import getopt
import os, sys



def GetHeaderFromConsvd(SeqFile):
    HeaderSeq = []
    with open (SeqFile, 'r') as f:
        for line in f:
            if line.startswith('>'):
                Newline = line.strip('\n').replace('>', '').split(" ")
                if len(Newline) > 1:
                    HeaderSeq.append(Newline[0])
                    HeaderSeq.append(Newline[1])
                else:
                    HeaderSeq.append(Newline[0])
            else:
                pass
    return set(HeaderSeq)




def GroupGff3(GffGenomeFile):
    AssemblyGroupin = []
    with open(GffGenomeFile, 'r') as z:
        Group = []
        for line in z:
            X = len(line)
            if X != 1:
                Cleanline = line.strip('\n').split('\t')
                Group.append(Cleanline)
            elif X == 1:
                AssemblyGroupin.append(Group)
                Group = []
    return AssemblyGroupin


def FindGoodGroups(Assmblys, seqset):
    HitSeq = []
    OneTrancsript = []
    for assmb in Assmblys:
        OnlyHeader = assmb[0][8].replace('ID=', '').split(';')
        RemoveId = OnlyHeader[0]
        if RemoveId in seqset:
            HitSeq.append(assmb)

    return HitSeq



def CreateDictSingleLocations(ListofGff4s):
    GeneOverlapDict = {}    
    GeneLocation = {}
    AllGenes = []
    for gene in ListofGff4s:
        for seq in gene:
            if seq[2] == 'gene':
                AllGenes.append(seq)
   
#ONLY ADD THING THAT OCCUR ONCE OR 5 TIMES NO MORE than 5  - eradicate others

    for item in AllGenes:
        LocationInfo = (item[3], item[4])
        if LocationInfo not in GeneLocation:
            GeneLocation[LocationInfo] = 1
        else:
            GeneLocation[LocationInfo] += 1

 
    for thing in AllGenes:
        LocationInfo = (thing[3], thing[4])
        if GeneLocation[LocationInfo] == 1 and thing[0] not in GeneOverlapDict:
            GeneOverlapDict[thing[0]] = [thing]
        elif GeneLocation[LocationInfo] == 1 and thing[0] in GeneOverlapDict:
           GeneOverlapDict[thing[0]].append(thing)
        else:
            pass
    return GeneOverlapDict
    

def CreateDict(ListofScafs):
    CreatedDict = {}
    for item in ListofScafs:
        if item[0] not in CreatedDict:
            CreatedDict[item[0]] = [item]   
        else:
            CreatedDict[item[0]].append(item)
    return CreatedDict





def RemoveOver(ScafDict):

    def checkOverlap(itema, itemb):
        Ends = max(int(itema[4]),int(itemb[4]))
        Starts = min(int(itema[3]),int(itemb[3])) 
        if int(Ends) - int(Starts) < ((int(itema[4]) - int(itema[3])) + \
                (int(itemb[4]) - int(itemb[3]))):
            return False
        else:
            #No Overlap return True
            return True

    Overlap = []
    Nooverlap = []
    for key, value in ScafDict.iteritems():
        for item1, item2 in itertools.combinations(value, 2):
            Check = checkOverlap(item1, item2)
            if Check == True:
                Nooverlap.append(item1)
                Nooverlap.append(item2)
            elif Check == False:
                Overlap.append(item1)
                Overlap.append(item2)
    
    #New Rule - tuples and map and sets are king. Sped this code up SO much
    FinalNoOver = []
    Intersection  = set(map(tuple,Overlap)) & set(map(tuple,Nooverlap))

    TupalizeNoOverlaps = set(map(tuple,Nooverlap))
    for item in TupalizeNoOverlaps:
        if item not in Intersection:
            FinalNoOver.append(list(item))

    for item in FinalNoOver:
        print item
    return FinalNoOver


def GetFlankingRegions1000(ListofNonOverlappingGenes):
    """
    We need to add 1000 bp on the side of each gene and then again check for overlp. This can help create a better training set. SO we're gonna try it. It's important to keep in mind that for this set we aren't interested in getting the largest set possible, but rather the best set to trian augustus on
    """
    CopyList = []
    
    for item in ListofNonOverlappingGenes:
        Start = item[3]
        End = item[4]
        NewStarts = int(Start) - 1000
        NewEnd = int(End) + 1000
        item[3] = NewStarts
        item[4] = NewEnd
        CopyList.append(item)
    
    return CopyList


def GetFlankingRegions5000(ListofNonOverlappingGenes):
    """
    We need to add 1000 bp on the side of each gene and then again check for overlp. This can help create a better training set. SO we're gonna try it. It's important to keep in mind that for this set we aren't interested in getting the largest set possible, but rather the best set to trian augustus on
    """
    CopyList = []
    
    for item in ListofNonOverlappingGenes:
        Start = item[3]
        End = item[4]
        NewStarts = int(Start) - 5000
        NewEnd = int(End) + 5000
        item[3] = NewStarts
        item[4] = NewEnd
        CopyList.append(item)
    
    return CopyList

def IsolateUniqGff3s(FinalListofFlanks, GFF3Groups, FileToWrite, BaseName):

    #I could def make this faster - I just need to think how
    
    WriteMeToDoom = str(BaseName) + '_' + str(FileToWrite)
    try:
        os.remove(WriteMeToDoom)
    except OSError :
        pass

    with open(WriteMeToDoom, 'a') as f: 
        for finalgenename in FinalListofFlanks:
            for Gffs in GFF3Groups:
                if finalgenename[8] in Gffs[0]:
                    for hit in Gffs:
                        Formated  = '\t'.join(hit)
                        f.write(Formated)
                        f.write('\n')
                    f.write('\n')


def Usage():
    print "\n Application %s [options] -s <ConsvSeqfile> -g <Gff3File>  -o <OutPutBaseName> \n" \
        "-s     Conserved Seq file with header matching Gff3     \n" \
        "-g     Gff3 output genome file from PASA output  \n" \
        "-o     The output file you are going to write to. DO NOT INCLUDE.ending. All FILES will end with a ,out \n" % (sys.argv[0])

def Main():

    global oflag
    Sflag = None
    Gflag = None
    Oflag = None

    try:
        options, other_args = getopt.getopt(sys.argv[1:], "s:g:h:o:", ["help"])

    except getopt.GetoptError:
        print "There was a command parsing error"
        Usage()
        sys.exit(1)

    for option, value in options:
        if option == "-s":
            Sflag = value
        elif option == "-g":
            Gflag = value
        elif option == "-o":
            Oflag = value
        elif option == "--help":
            Usage()
        else:
            print "Unhandeled options %s %s" % (options)

    if Sflag == None:
        print "Need a Conserved Seq inpint with FASTA headers matching Gff3"
        Usage()
        exit(-1)
    elif Gflag == None:
        print "Need a GFF3 output file from PAA Pipeline"
        Usage()
        exit(-1)
    elif Oflag == None:
        print "Need output"
        Usage()
        exit(-1)



    Headers = GetHeaderFromConsvd(Sflag)
    Gff3Assmbls  = GroupGff3(Gflag)
    GoodGff3s = FindGoodGroups(Gff3Assmbls,Headers)
    DictOfHits = CreateDictSingleLocations(GoodGff3s)
    print "Removing Overlap Seq 1"
    print "This could take some time"
    NonOverlapGenes = RemoveOver(DictOfHits)
    print "Writing NonFlankers to File"
    IsolateUniqGff3s(NonOverlapGenes, GoodGff3s, 'ConservedSeqNoFlanking.gff3', Oflag)

    print "Create Flanking 1k set"
    AddFlankingRegions = GetFlankingRegions1000(NonOverlapGenes)
    DictofFlanks = CreateDict(AddFlankingRegions)

    print "Removing Overlap Seq 2"
    print "This could take some time"
    RemoveOverlapFromFlank = RemoveOver(DictofFlanks)
    print "Writing 1k indvidualts to file"
    IsolateUniqGff3s(RemoveOverlapFromFlank, GoodGff3s, '1kFlankingGroups.gff3', Oflag)


    Add5kFlank =  GetFlankingRegions5000(NonOverlapGenes)
    Dictof5kFlanks = CreateDict(Add5kFlank)
    print "Removing Overlap Seq 3"
    print "This could take some time"

    RemoveOverlap5k = RemoveOver(Dictof5kFlanks)
    IsolateUniqGff3s(RemoveOverlap5k, GoodGff3s, '5kFlankingGroups.gff3', Oflag)





if __name__ == '__main__':
    Main()

