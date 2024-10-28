# This code is part of Mthree.
#
# (C) Copyright IBM 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""Test bit-array generators"""
import itertools
import numpy as np

from mthree.generators import HadamardGenerator


def test_hadamard1():
    """Test Hadamard generator does even pairwise sampling up to 100 qubit strings"""
    for integer in range(2, 101):
        G = HadamardGenerator(integer)
        pairwise_dict = {}
        for arr in G:
            for item in itertools.combinations(range(G.num_qubits), 2):
                pair = str(arr[item[0]]) + str(arr[item[1]])
                if item not in pairwise_dict:
                    pairwise_dict[item] = {}
                if pair in pairwise_dict[item]:
                    pairwise_dict[item][pair] += 1
                else:
                    pairwise_dict[item][pair] = 1

        for idx, pair in enumerate(pairwise_dict):
            assert len(pairwise_dict[pair]) == 4
            assert len(set(pairwise_dict[pair].values())) == 1
            if idx == 0:
                pair_count = list(set(pairwise_dict[pair].values()))[0]
            else:
                temp_count = list(set(pairwise_dict[pair].values()))[0]
                assert temp_count == pair_count
