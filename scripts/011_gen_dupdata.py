import argparse
import random
import sys


def shift_string(s, n):
    # Convert the input string to a list of characters
    s_list = list(s)
    # Shift the list of characters by n
    s_list = s_list[n:] + s_list[:n]
    # Join the list of characters back into a string
    return "".join(s_list)


def main(n, out):
    """
    Generate a file with duplicate data.
    """
    for _ in range(int(n)):
        article = " ".join(
            "%s%d" % (c, i)
            for i in range(10)
            for c in ("ABC" + random.choice(["", "", "", "", "", ".", ","]).strip())
        )
        line = shift_string(article, random.choice(range(10)))
        out.write(line + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="number of lines to generate")
    args = parser.parse_args()
    n = args.n
    main(n, out=sys.stdout)
