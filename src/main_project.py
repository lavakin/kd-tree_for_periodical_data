import numpy as np
import time
import settings
import angle_operations
from sklearn.neighbors import KDTree


def modify_input(vector):  # modifies angles, that are not in the range (range given by the median)
    non_periodical = vector[len(vector) - 2:]
    non_periodical = np.array([x*32 for x in non_periodical]) #*32 to normalize the data and find the neighbours correctly
    periodical = vector[0:len(vector) - 2]  # modifying just periodical ones
    for i in range(0, len(periodical)):
        periodical[i] = angle_operations.angle_in_the_range(periodical[i], Loaded.Medians[i])
    vector = np.concatenate((np.array(periodical), non_periodical),axis=0) # append the nonperiodical
    return vector


# output of the tree is indexes of the data array. This method converts the valid ones to data arrays
def from_tree_outputs_to_valid_vectors(array_of_indexes,
                                       data, i):  # output is [[]] (array of neighbours for each of our data)
    neighbours = []
    for index in array_of_indexes:
        neighbours.append(np.array(data[index]).tolist())
    return neighbours


# the tree returns the indexes of the modified data. This method maps them to the indexes of the original data set
def to_original_indexes(array_of_indexes):
    print(array_of_indexes)
    new_indexes = [Loaded.indexes[index] for index in array_of_indexes]
    TreeOutputs.original_indx = new_indexes  # needed for the TreeOutputs object
    return new_indexes


def make_list_of_tree_outputs(tree_output, distance):
    i = 0
    list_of_obj = []
    for neighbours_of_one_vector in tree_output:
        obj = TreeOutputs(neighbours_of_one_vector, i, distance)
        i += 1
        list_of_obj.append(obj)
    return list_of_obj


def get_neighbours(data):
    data = [modify_input(item) for item in data]  # modified input data
    list_of_tree_outputs_objects = make_list_of_tree_outputs(
        tree.query(data, k=settings.number_of_matches, return_distance=False),
        tree.query(data, k=settings.number_of_matches, return_distance=True)[0])
    return list_of_tree_outputs_objects


# all informations about the tree output
class TreeOutputs:
    original_indx = []

    def __init__(self, indexes, i, distances):
        print(indexes)
        self.indexes = indexes
        self.original_indexes = np.array(to_original_indexes(indexes))
        self.distance = np.array(from_tree_outputs_to_valid_vectors(indexes, Loaded.cloned_data, i))
        self.original_distance = np.array(
            from_tree_outputs_to_valid_vectors(TreeOutputs.original_indx, Loaded.raw_data, i))
        self.identifiers = np.array([Loaded.Identifiers[index] for index in TreeOutputs.original_indx])
        self.distance = distances


class Loaded:
    cloned_data = np.load('data.npy')
    raw_data = np.load('raw_data.npy')
    indexes = np.load('indexes.npy')
    Medians = np.load('medians.npy')
    Identifiers = np.load('identifiers.npy')


print(len(Loaded.cloned_data))
print(Loaded.raw_data[273])
tree = KDTree(Loaded.cloned_data, metric='euclidean')
#X1 = Loaded.raw_data  #test input data
X1 = [[74.9, 263.2, 222., 73.5, 258.9, 199.3, 81.1, 182., 165.8, 1., 4.48, 4.72]]
list_of_tree_outputs_objects = get_neighbours(X1)  #usage example
i = 0
for object in list_of_tree_outputs_objects:
    print(object.identifiers)
    print(Loaded.Identifiers[i])
    print(object.distance[0][0])
    i+=1

