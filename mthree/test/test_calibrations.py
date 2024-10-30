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
# pylint: disable=no-name-in-module
"""Test Calibration class"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeManilaV2 as FakeManila

from mthree.generators._fake import FakeGenerator
from mthree.calibrations import Calibration
from mthree.calibrations.src import calibration_to_m3, calibration_to_texmex


# Qiskit Runtime updated the Fake backends without including that in a release
# note.  A consequence was that that update changed the readout error value on
# Q0 of FakeManilaV2.  This adds that error back to fix the tests.
BACKEND = FakeManila()
_ = BACKEND.properties()
BACKEND._props_dict["qubits"][0][5]["value"] = 0.234


def test_independent_generator_circuits():
    """Test independent generator circuits get remapped correctly"""
    qubits = [0, 4, 2, 1, 3]
    cal = Calibration(BACKEND, qubits, method="independent")
    cal_circuits = cal.calibration_circuits()
    for idx, val in cal.bit_to_physical_mapping.items():
        qc = QuantumCircuit(5, 1)
        qc.measure(val, 0)
        assert qc == cal_circuits[2 * idx]
        qc2 = QuantumCircuit(5, 1)
        qc2.x(val)
        qc2.measure(val, 0)
        assert qc2 == cal_circuits[2 * idx + 1]


def test_hadamard_generator_circuits():
    """Test hadamard generator circuits get remapped correctly"""
    qubits = [4, 0, 1, 3, 2]
    cal = Calibration(BACKEND, qubits, method="balanced")
    cal_circs = cal.calibration_circuits()
    for kk, string in enumerate(cal.generator):
        string = string[::-1]
        qc = QuantumCircuit(5, 5)
        for idx, val in cal.bit_to_physical_mapping.items():
            if string[idx]:
                qc.x(val)
            qc.measure(val, idx)
        assert qc == cal_circs[kk]


def test_texmex_conversion1():
    """Test that texmex calibration conversion works"""
    cals = [{"111": 4, "110": 1}, {"101": 6, "000": 9}, {"000": 10}]
    strings = [
        np.array([0, 0, 1], dtype=np.uint8),
        np.array([0, 0, 1], dtype=np.uint8),
        np.array([1, 1, 1], dtype=np.uint8),
    ]
    gen = FakeGenerator(strings)
    reduced_cals = calibration_to_texmex(cals, gen)
    assert abs(reduced_cals["001"] - 9 / 30) < 1e-6
    assert abs(reduced_cals["100"] - 6 / 30) < 1e-6
    assert abs(reduced_cals["111"] - 11 / 30) < 1e-6
    assert abs(reduced_cals["110"] - 4 / 30) < 1e-6


def test_texmex_conversion2():
    """Test that texmex calibration conversion works 2"""
    cals = [{"1111": 4, "1100": 1}, {"1001": 6, "0001": 9}, {"1000": 10}]
    strings = [
        np.array([1, 1, 0, 0], dtype=np.uint8),
        np.array([0, 0, 0, 0], dtype=np.uint8),
        np.array([0, 1, 1, 1], dtype=np.uint8),
    ]
    gen = FakeGenerator(strings)
    reduced_cals = calibration_to_texmex(cals, gen)
    assert abs(reduced_cals["0011"] - 4 / 30) < 1e-6
    assert abs(reduced_cals["0000"] - 1 / 30) < 1e-6
    assert abs(reduced_cals["1001"] - 6 / 30) < 1e-6
    assert abs(reduced_cals["0001"] - 9 / 30) < 1e-6
    assert abs(reduced_cals["1111"] - 10 / 30) < 1e-6


def test_m3_conversion1():
    """Test that M3 conversion works from IndependentGenerator"""
    cal = Calibration(BACKEND, qubits=range(5), method="independent")
    cal.run(shots=int(1e4))
    assert cal.shots_per_circuit == int(1e4)
    out = calibration_to_m3(cal.calibration_data, cal.generator)
    # This checks that Q0 result is valid since FakeManila qubit 0 is bad readout
    assert abs(out[1] - 0.766) < 0.02


def test_m3_conversion2():
    """Test that M3 conversion works from HadamardGenerator"""
    cal = Calibration(BACKEND, qubits=range(5), method="balanced")
    cal.run(shots=int(1e4))
    assert cal.shots_per_circuit == 2 * int(1e4) / cal.generator.length
    out = calibration_to_m3(cal.calibration_data, cal.generator)
    # This checks that Q0 result is valid since FakeManila qubit 0 is bad readout
    assert abs(out[1] - 0.766) < 0.02


def test_m3_conversion3():
    """Test that M3 conversion for balanced cals works for permuted orderings"""
    for _ in range(5):
        perm = np.random.permutation(range(5))
        target_idx = np.where(perm == 0)[0][0]
        cal = Calibration(BACKEND, qubits=perm)
        cal.run(shots=int(1e4))
        out = cal.to_m3_calibration()
        assert abs(out[2 * target_idx + 1] - 0.766) < 0.02


def test_m3_conversion4():
    """Test that M3 conversion works for permuted and subset orderings"""
    cal = Calibration(BACKEND, qubits=[4, 2, 0])
    cal.run(shots=12345)
    out = calibration_to_m3(cal.calibration_data, cal.generator)
    # This checks that Q0 P1->1 value is that corresponding to Q0
    assert abs(out[5] - 0.766) < 0.02


def test_m3_conversion5():
    """Test that M3 conversion for independent cals works for permuted orderings"""
    for _ in range(5):
        perm = np.random.permutation(range(5))
        target_idx = np.where(perm == 0)[0][0]
        cal = Calibration(BACKEND, qubits=perm, method="independent")
        cal.run(shots=int(1e4))
        out = cal.to_m3_calibration()
        assert abs(out[2 * target_idx + 1] - 0.766) < 0.02