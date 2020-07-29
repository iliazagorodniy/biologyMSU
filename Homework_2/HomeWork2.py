def frame_codon_count(dna):
    dna_list = list(dna)
    dna_leng = len(dna)
    codons_list = []
    uniq_codons_list = []
    codons_dict = {}
    for index in range(0, dna_leng // 3):
        codon_index = index*3
        codon = ''.join(dna_list[codon_index:codon_index+3])
        codons_list.append(codon)
        if (not codon in uniq_codons_list):
            uniq_codons_list.append(codon)
        for uniq_codon in uniq_codons_list:
            codons_dict[uniq_codon] = codons_list.count(uniq_codon)

    return codons_dict

print(frame_codon_count('AGGGATTGCTTAAGG'))
