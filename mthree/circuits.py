# This code is part of Mthree.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""mthree circuit building routines"""
import numpy as np
from qiskit import QuantumCircuit


def _tensor_meas_states(qubit, num_qubits, initial_reset=False):
    """Construct |0> and |1> states
    for independent 1Q cals.
    """
    qc0 = QuantumCircuit(num_qubits, 1)
    if initial_reset:
        qc0.reset(qubit)
    qc0.measure(qubit, 0)
    qc1 = QuantumCircuit(num_qubits, 1)
    if initial_reset:
        qc1.reset(qubit)
    qc1.x(qubit)
    qc1.measure(qubit, 0)
    return [qc0, qc1]


def _marg_meas_states(qubits, num_system_qubits, initial_reset=False):
    """Construct all zeros and all ones states
    for marginal 1Q cals.
    """
    num_qubits = len(qubits)
    qc0 = QuantumCircuit(num_system_qubits, num_qubits)
    if initial_reset:
        qc0.reset(qubits)
    qc0.measure(qubits, range(num_qubits))
    qc1 = QuantumCircuit(num_system_qubits, num_qubits)
    if initial_reset:
        qc1.reset(qubits)
    qc1.x(qubits)
    qc1.measure(qubits, range(num_qubits))
    return [qc0, qc1]


def balanced_cal_circuits(generator, layout, system_qubits, initial_reset=False):
    """Build balanced calibration circuits.

    Parameters:
        generator (HadamardGenerator): Generator of balanced cal bit-strings for circuits
        layout (list): Logical to physical qubit layout
        initial_reset (bool): Use resets at beginning of circuit.
        system_qubits (int): Number of qubits in system

    Returns:
        list: List of balanced cal circuits.
    """
    circs = []
    num_active_qubits = generator.num_qubits
    for bit_array in generator:
        qc = QuantumCircuit(system_qubits, num_active_qubits)
        if initial_reset:
            qc.barrier()
            qc.reset(range(system_qubits))
            qc.reset(range(system_qubits))
            qc.reset(range(system_qubits))
        for idx, bit in enumerate(bit_array[::-1]):
            if bit == 1:
                qc.x(layout[idx])
        qc.measure(layout, range(num_active_qubits))
        circs.append(qc)
    return circs
