import csv
import statistics as st
import numpy as np
import pandas as pd
import angle_operations
import settings


def must_be_cloned(median, angle):
    return False if angle_operations.periodic_distance(angle, median) < settings.accepted_range else True


def append_non_periodical(duplicates, non_periodical):
    for duplicate in duplicates:
        for item in non_periodical:
            duplicate.append(float(item))
    return duplicates


def duplicate_each_cell_in_row(row, j):
    global indexes
    global raw_data
    global raw_data_identifiers
    i = 0
    list_of_duplicates = [[]]
    raw_data.append(np.array(row[2:]).astype(float))  # original data used for gaining the original indexing
    raw_data_identifiers.append(row[:2])
    non_periodical = np.array(row[len(row) - 2:]).astype(float)
    non_periodical = [x*32 for x in non_periodical]
    row = np.array(row[2:len(row) - 2]).astype(float)
    for cell in row:
        list_of_cloned_rows, list_of_original_rows, merged_list = [], [], [[]]
        angle_in_range = angle_operations.angle_in_the_range(float(cell), Medians[i])
        for _row in list_of_duplicates:
            merged_list = [[]]  # because just the last version contains all the rows
            if must_be_cloned(Medians[i], angle_in_range):  # clones it if it is further from median, than it should be
                cloned_row = _row.copy()
                cloned_row.append(
                    angle_operations.clone_angle(Medians[i], cell))  # append a cloned version to a row
                list_of_cloned_rows.append(cloned_row)  # append the whole clonedrow
            _row.append(float(cell))  # append an original version to row
            list_of_original_rows.append(_row) # append the whole original row
            merged_list = (merged_list + list_of_original_rows + list_of_cloned_rows)[1:]  # merge al the rows
        list_of_duplicates = merged_list
        i = i + 1
    list_of_duplicates = append_non_periodical(list_of_duplicates, non_periodical)
    for duplicate in list_of_duplicates:
        indexes.append(j)  # for the mapping from cloned indexes to original
    print(j)
    return list_of_duplicates


def get_medians():
    Medians = []
    for header in headers:
        Medians.append(st.median(data[header]))
    return Medians


def get_cloned_data():
    golden = csv.DictReader(open("Golden_NtC_plus_Suites_OCT2019.csv"))
    j = 0
    cloned_data = []
    for row in golden:
        row = [float(row['clustnr']), row['my_id_q'],row['delta'], row['epsilon'], row['zeta'],
             row['alpha'], row['beta'], row['gamma'], row['delta2'], row['chi'],
             row['chi2'], row['NCCN_tors'], row['NN_dist'], row['CC_dist']]
        row_versions = duplicate_each_cell_in_row(row, j)
        cloned_data = (cloned_data + row_versions)  # append the row version to the cloned data
        j += 1
    return np.array(cloned_data)


def save_on_disk():
    np.save('raw_data.npy', raw_data)
    np.save('indexes.npy', indexes)
    np.save('data.npy', cloned_data)
    np.save('medians.npy', Medians)
    np.save('identifiers.npy', raw_data_identifiers)


indexes = []
data = pd.read_csv('Golden_NtC_plus_Suites_OCT2019.csv', header=0,
                   usecols=['delta', 'epsilon', 'zeta', 'alpha', 'beta', 'gamma', 'delta2', 'chi', 'chi2',
                            'NCCN_tors'])  # imports needed data with header

raw_data = []
raw_data_identifiers = []
headers = data.head(0)
Medians = get_medians()
cloned_data = np.array(get_cloned_data())
raw_data = np.array(raw_data)
save_on_disk()
