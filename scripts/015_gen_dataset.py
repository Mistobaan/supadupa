import argparse
import os
import random

import pandas as pd
from tqdm import auto as tqdm


def shift_string(s, n):
    # Convert the input string to a list of characters
    s_list = list(s)
    # Shift the list of characters by n
    s_list = s_list[n:] + s_list[:n]
    # Join the list of characters back into a string
    return "".join(s_list)


def generate_doc(n):
    """
    Generate a document of n `tokens` with repetition, shift and random punctuation
    """
    for _ in range(int(n)):
        article = " ".join(
            "%s%d" % (c, i)
            for i in range(10)
            for c in ("ABC" + random.choice(["", "", "", "", "", ".", ","]).strip())
        )
        yield shift_string(article, random.choice(range(10)))


def main(name, n, m, output):
    all_documents = []

    n_docs = random.choice(range(1, m + 1))
    for idx in tqdm(range(n_docs), desc="documents.."):
        n_rows = random.choice(range(1, n + 1))
        rows = list(generate_doc(n_rows))
        df = pd.DataFrame({"text": rows, "idx": range(1, len(rows) + 1)})
        all_documents.append(df)
    output_folder = os.path.join(output, name)
    os.makedirs(output_folder, exist_ok=True)
    pd.concat(all_documents).to_parquet(
        os.path.join(output_folder, name + ".parquet"),
        partition_cols=["idx"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="the name of the dataset")
    parser.add_argument(
        "n", help="max number of lines to generate per document", type=int, default=1
    )
    parser.add_argument(
        "m", help="max number of documents to generate per dataset", type=int, default=1
    )
    parser.add_argument("output", help="directory to store the generated dataset")
    args = parser.parse_args()
    main(args.name, args.n, args.m, args.output)
