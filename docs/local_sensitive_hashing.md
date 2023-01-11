# Locality-Sensitive Hashing

In Locality-Sensitive Hashing (LSH), the idea is to hash similar items to the same "bucket" with high probability.

- To increase the chances of this happening, multiple hash tables are used.
- Each table uses a different hash function, and when an item is hashed, it is hashed to each of the tables using the corresponding hash function.

- The parameter b in the false_positive_probability function represents the number of hash tables used.

- The larger the value of b, the more hash tables are used, and the higher the probability that similar items will be hashed to the same bucket in at least one of the tables.

- This means that using a larger value of b will increase the chances of correctly identifying similar items, but it will also increase the number of hash tables needed to be searched, which can increase the running time.

- It is worth noting that it is a trade-off between recall and precision when it comes to the number of hash tables.

- In general, more hash tables would increase the recall but decrease the precision of the search and the other way around.

 How to determine the B, R optimal params given a
SIMILARITY threshold and a number of permutations

This code defines a function false_positive_probability(threshold: float, b: int, r: int) that calculates the probability of a false positive in the context of Locality-Sensitive Hashing (LSH).

This function takes in three arguments:

- threshold is a float representing a similarity threshold
- b is an integer representing the number of hash tables used
- r is an integer representing the number of hash functions per table

It uses an inner function proba(s) which calculates the probability that any two items that are similar to each other by at least s will be hashed to the same bucket. The inner function returns a probability value, and this probability is used in the outer function.

The outer function then use integrate function which is not provided here and calculates the area under the curve of this probability function between 0.0 and the given threshold and returns the result as the probability of false positive.

This code is based on datasketch library, The datasketch library provides a variety of algorithms for performing approximate nearest neighbor search in high-dimensional spaces, including LSH.

## Aggregation

A Union-find data structure is an algorithm that keeps track of a set of elements partitioned into a number of disjoint (non-overlapping) subsets. The Union-find algorithm is used to keep track of which elements are in the same subset and quickly perform union and find operations on these subsets.

In the provided code, the UnionFind class is used to keep track of subsets of integers, which are represented by instances of the UnionFind class. The class has three methods:

The __init__() method creates an empty dictionary named parent which is used to store the parent-child relationship of the elements in the subsets.

The find(x) method takes an integer x as an input and returns the unique identifier of the subset which element x belongs to. This is done by following the chain of parent pointers up the tree until the parent pointer of x points to itself, which indicates that x is the root element of its subset.

The union(x, y) method takes two integers x and y as input and unite two subsets which the element x and y respectively belong to. The method performs find on x and y to find the unique identifier of the subsets, and then set the root of the smaller set to point to the root of the larger set, effectively merging the two subsets into one.

The parent dictionary is used to store the parent-child relationship of the elements in the subsets, and the find and union method use this dictionary to keep track of which elements are in the same subset and perform union and find operations on these subsets. The parent is an important part of Union-find data structure, it is used to maintain the disjoint sets of element in memory, to perform the union operation and find operation efficiently.
