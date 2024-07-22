import os, sys
from glob import glob
import argparse

#thresholds
min_prot_len = 100
min_identity = 90

#variables
query_prot_id_index = 0 
ref_prot_id_index = 1
identity_index = 2
prot_query_start = 6
prot_query_end = 7


def parse_commandline_args():
    """
    read command line arguments or set the default values
    """
    parser = argparse.ArgumentParser(description='Process Diamond output')
    parser.add_argument('-p', '--protein_files_in', help= "tab-separated file containing list of samples and their matching protein file", required=True, type=int)
    parser.add_argument('-d', '--uniref_prot_headers_file', help= "path to Uniref database", required=True)
    parser.add_argument('-o', '--out_dir', help= "output directory", required=True)

    return parser.parse_args(sys.argv[1:])

args = parse_commandline_args()


def get_prot_name_from_uniref(uniref_prot_headers_file):
    print('Generating protein_taxa dict')
    uniref_protID_protName_taxa = {}        
    with open(uniref_prot_headers_file, 'r') as uniref_headers:

        l = uniref_headers.readline().strip('\n').strip('>')
        'e.g.: UniRef90_A0A6P8R4F2 Titin isoform X8 n=1 Tax=Geotrypetes seraphini TaxID=260995 RepID=A0A6P8R4F2_GEOSA'
        i = 1
        while len(l)>3:
            prot_id = l.split(' ')[0].replace('UniRef90_','')
            prot_name = ' '.join(l.split('=')[0].split(' ')[1:-1])
            prot_taxa = ' '.join(l.split('=')[2].split(' ')[0:-1])

            uniref_protID_protName_taxa[prot_id] = prot_name+"\t"+prot_taxa

            l = uniref_headers.readline().strip('\n').strip('>')
            i+=1
            if i % 10000000 == 0:
               print('processed', i)
    return uniref_protID_protName_taxa

prots_info = get_prot_name_from_uniref(args.uniref_prot_headers_file)


samples_proteins = {}

protein_files = [l.strip('\n').split('\t') for l in open(args.protein_files_in, 'r')]


for protein_file in protein_files:
    
    print('Processing {}'.format(protein_file))

    sample = protein_file[0]
    file_path = protein_file[1]
    if sample not in samples_proteins:
        samples_proteins[sample] = {}
    
    with open(file_path, 'r') as proteins:
        
        for l in proteins.readlines():

            sl = l.strip('\n').split('\t')
            if float(sl[identity_index]) < min_identity or (int(sl[prot_query_end])-int(sl[prot_query_start])) < min_prot_len:
                continue
            
            try:
                if samples_proteins[sample][sl[query_prot_id_index].replace('UniRef90_', '')][identity_index] < sl[identity_index]:
                    samples_proteins[sample][sl[query_prot_id_index].replace('UniRef90_', '')] = sl
            except KeyError:
                samples_proteins[sample][sl[query_prot_id_index].replace('UniRef90_', '')] = sl

    print('Processed #{}'.format(len(samples_proteins[sample].keys())))

for sample in samples_proteins.keys():
    
    print('Processing {}'.format(sample))

    with open(args.out_dir + '/' + sample + "_dimond_filtered.tsv", 'w') as sample_out:
        for query_prot, info in samples_proteins[sample].items():
            try:
                ref_prot_name_taxa = prots_info[info[ref_prot_id_index].replace('UniRef90_', '')]
                sample_out.write('{}\t{}\n'.format(ref_prot_name_taxa, '\t'.join(info)))
            except KeyError:
                print('No ref protein ID {} is found'.format(info[ref_prot_id_index].replace('UniRef90_', '')))
            

print("Finished processing {} samples".format(len(samples_proteins.keys())))   
