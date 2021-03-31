# KD tree for periodical data
Project made for a [conformer research](https://blackbox.ibt.biocev.org/devel/conformers_cif.php?cifcode=1hmh) for Institute of Biotechnology of the Czech Academy of Sciences.

The implementation enables a fast search of nearest neighbours for a dataset of vectors of degrees. Preparation of the data is computationally demanding, but is necessary only when the dataset is modified. Building the tree and searching in it is fast.

## Data preparation
Two versions are created for each index. This would theoretically result in 2^len(vect) more data, but throught a effective heuristic only 8 times more vectors was created, for a vector of 10 angles. Although this is rather a question of space. Because of the logarithmicity of the tree and the fact that we could have also stored the tree on the disc. 
