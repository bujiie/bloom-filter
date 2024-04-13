#!/usr/bin/env python3

# generate random database
# calculate bloomfilter
# return matched rows
# compare to full text search (regex)
# calculate how many false positives

# TABLE
# [index, bloomfilter, rawdata]

import mmh3
from math import log, floor
from random import randrange
from sys import argv


BITS_PER_BYTE = 8
num_bytes = 8

values = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

num_of_bits = num_bytes * BITS_PER_BYTE
k = floor((num_of_bits/len(values)) * log(2))

primes = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 27]
# Minimum number of primes should equal number of values
assert len(primes) >= len(values)


def calculate_signature(subject, k=1, bits_set=None):
    bits_set = bits_set if bits_set is not None else []
    if k <= 0:
        return bits_set
    return calculate_signature(subject, k - 1, bits_set + [mmh3.hash(subject, primes[k]) % num_of_bits])


def build_bloom_filter(signature, bits=None):
    bits = bits if bits is not None else [0] * num_of_bits
    for n in signature:
        bits[n] = 1
    return bits


def coalesce_bloom_filters(signatures, bits=None):
    bits = bits if bits is not None else [0] * num_of_bits
    if signatures is None or len(signatures) <= 0:
        return bits
    for n in signatures.pop(0):
        bits[n] = 1
    return coalesce_bloom_filters(signatures, bits)


def match_bloom_filter(subject, entity_bloom_filter):
    bloom_filter = bit_array_to_bin(build_bloom_filter(calculate_signature(subject, k)))
    return bloom_filter & entity_bloom_filter == bloom_filter


def bit_array_to_bin(bits=None):
    return int("".join([str(b) for b in bits]), 2) if bits is not None else 0b0


if __name__ == "__main__":
    rows = []
    with open("database.txt", "w") as fp:
        for i in range(10):
            subjects = set(sorted([values[n] for n in [randrange(9) for _ in range(randrange(1, 9))]]))
            signatures = [calculate_signature(subject, k) for subject in subjects]
            bloom_filter = coalesce_bloom_filters(signatures)
            rows.append((i, bit_array_to_bin(bloom_filter), subjects))
            fp.write("\t".join([str(i), str(bit_array_to_bin(bloom_filter)), ",".join(subjects)]))

    needle = argv[1]
    for row in rows:
        index, entity_bloom_filter, results = row
        if match_bloom_filter(needle, entity_bloom_filter):
            print(f"{index} - {results}")





