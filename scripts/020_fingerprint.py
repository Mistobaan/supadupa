import argparse
import hashlib
import logging
import pickle
import re
import struct
from typing import List

import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

NON_ALPHA = re.compile(r"[^a-zA-Z0-9]")


def do_chunk(doc: str) -> List[str]:
    return NON_ALPHA.split(doc)


def un_chunk(chunks: List[str]) -> str:
    return " ".join(chunks).encode("utf-8")


def np64array(int_array):
    """
    Convert a list of integers to a numpy array of 64-bit unsigned integers
    """
    return np.array(int_array, dtype=np.uint64)


def ngrams(text, n):
    """
    An n-gram is a contiguous sequence of n items

    returns: a list of n-grams
    """
    n -= 1
    return [text[i - n : i + 1] for i in range(len(text))][n:]


def sha1_hash32(data: bytes) -> int:
    """
    Compute hash32 (int) value of a sequence of bytes

    Parameters
    ----------
    data : bytes

    Returns
    -------
    int
    """
    digest = hashlib.sha1(data).digest()
    top4bytes = digest[:4]
    return struct.unpack("<I", top4bytes)[0]


def create_hash_vector(
    document: str,
    ngram_size: int,
) -> np.array:

    # Split the document by non-alphanumeric characters
    chunks = do_chunk(document)

    # Create n-grams from the chunks and join them to create a set of tokens
    unordered_set_of_document_ngrams = {
        un_chunk(ngram) for ngram in ngrams(chunks, ngram_size)
    }

    # Create a hash value for each token in the set using sha1
    doc_hash_vector_np = np64array(
        [sha1_hash32(ngram) for ngram in unordered_set_of_document_ngrams]
    )
    return doc_hash_vector_np


def apply_hash_functions(permutations, doc_hash_vector_np, hashvalues, hashranges):
    # Get permutation parameters
    a, b = permutations
    # SEED = 42
    # MERSENNE_TWISTER_RNG = np.random.RandomState(SEED)
    # Container for the slow Mersenne Twister pseudo-random number generator.
    # Consider using a different BitGenerator with the Generator container instead.
    # TODO: USE NEW RANDOM GENERATION CODE FOR *SPEED*

    MAX_HASH = np.uint64((1 << 32) - 1)
    MERSENNE_PRIME = np.uint64((1 << 61) - 1)

    # Apply permutation to the hash values and take the bitwise AND with MAX_HASH
    permuted_hash_values = np.bitwise_and(
        ((doc_hash_vector_np * np.tile(a, (len(doc_hash_vector_np), 1)).T).T + b)
        % MERSENNE_PRIME,
        MAX_HASH,
    )

    # Take the minimum of the permuted hash values and the original hash values
    hashvalues = np.vstack([permuted_hash_values, hashvalues]).min(axis=0)

    # Create a bytes representation of the hashed values for each range
    hash_set = [
        bytes(hashvalues[start:end].byteswap().data) for start, end in hashranges
    ]
    # return hash_set which is the signature of the document with idx
    return hash_set


def main(lsh_table_spec_filepath):
    with open(lsh_table_spec_filepath, "rb") as fd:
        lsh_table = pickle.load(fd)
    print(lsh_table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lsh_table_spec_path", type=str, default="lsh_table_spec.cpk")
    args = parser.parse_args()
    main(args.lsh_table_spec_path)
