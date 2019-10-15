
def trypsin_digestion(proseq_incl_stop, miss_cleavage):
    """digest peptides using the tryptic rule, allowing for miss cleavages
    @params:
        proseq_incl_stop (str): full protein sequence to be digested
        miss_cleavage (int): number of allowed missed cleavages
    @return:
        list: tryptic peptides 
    """
    
    all_peptides = []
    for protseq in proseq_incl_stop.split('*'):
        if len(protseq)<=0:
            continue
        peptides = []
        peptide = ''
        "remove the first K/R if in the begining of a reading frame"
        protseq_updated = protseq[0::]
        if protseq[0]=='K' or protseq[0]=='R' and len(protseq)>1:
            protseq_updated = protseq[1::]
        
        for c, aa in enumerate(protseq_updated):
            peptide += aa
            next_aa = ''
            try:
                next_aa = protseq_updated[c + 1]
            except IndexError:
                pass
    
            if aa in ['K', 'R'] and next_aa != 'P':  # for trypsin peptides
                if len(peptide) > 0:
                    peptides.append(peptide)
                peptide = ''
                continue
        
        if len(peptide) > 0:
            peptides.append(peptide)
        
        peptides_with_miss_cleavage = []
        for i in range(1, miss_cleavage + 1):
            for j, pep in enumerate(peptides):
                if j + i < len(peptides):
                    peptide = ''.join([x for x in (peptides[j:j + i + 1])])
                    peptides_with_miss_cleavage.append(peptide)
        
        peptides.extend(peptides_with_miss_cleavage)
        all_peptides.extend(peptides)
        
    return all_peptides
