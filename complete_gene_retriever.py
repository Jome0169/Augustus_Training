# -*- coding: utf-8 -*-
"""
    22.train_augustus.CompleteGeneRetriever
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This is the start of the pipeline used to train Augutus. This pipeline will
    go through and filter a list of theoretical pasa transcripts, and output a
    high quality training set that can then be used in order to train AUGUSTUS
    which can then be used to train maker in genome annotation.

    :copyright: (c) 2018 by Pablo Mendieta
    :license: LICENSE_NAME, see LICENSE for more details.
"""
from datetime import datetime
import argparse
import sys
import os




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




def OnlyComplete(Dict,output):


    try:
        os.remove(output)
        os.remove(output)
    except OSError:
        pass

    for key, value in Dict.iteritems():
        if "complete" in key:
            with open(output, 'a+') as Z:
                formatkey = str(key) +'\n'
                Z.write(formatkey)
                Z.write(value)
                Z.write("\n")
        else:
            pass


def get_parser():
    parser = argparse.ArgumentParser(description='Extracts theorteical complete \
            genes from the PASA output file for further filtering to eventually \
            be used in the AUGUSTUS markov trainign software.')
    parser.add_argument('-f','--fasta', help='fasta file output from PASA', \
            required=True, dest='f')
    parser.add_argument('-o','--output', help='output file to write complete genes to',\
            required=False,dest='o') 

   
if __name__ == "__main__":
    args = get_parser().parse_args()
    StartTime = datetime.now()
    
    print("Reading in Fasta File")
    LoadedFile = LoadProtFiles(args.f)

    print("Writing complete genes into %s file" % args.o)
    OnlyComplete(LoadedFile, args.o)

  
endtime = datetime.now()
finaltime = endtime - StartTime 
print("script is finished running. Please blast output file Vs other well known \
        databases, cat output, and feed that output int\
        strict_gene_isolation.py")
print ("Total Time %s" % (finaltime))

     
