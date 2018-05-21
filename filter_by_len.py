import getopt
import os
from sys import argv
import argparse



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




def quick_filter(filter1, filter2, dict_to_parse):
    final_dict = {}
    for key, value in dict_to_parse.iteritems():
        if len(value) >= int(filter1) and len(value) <= int(filter2):
            final_dict[key] = value
        else:
            pass
    return final_dict


def output_writer(output, dict_to_parse):

    try:
        os.remove(output)
    except OSError:
        pass

    with open(output, 'a') as f:
        for key, value in dict_to_parse.iteritems():
            if value[-1] != '*':
                pass
            else:
                print(len(value) * 3)
                f.write(key)
                f.write('\n')
                f.write(value)
                f.write('\n')




def get_parser():
    parser = argparse.ArgumentParser(description='Software to read in fasta \
            file and do basic functionality that is often required  ')
    parser.add_argument('-i','--input', help='fasta file to read', \
            required=True, dest='i')
    parser.add_argument('-f1','--filter1', help='shorter than this will be filtered',\
            required=False,dest='f1') 
    parser.add_argument('-f2','--filter2', help='longer than this will be filtered',\
            required=False,dest='f2') 
    parser.add_argument('-o','--output', help='output name',\
            required=False,dest='o') 
    args = vars(parser.parse_args())    

    return parser




if __name__ == "__main__":
    args = get_parser().parse_args()

    read_fasta = LoadProtFiles(args.i)
    filtered_list = quick_filter(args.f1, args.f2, read_fasta)

    output_writer(args.o, filtered_list)
    
