import argparse
import pickle
from scipy.integrate import quad as integrate


def optimal_param(
    threshold: float,
    num_perm: int,
    false_positive_weight: float = 0.5,
    false_negative_weight: float = 0.5,
):
    """
    Compute the optimal `MinHashLSH` parameter that minimizes the weighted sum
    of probabilities of false positive and false negative, taken from datasketch.

    Parameters
    ----------
    threshold : float
        The threshold for similarity.
    num_perm : int
        The number of permutations.
    false_positive_weight : float
        The weight of false positive.
    false_negative_weight : float
        The weight of false negative.

    Returns
    -------
    Tuple[int, int]
        The optimal `b` and `r` parameters.
    """

    def false_positive_probability(threshold: float, b: int, r: int):
        """Source: `datasketch.lsh`"""

        def proba(s):
            return 1 - (1 - s ** float(r)) ** float(b)

        a, _ = integrate(proba, 0.0, threshold)
        return a

    def false_negative_probability(threshold: float, b: int, r: int):
        """Source: `datasketch.lsh`"""

        def proba(s):
            return 1 - (1 - (1 - s ** float(r)) ** float(b))

        a, _ = integrate(proba, threshold, 1.0)
        return a

    min_error = float("inf")
    opt = (0, 0)
    for b in range(1, num_perm + 1):
        max_r = int(num_perm / b)
        for r in range(1, max_r + 1):
            fp = false_positive_probability(threshold, b, r)
            fn = false_negative_probability(threshold, b, r)
            error = fp * false_positive_weight + fn * false_negative_weight
            if error < min_error:
                min_error = error
                opt = (b, r)
    return opt


def main(args):
    num_of_tables, num_of_hash_functions = optimal_param(args.threshold, args.num_perm)
    HASH_RANGES = [(i * num_of_hash_functions, (i + 1) * num_of_hash_functions) for i in range(num_of_tables)]
    with open("hsl_hash_ranges.pkl", "wb") as fd:
        pickle.dump(HASH_RANGES, fd)

if __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('ngram_size', default=5, help="The ngram size to use for MinHash")
    parser.add_argument('num_perm', default=256, help="Number of permutations")
    parser.add_argument('threshold', default=0.7, help="Minhash threshold")
    parser.add_argument('jobid', default=0, help="uniquejobid")
    args = parser.parse_args()
    main(args)