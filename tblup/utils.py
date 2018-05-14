import random
import numpy as np


def make_grm(geno):
    """
    Make the genomic relationship matrix.
    - Expects rows as individuals and columns as markers.
    :param geno: np.ndarray, 2D, genotype marker matrix. (N x P)
    :return: np.ndarray, 2D, genomic relationship matrix. (N X N)
    """
    p = np.mean(geno, axis=0) / 2  # Row means over 2.
    P = 2 * (p - 0.5)
    W = (geno - 1) - P  # Subtract P from each column of G, where G is put into {-1, 0, 1} format from {0, 1, 2}.
    WtW = np.matmul(W, np.transpose(W))
    return WtW / (2 * np.sum(p * (1 - p)))


def exclusive_randrange(begin, end, exclude):
    """
    Get a random integer in a range [begin, end), excluding a particular number.
    :param begin: int, beginning of range.
    :param end: int, end of range.
    :param exclude: int, exclude this from the range.
    :return: int, random number != exclude
    """
    r = random.randrange(begin, end)
    while r == exclude:
        r = random.randrange(begin, end)
    return r


def build_kwargs(args):
    """
    Builds the arguements for a tblup.Population object as keyword arguments.
    :param args: object, argparse arguments.
    :return: dict, kwargs
    """
    return {}