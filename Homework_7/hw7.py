from Bio.Align import AlignInfo
from Bio import Entrez
from Bio import AlignIO  # module to work with the alignments
import matplotlib.pyplot as plt
import numpy as np
from Bio.Blast import NCBIWWW  # interface to blast
from Bio.Blast import NCBIXML  # parser of XML files
from Bio.Align.Applications import MuscleCommandline

# All the functions that send requests to the NCBI Entrez API will automatically
# respect the NCBI rate limit (of 3 requests per second without an API key,
# or 10 requests per second with an API key).
#
Entrez.email = "orekhov@mail.bio.msu.ru"
Entrez.api_key = '9fd2838e72a1e3a3a1456e8d278f7476ed08'
#
# publications = []  # here we’ll store number of publications per year

# for i in range(1960, 2018, 2):
#     term = "Ebola AND " + str(i) + "[Publication Date]"
#     handle = Entrez.esearch(db="pubmed", term=term)
#     record = Entrez.read(handle)
#     publications.append(int(record["Count"]))
#
# plt.figure(figsize=(5, 7))
# plt.plot(range(1960, 2018, 2), publications, lw=1, marker='o', ms=3)
# plt.savefig('ebola.png')
# plt.show()

# First, we'll retrieve a protein sequence from the protein DB by its NCBI GI id
query_gi = "4501969"  # NCBI GI id of a sequence

handle = Entrez.efetch(db="protein", id=query_gi, retmode="xml")
records = Entrez.read(handle)
query_seq = str(records[0]["GBSeq_sequence"]).upper()
print("Protein accession id: ", records[0]["GBSeq_primary-accession"])
print("Protein name: ", records[0]["GBSeq_definition"])
print("Protein sequece: ", query_seq)

# Now, we'll perform a blast search for other sequences
# which are homologous to the obtained above sequence of
# human beta-2 adrenergic receptor
# Here, we'll seach for a homolog from Bos taurus (Cow)
result_handle = NCBIWWW.qblast("blastp", "swissprot", query_seq, hitlist_size=1, entrez_query="Bos taurus[orgn]")
# ...and write the result to .xml file
blast_result = open("Bovine_seq.xml", "w")
blast_result.write(result_handle.read())
blast_result.close()
# now we can read this file at any time and get the sequence, its id, etc.
print(
    NCBIXML.read(open("Bovine_seq.xml")).alignments[0].__str__())  # returns formated string with this alignment details
print('Seq ID: ', NCBIXML.read(open("Bovine_seq.xml")).alignments[0].hit_id.split("|")[1])
# getting the sequence of an HSP (high scoring segment pair)
print('Protein sequence: ', NCBIXML.read(open("Bovine_seq.xml")).alignments[0].hsps[0].sbjct)

# This loop reads the species list specified in the species.txt file and print the Entrez queries
with open("./data/species.txt", 'r') as species:
    species_lines = species.readlines()
    for line in species_lines:
        species_latin = line.split(".")[0].strip()
        species_common = line.split(".")[1].strip()
        entrez_q = str(species_latin + "[orgn]")
        print(species_common, ': ', entrez_q)
#
with open("species.fasta", 'w') as fasta_out:  # we’ll write the results here
    with open("./data/species.txt", 'r') as species:  # list of species
        species_lines = species.readlines()
        for line in species_lines:
            species_latin = line.split(".")[0].strip()
            species_common = line.split(".")[1].strip()
            entrez_q = str(species_latin + "[orgn]")
            # try the following code, if it’ll generate an error, go to except:
            try:
                # result_handle = NCBIWWW.qblast("blastp", "nr", query_seq, hitlist_size=1, entrez_query=entrez_q)
                # blast_result = open(species_common + "_seq.xml", "w")
                # blast_result.write(result_handle.read())
                # blast_result.close()
                gi = str(NCBIXML.read(open("./data/" + species_common + "_seq.xml")).alignments[
                             0].hit_id.split("|")[1])
                seq = str(
                    NCBIXML.read(open("./data/" + species_common + "_seq.xml")).alignments[0].hsps[
                        0].sbjct)
                fasta_out.write('>' + gi + '|' + species_common + '\n' + seq.upper() + '\n')
                print(species_common + ' is ready.')
                # time.sleep(5) # wait for a few seconds (otherwise, you can be banned)
            # do in case of an error
            except:
                print('Problem with ', species_common)

# cline = MuscleCommandline(cmd="./muscle3.8.31_i86win32", input="species.fasta", out="muscle.clw", clw=True)
# cline()


alignment = AlignIO.read("./data/muscle.clw", "clustal")
# we will be using just a part of the alignment to build the phylogenetic tree
# this command writes a file in a fromat suitable for Phyml (software for molecular phylogeny)
AlignIO.write(alignment[:, 60:300], "phyml.phy", "phylip-relaxed")

# Some general alignment analysis tools are available in module Bio.Align as AlignInfo

summary_align = AlignInfo.SummaryInfo(alignment)
consensus = summary_align.gap_consensus()
print(consensus)
#
# if we have phyml locally, we can run it with this code
# otherwise, we can run it online http://atgc.lirmm.fr/phyml
from Bio.Phylo.Applications import PhymlCommandline

cmdline = PhymlCommandline(input='phyml.phy', datatype='aa', model='LG', alpha='e', bootstrap=100)

# module for delaing phylogenetic trees
from Bio import Phylo

# loading file into an object “tree”
tree = Phylo.read("./data/phyml_phy_phyml_tree.txt", "newick")
# text visualization
Phylo.draw_ascii(tree)
#
# matplotlib visualization
# get_ipython().magic('matplotlib notebook')
Phylo.draw(tree)
plt.show(block=True)
