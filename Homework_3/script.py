class DNA:
    basecomplement = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C'}

    def __init__(self, string):
        self.sequence = string.upper()
        self.name = 'my DNA Sequence'

    def to_rna(self):
        return self.sequence.replace('T', 'U')

    def reverse(self):
        letters = list(self.sequence)
        letters.reverse()
        return ''.join(letters)

    def complement(self):
        letters = list(self.sequence)
        letters = [self.basecomplement[base] for base in letters]
        return ''.join(letters)

    def write_file(self, fasta):
        f = open(fasta, 'w')
        f.write('> ' + self.name + '\n')
        f.write(self.sequence)
        f.close()

    def read_file(self, fasta):
        f = open(fasta, 'r')
        lines = f.readlines()
        self.name = lines[0].strip('>\n ')
        self.sequence = lines[1].split('\n')[0]
        f.close()

    def gc(self):
        s = self.sequence
        gc = s.count('G') + s.count('C')
        return gc * 100.0 / len(s)


file = open('./hw3.fasta', 'r')
file_lines = file.readlines()
length = len(file_lines)

seq_list = []
for i in range(0, length, 2):
    seq_list.append(DNA(file_lines[i+1].split('\n')[0]))
    seq_list[i // 2].name = file_lines[i].strip('>\n ')

for obj in seq_list:
    print('Sequence name: ' + obj.name)
    print('Sequence value: ' + obj.sequence)
    print('')


GC_percentage = [obj.gc() for obj in seq_list]

print(GC_percentage)