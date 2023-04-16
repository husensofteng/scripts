import argparse
import sys
from Bio import SeqIO
from random import sample


def parse_commandline_args():
    """
    read command line arguments or set the default values
    """
    parser = argparse.ArgumentParser(description='Generate n random sequences from a fasta file')
    parser.add_argument('-n', '--number_seqs', help= "Number of sequences to extract (without repeat)", required=True, type=int)
    parser.add_argument('-fi', '--input_fasta', help= "path to input fasta file (not compressed)", required=True)
    parser.add_argument('-fo', '--output_fasta', help= "path to output fasta file", required=True)

    return parser.parse_args(sys.argv[1:])

args = parse_commandline_args()


def get_rand_seqs():
    with open(args.input_fasta, 'r') as f, open(args.output_fasta, 'w') as of:
        seqs = SeqIO.parse(f, "fasta")
        samps = ((seq.name, seq.seq) for seq in  sample(list(seqs), args.number_seqs))
        samps
        for n, samp in enumerate(samps):
            of.write(">{}\n{}\n".format(*samp))
        print('wrote {} to {}'.format(n+1, args.output_fasta))

if __name__ == '__main__':

    get_rand_seqs()
