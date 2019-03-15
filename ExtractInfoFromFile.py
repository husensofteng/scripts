'''
Created on 15 Mar 2019

@author: husen.umer
'''
import argparse
import sys

def parse_commandline_args():
    """
    read command line arguments or set the default values
    """
    parser = argparse.ArgumentParser(description='Get colums from the second file for the first file')
    parser.add_argument('-f1', help= "the file that lacks the ID column", required=True)
    parser.add_argument('-f2', help= "the file that has the ID column", required=True)
    parser.add_argument('-fo', help= "output file name", default = 'outputfile.tsv')
    parser.add_argument('-sep', help= "split character", default = '\t')
    parser.add_argument('--cols_f1', default = '0,1,2,3', 
                        help= "index of columns to consider to match from file 1. For example to consider chromsome and position write 0,1")
    parser.add_argument('--cols_f2', default = '0,1,2,3', 
                        help= "index of columns to consider to match from file 1, it should have the same number of columns as cols_f1")
    parser.add_argument('--cols_to_extract_from_f2', default ='4', help= "index of the columns to be extracted from file 2 and added to the matches in file1, to just get id from the second file write 2")
    
    return parser.parse_args(sys.argv[1:])
    
args = parse_commandline_args()

def read_file2():
    """
    reads f2 and stores the desired columns for each rowin a dictionary where the seach columns are the keys
    """
    sep = args.sep
    dict_f2 = {}
    with open(args.f2, 'r') as f2:
        for l in f2.readlines():
            if l.startswith('#'):
                continue
            sl = l.strip().split(sep)
            try:
                search_cols = '#'.join([sl[int(x)] for x in args.cols_f2.split(',')])
                dict_f2[search_cols]  = [sl[int(x)] for x in args.cols_to_extract_from_f2.split(',')]
            except IndexError:
                print("more columns are given for (cols_f2) or (cols_to_extract_from_f2 parameters) than what exists on line {line}.".format(line=l))
                sys.exit()
    print("{} lines are read into memory from {}.", len(dict_f2), args.f2)
    return dict_f2
    
def add_cols_to_f1(dict_f2):
    """
    read f1 line by line and retreives the required cols from dict_f2
    it write the original cols from f1 followed by the desired cols from f2
    if the search cols where not found in dict_f2, it writes NA to the output file
    """
    sep = args.sep
    with open(args.f1, 'r') as f1, open(args.fo, 'w') as fo:
        for l in f1.readlines():
            if l.startswith('#'):
                fo.write(l)
                continue
            sl = l.strip().split(sep)
            try:
                search_cols = '#'.join([sl[int(x)] for x in args.cols_f1.split(',')])
            except IndexError:
                print("more columns are given for (cols_f1) than what exists on line {line}.".format(line=l))
                sys.exit()
            try:
                cols_from_f2 = dict_f2[search_cols]
            except KeyError:
                cols_from_f2 = ['NA' for i in range(0, len(args.cols_to_extract_from_f2.split(',')))]
            
            fo.write(l.strip() + sep + sep.join(cols_from_f2)+ '\n')
    del dict_f2
           
if __name__ == '__main__':
    #convert f2 input file (the file to get info from) into a dictionary 
    dict_f2 = read_file2()
    #get the desired columns for f1 from the dictionary
    add_cols_to_f1(dict_f2)
    
    