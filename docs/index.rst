#######################################
Matrix-free measurement mitigation (M3)
#######################################

M3 is a package for scalable quantum measurement error mitigation that need not
explicitly form the assignment matrix, or its inverse, as is thus a **m**\atrix-free
**m**\easurement **m**\itigation (M3) routine.

M3 works in a reduced subspace defined by the noisy input bitstrings that are to be
corrected.  Because the number of unique bitstrings can be much smaller than the
dimensionality of the full multi-qubit Hilbert space, the resulting linear system
of equations is nominally much easier to solve.

.. figure:: images/truncation.png
    :align: center

It is often the case that this linear equation is trivial to solve using LU decomposition,
using only modest computing resources.  However, if the number of unique bitstrings is large,
or if you have very tight memory constraints, then the problem can be solved in a matrix-free
manner using a preconditioned iterative linear solution method &mdash; for example, the generalized minimal
residual (GMRES) or biconjugate gradient stabilized (BiCGSTAB) methods.

M3 is suitable for problems amenable to using quasi-probabilities such as those
formulated in terms of expectation values, or sampling problems where, for example, one is
interested in the bitstring with the highest probability.  Quasi-probabilities can be
projected onto the nearest probability distribution if true probabilities are desired, but
this makes error analysis more difficult.  M3 works for mid-circuit measurements as well,
provided that you are interested in ensemble averages, as opposed to correcting single-shot
measurements; it cannot mitigate single-shot measurements used for conditional-gate logic. 

.. tip:: Not sure where to get started?
   
   Have a look at how others have utilized M3: :ref:`papers`.

