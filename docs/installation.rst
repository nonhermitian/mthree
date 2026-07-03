############
Installation
############

You can `pip` install M3 in serial mode using PyPi via:

.. code-block:: bash

    pip install mthree


Alternatively, you can install from source:

.. code-block:: bash

    python setup.py install


To enable OpenMP, you must have an OpenMP 3.0+ enabled compiler and install with:

.. code-block:: bash

    python setup.py install --with-openmp


Optionally you can also set ``-march=native`` using:

.. code-block:: bash

    python setup.py install --with-native


The ``openmp`` and ``native`` flags can be used simultaneously using a comma.

OpenMP on OSX
-------------

On OSX, install LLVM using homebrew (You cannot use GCC):

.. code-block:: bash

    brew install llvm


after which the following (or the like) must be executed in the terminal:

.. code-block:: bash

    export PATH="/usr/local/opt/llvm/bin:$PATH"


and

.. code-block:: bash

    export LDFLAGS="-L/usr/local/opt/llvm/lib -Wl,-rpath,/usr/local/opt/llvm/lib"
    export CPPFLAGS="-I/usr/local/opt/llvm/include"

Install with OpenMP using:

.. code-block:: bash

    CC=clang CXX=clang python setup.py install --with-openmp
