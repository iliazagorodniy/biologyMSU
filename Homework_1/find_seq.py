def find_seq(where_to_search, what_to_search='A'):
    nuc_sec_1 = where_to_search.upper()
    nuc_sec_2 = what_to_search.upper()

    return nuc_sec_1.count(nuc_sec_2)


test_1 = find_seq('ACGCACTAACC', 'AC')
test_2 = find_seq('AcGCaCTaACC', 'ac')
test_3 = find_seq('ACGCACTAACC')


print(test_1)
print(test_2)
print(test_3)
