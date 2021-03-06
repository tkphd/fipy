.. _USAGE:

==========
Using FiPy
==========

This document explains how to use :term:`FiPy` in a practical sense.
To see the problems that :term:`FiPy` is capable of solving, you can
run any of the scripts in the :ref:`examples <part:examples>`.

.. note::

   We strongly recommend you proceed through the :ref:`examples
   <part:examples>`, but at the very least work through
   :mod:`examples.diffusion.mesh1D` to understand the notation and
   basic concepts of :term:`FiPy`.

We exclusively use either the UNIX command line or :term:`IPython` to
interact with :term:`FiPy`. The commands in the :ref:`examples
<part:examples>` are written with the assumption that they will be
executed from the command line. For instance, from within the main
:term:`FiPy` directory, you can type::

    $ python examples/diffusion/mesh1D.py

A viewer should appear and you should be prompted through a series of
examples.

.. note::

   From within :term:`IPython`, you would type::

       >>> run examples/diffusion/mesh1D.py

In order to customize the examples, or to develop your own scripts, some
knowledge of Python syntax is required.  We recommend you familiarize
yourself with the excellent `Python tutorial`_ :cite:`PythonTutorial`
or with `Dive Into Python`_ :cite:`DiveIntoPython`.

.. _Python tutorial: http://docs.python.org/tut/tut.html
.. _Dive Into Python: http://diveintopython.org

As you gain experience, you may want to browse through the
:ref:`FlagsAndEnvironmentVariables` that affect :term:`FiPy`.

------------
Testing FiPy
------------

For a general installation, :term:`FiPy` can be tested by running::

    $ python -c "import fipy; fipy.test()"

This command runs all the test cases in :ref:`FiPy's modules
<part:modules>`, but doesn't include any of the tests in :ref:`FiPy's
examples <part:examples>`. To run the test cases in both :ref:`modules
<part:modules>` and :ref:`examples <part:examples>`, use::

    $ python setup.py test

in an unpacked :term:`FiPy` archive. The test suite can be run with a
number of different configurations depending on which solver suite is
available and other factors. See :ref:`FlagsAndEnvironmentVariables`
for more details.

:term:`FiPy` will skip tests that depend on :ref:`OPTIONALPACKAGES` that
have not been installed. For example, if :term:`Mayavi` and :term:`Gmsh`
are not installed, :term:`FiPy` will warn::

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Skipped 131 doctest examples because `gmsh` cannot be found on the $PATH
    Skipped 42 doctest examples because the `tvtk` package cannot be imported
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

We have a few known, intermittent failures:

 :trac:`#425`
    The test suite can freeze, usually in :mod:`examples.chemotaxis`,
    when running on multiple processors. This has never affected us in an
    actual parallel simulation, only in the test suite.

 :trac:`#430`
    When running in parallel, the tests for
    :class:`~fipy.terms.binaryTerm._BinaryTerm` sometimes return one
    erroneous result. This is not reliably reproducible and doesn't seem to
    have an effect on actual simulations.

Although the test suite may show warnings, there should be no other errors.
Any errors should be investigated or reported on the `issue tracker`_.
Users can see if there are any known problems for the latest :term:`FiPy`
distribution by checking `FiPy's automated test display`_.

.. _FiPy's automated test display: http://build.cmi.kent.edu:8010/console
.. _issue tracker: https://github.com/usnistgov/fipy/issues/new

Below are a number of common `Command-line Flags`_ for testing various
:term:`FiPy` configurations.

Parallel Tests
==============

If :term:`FiPy` is configured for :ref:`PARALLEL`, you can run the tests
on multiple processor cores with::

    $ mpirun -np {# of processors} python setup.py test --trilinos

or::

    $ mpirun -np {# of processors} python -c "import fipy; fipy.test('--trilinos')"

.. _FlagsAndEnvironmentVariables:

--------------------------------------------
Command-line Flags and Environment Variables
--------------------------------------------

:term:`FiPy` chooses a default run time configuration based on the
available packages on the system. The `Command-line Flags`_ and
`Environment Variables`_ sections below describe how to override
:term:`FiPy`'s default behavior.

Command-line Flags
==================

You can add any of the following case-insensitive flags after the name of a
script you call from the command line, e.g::

    $ python myFiPyScript --someflag

.. cmdoption:: --inline

   Causes many mathematical operations to be performed in C, rather than
   Python, for improved performance. Requires the :mod:`scipy.weave`
   package.

The following flags take precedence over the :envvar:`FIPY_SOLVERS`
environment variable:

.. cmdoption:: --pysparse

   Forces the use of the :ref:`PYSPARSE` solvers.

.. cmdoption:: --trilinos

   Forces the use of the :ref:`TRILINOS` solvers, but uses
   :ref:`PYSPARSE` to construct the matrices.

.. cmdoption:: --no-pysparse

   Forces the use of the :ref:`TRILINOS` solvers without any use of
   :ref:`PYSPARSE`.

.. cmdoption:: --scipy

   Forces the use of the :ref:`SCIPY` solvers.

.. cmdoption:: --pyamg

   Forces the use of the :ref:`PYAMG` preconditioners in conjunction
   with the :ref:`SCIPY` solvers.

.. cmdoption:: --lsmlib

   Forces the use of the :ref:`LSMLIBDOC` level set solver.

.. cmdoption:: --skfmm

   Forces the use of the :ref:`SCIKITFMM` level set solver.


Environment Variables
=====================

You can set any of the following environment variables in the manner
appropriate for your shell. If you are not running in a shell (*e.g.*,
you are invoking :term:`FiPy` scripts from within :term:`IPython` or IDLE),
you can set these variables via the :data:`os.environ` dictionary,
but you must do so before importing anything from the :mod:`fipy`
package.

.. envvar:: FIPY_DISPLAY_MATRIX

   .. currentmodule:: fipy.terms.term

   If present, causes the graphical display of the solution matrix of each
   equation at each call of :meth:`~Term.solve` or :meth:`~Term.sweep`.
   Setting the value to "``terms``," causes the display of the matrix for each
   :class:`Term` that composes the equation. Requires the :term:`Matplotlib`
   package.

.. envvar:: FIPY_INLINE

   If present, causes many mathematical operations to be performed in C,
   rather than Python. Requires the :mod:`scipy.weave` package.

.. envvar:: FIPY_INLINE_COMMENT

   If present, causes the addition of a comment showing the Python context
   that produced a particular piece of :mod:`scipy.weave` C code. Useful
   for debugging.

.. envvar:: FIPY_SOLVERS

   Forces the use of the specified suite of linear solvers. Valid
   (case-insensitive) choices are "``pysparse``", "``trilinos``",
   "``no-pysparse``", "``scipy``" and "``pyamg``".

.. envvar:: FIPY_VERBOSE_SOLVER

   If present, causes the linear solvers to print a variety of diagnostic
   information.

.. envvar:: FIPY_VIEWER

   Forces the use of the specified viewer. Valid values are any
   :samp:`{<viewer>}` from the
   :samp:`fipy.viewers.{<viewer>}Viewer`
   modules. The special value of ``dummy`` will allow the script
   to run without displaying anything.

.. envvar:: FIPY_INCLUDE_NUMERIX_ALL

   If present, causes the inclusion of all functions and variables of the
   :mod:`~fipy.tools.numerix` module in the :mod:`fipy` namespace.

.. _PARALLEL:

-------------------
Solving in Parallel
-------------------

:term:`FiPy` can use :term:`Trilinos` to solve equations in
parallel. Most mesh classes in :mod:`fipy.meshes` can solve in
parallel. This includes all "``...Grid...``" and "``...Gmsh...``"
class meshes. Currently, the only remaining serial-only meshes are
:class:`~fipy.meshes.tri2D.Tri2D` and
:class:`~fipy.meshes.skewedGrid2D.SkewedGrid2D`.

.. attention::

   :term:`Trilinos` *must* be compiled with MPI support.

.. attention::

   :term:`FiPy` requires :ref:`MPI4PY` to work in parallel. See the
   :ref:`MPI4PY` installation guide.

.. note::

   Parallel efficiency is greatly improved by installing
   :term:`Pysparse` in addition to :term:`Trilinos`. If
   :term:`Pysparse` is not installed be sure to use the
   ``--no-pysparse`` flag when running in parallel.

It should not generally be necessary to change anything in your script.
Simply invoke::

    $ mpirun -np {# of processors} python myScript.py --trilinos

instead of::

    $ python myScript.py

To confirm that :term:`FiPy` and :term:`Trilinos` are properly configured
to solve in parallel, the easiest way to tell is to run one of the
examples, e.g.,::

    $ mpirun -np 2 examples/diffusion/mesh1D.py

You should see two viewers open with half the simulation running in one of
them and half in the other. If this does not look right (e.g., you get two
viewers, both showing the entire simulation), or if you just want to be
sure, you can run a diagnostic script::

    $ mpirun -np 3 python examples/parallel.py

which should print out::

    mpi4py: processor 0 of 3 :: PyTrilinos: processor 0 of 3 :: FiPy: 5 cells on processor 0 of 3
    mpi4py: processor 1 of 3 :: PyTrilinos: processor 1 of 3 :: FiPy: 7 cells on processor 1 of 3
    mpi4py: processor 2 of 3 :: PyTrilinos: processor 2 of 3 :: FiPy: 6 cells on processor 2 of 3

If there is a problem with your parallel environment, it should be clear
that there is either a problem importing one of the required packages or
that there is some problem with the MPI environment. For example::

    mpi4py: processor 2 of 3 :: PyTrilinos: processor 0 of 1 :: FiPy: 10 cells on processor 0 of 1
    [my.machine.com:69815] WARNING: There were 4 Windows created but not freed.
    mpi4py: processor 1 of 3 :: PyTrilinos: processor 0 of 1 :: FiPy: 10 cells on processor 0 of 1
    [my.machine.com:69814] WARNING: There were 4 Windows created but not freed.
    mpi4py: processor 0 of 3 :: PyTrilinos: processor 0 of 1 :: FiPy: 10 cells on processor 0 of 1
    [my.machine.com:69813] WARNING: There were 4 Windows created but not freed.

indicates :ref:`MPI4PY` is properly communicating with MPI and is running
in parallel, but that :ref:`TRILINOS` is not, and is running three separate
serial environments. As a result, :term:`FiPy` is limited to three separate
serial operations, too. In this instance, the problem is that although
:ref:`TRILINOS` was compiled with MPI enabled, it was compiled against a
different MPI library than is currently available (and which :ref:`MPI4PY`
was compiled against). The solution is to rebuild :ref:`TRILINOS` against
the active MPI libraries.

When solving in parallel, :term:`FiPy` essentially breaks the problem
up into separate sub-domains and solves them (somewhat) independently.
:term:`FiPy` generally "does the right thing", but if you find that
you need to do something with the entire solution, you can use
``var.``:attr:`~fipy.variables.cellVariable.CellVariable.globalValue`.

.. note::

    :term:`Trilinos` solvers frequently give intermediate output that
    :term:`FiPy` cannot suppress. The most commonly encountered
    messages are

     ``Gen_Prolongator warning : Max eigen <= 0.0``
        which is not significant to :term:`FiPy`.

     ``Aztec status AZ_loss: loss of precision``
        which indicates that there was some difficulty in solving the
        problem to the requested tolerance due to precision limitations,
        but usually does not prevent the solver from finding an adequate
        solution.

     ``Aztec status AZ_ill_cond: GMRES hessenberg ill-conditioned``
        which indicates that GMRES is having trouble with the problem, and
        may indicate that trying a different solver or preconditioner may
        give more accurate results if GMRES fails.

     ``Aztec status AZ_breakdown: numerical breakdown``
        which usually indicates serious problems solving the equation which
        forced the solver to stop before reaching an adequate solution.
        Different solvers, different preconditioners, or a less restrictive
        tolerance may help.

.. _MeshingWithGmsh:

-----------------
Meshing with Gmsh
-----------------

:term:`FiPy` works with arbitrary polygonal meshes generated by
:term:`Gmsh`.  :term:`FiPy` provides two wrappers classes
(:class:`~fipy.meshes.gmshImport.Gmsh2D` and
:class:`~fipy.meshes.gmshImport.Gmsh3D`) enabling :term:`Gmsh` to be
used directly from python. The classes can be instantiated with a set
of :term:`Gmsh` style commands (see
:mod:`examples.diffusion.circle`). The classes can also be
instantiated with the path to either a :term:`Gmsh` geometry file
(``.geo``) or a :term:`Gmsh` mesh file (``.msh``) (see
:mod:`examples.diffusion.anisotropy`).

As well as meshing arbitrary geometries, :term:`Gmsh` partitions
meshes for parallel simulations. Mesh partitioning automatically
occurs whenever a parallel communicator is passed to the mesh on
instantiation. This is the default setting for all meshes that work in
parallel including :class:`~fipy.meshes.gmshImport.Gmsh2D` and
:class:`~fipy.meshes.gmshImport.Gmsh3D`.

.. note::

    :term:`FiPy` solution accuracy can be compromised with highly
    non-orthogonal or non-conjunctional meshes.

.. _CoupledEquations:

----------------------------
Coupled and Vector Equations
----------------------------

Equations can now be coupled together so that the contributions from
all the equations appear in a single system matrix. This results in
tighter coupling for equations with spatial and temporal derivatives
in more than one variable. In :term:`FiPy` equations are coupled
together using the ``&`` operator::

   >>> eqn0 = ...
   >>> eqn1 = ...
   >>> coupledEqn = eqn0 & eqn1

The ``coupledEqn`` will use a combined system matrix that includes
four quadrants for each of the different variable and equation
combinations. In previous versions of :term:`FiPy` there has been no
need to specify which variable a given term acts on when generating
equations. The variable is simply specified when calling ``solve`` or
``sweep`` and this functionality has been maintained in the case of
single equations. However, for coupled equations the variable that a
given term operates on now needs to be specified when the equation is
generated. The syntax for generating coupled equations has the form::

   >>> eqn0 = Term00(coeff=..., var=var0) + Term01(coeff..., var=var1) == source0
   >>> eqn1 = Term10(coeff=..., var=var0) + Term11(coeff..., var=var1) == source1
   >>> coupledEqn = eqn0 & eqn1

and there is now no need to pass any variables when solving::

   >>> coupledEqn.solve(dt=..., solver=...)

In this case the matrix system will have the form

.. math::

   \left(
   \begin{array}{c|c}
   \text{\ttfamily Term00} & \text{\ttfamily Term01} \\ \hline
   \text{\ttfamily Term10} & \text{\ttfamily Term11}
   \end{array} \right)
   \left(
   \begin{array}{c}
   \text{\ttfamily var0}  \\ \hline
   \text{\ttfamily var1}
   \end{array} \right)
   =
   \left(
   \begin{array}{c}
   \text{\ttfamily source0}  \\ \hline
   \text{\ttfamily source1}
   \end{array} \right)

:term:`FiPy` tries to make sensible decisions regarding each term's
location in the matrix and the ordering of the variable column
array. For example, if ``Term01`` is a transient term then ``Term01``
would appear in the upper left diagonal and the ordering of the
variable column array would be reversed.

The use of coupled equation is described in detail in
:mod:`examples.diffusion.coupled`. Other examples that demonstrate the
use of coupled equations are :mod:`examples.phase.binaryCoupled`,
:mod:`examples.phase.polyxtalCoupled` and
:mod:`examples.cahnHilliard.mesh2DCoupled`. As well as coupling
equations, true vector equations can now be written in :term:`FiPy`
(see :mod:`examples.diffusion.coupled` for more details).

.. _BoundaryConditions:

-------------------
Boundary Conditions
-------------------

.. currentmodule:: fipy.variables.cellVariable

Applying fixed value (Dirichlet) boundary conditions
====================================================

To apply a fixed value boundary condition use the
:meth:`~CellVariable.constrain` method. For example, to fix `var` to
have a value of `2` along the upper surface of a domain, use

>>> var.constrain(2., where=mesh.facesTop)

.. note::

   The old equivalent
   :class:`~fipy.boundaryConditions.fixedValue.FixedValue` boundary
   condition is now deprecated.

Applying fixed gradient boundary conditions (Neumann)
=====================================================

To apply a fixed Gradient boundary condition use the
:attr:`~.CellVariable.faceGrad`.\
:meth:`~fipy.variables.variable.Variable.constrain` method. For
example, to fix `var` to have a gradient of `(0,2)` along the upper
surface of a 2D domain, use

>>> var.faceGrad.constrain(((0,),(2,)), where=mesh.facesTop)

If the gradient normal to the boundary (*e.g.*,
:math:`\hat{n}\cdot\nabla\phi`) is to be set to a scalar value of `2`, use

>>> var.faceGrad.constrain(2 * mesh.faceNormals, where=mesh.exteriorFaces)

Applying fixed flux boundary conditions
=======================================

Generally these can be implemented with a judicious use of
:attr:`~.CellVariable.faceGrad`.\
:meth:`~fipy.variables.variable.Variable.constrain`.  Failing that, an
exterior flux term can be added to the equation. Firstly, set the
terms' coefficients to be zero on the exterior faces,

>>> diffCoeff.constrain(0., mesh.exteriorFaces)
>>> convCoeff.constrain(0., mesh.exteriorFaces)

then create an equation with an extra term to account for the exterior flux,

>>> eqn = (TransientTerm() + ConvectionTerm(convCoeff)
...        == DiffusionCoeff(diffCoeff)
...        + (mesh.exteriorFaces * exteriorFlux).divergence)

where `exteriorFlux` is a rank 1
:class:`~fipy.variables.faceVariable.FaceVariable`.

.. note::

   The old equivalent :class:`~fipy.boundaryConditions.fixedFlux.FixedFlux`
   boundary condition is now deprecated.

Applying outlet or inlet boundary conditions
============================================

Convection terms default to a no flux boundary condition unless the
exterior faces are associated with a constraint, in which case either
an inlet or an outlet boundary condition is applied depending on the
flow direction.

Applying spatially varying boundary conditions
==============================================

The use of spatial varying boundary conditions is best demonstrated with an
example. Given a 2D equation in the domain :math:`0 < x < 1` and :math:`0 < y < 1` with
boundary conditions,

.. math::

  \phi = \left\{
            \begin{aligned}
                xy &\quad \text{on $x>1/2$ and $y>1/2$} \\
                \vec{n} \cdot \vec{F} = 0 &\quad \text{elsewhere}
            \end{aligned}
        \right.

where :math:`\vec{F}` represents the flux. The boundary conditions in :term:`FiPy` can
be written with the following code,

>>> X, Y = mesh.faceCenters
>>> mask =  ((X < 0.5) | (Y < 0.5))
>>> var.faceGrad.constrain(0, where=mesh.exteriorFaces & mask)
>>> var.constrain(X * Y, where=mesh.exteriorFaces & ~mask)

then

>>> eqn.solve(...)

Further demonstrations of spatially varying boundary condition can be found
in :mod:`examples.diffusion.mesh20x20`
and :mod:`examples.diffusion.circle`

Applying internal boundary conditions
=====================================

Applying internal boundary conditions can be achieved through the use
of implicit and explicit sources. An equation of the form

>>> eqn = TransientTerm() == DiffusionTerm()

can be constrained to have a fixed internal ``value`` at a position
given by ``mask`` with the following alterations

>>> eqn = TransientTerm() == DiffusionTerm() - ImplicitSourceTerm(mask * largeValue) + mask * largeValue * value

The parameter ``largeValue`` must be chosen to be large enough to
completely dominate the matrix diagonal and the RHS vector in cells
that are masked. The ``mask`` variable would typically be a
``CellVariable`` Boolean constructed using the cell center values.

One must be careful to distinguish between constraining internal cell
values during the solve step and simply applying arbitrary constraints
to a ``CellVariable``. Applying a constraint,

>>> var.constrain(value, where=mask)

simply fixes the returned value of ``var`` at ``mask`` to be
``value``. It does not have any effect on the implicit value of ``var`` at the
``mask`` location during the linear solve so it is not a substitute
for the source term machinations described above. Future releases of
:term:`FiPy` may implicitly deal with this discrepancy, but the current
release does not. A simple example can be used to demonstrate this::

>>> m = Grid1D(nx=2, dx=1.)
>>> var = CellVariable(mesh=m)

Apply a constraint to the faces for a right side boundary condition
(which works).

>>> var.constrain(1., where=m.facesRight)

Create the equation with the source term constraint described above

>>> mask = m.x < 1.
>>> largeValue = 1e+10
>>> value = 0.25
>>> eqn = DiffusionTerm() - ImplicitSourceTerm(largeValue * mask) + largeValue * mask * value

and the expected value is obtained.

>>> eqn.solve(var)
>>> print var
[ 0.25  0.75]

However, if a constraint is used without the source term constraint an
unexpected value is obtained

>>> var.constrain(0.25, where=mask)
>>> eqn = DiffusionTerm()
>>> eqn.solve(var)
>>> print var
[ 0.25  1.  ]

although the left cell has the expected value as it is constrained.

.. %    http://thread.gmane.org/gmane.comp.python.fipy/726
   %    http://thread.gmane.org/gmane.comp.python.fipy/846

   %    \subsection{Fourth order boundary conditions}

   %    http://thread.gmane.org/gmane.comp.python.fipy/923

   %    \subsection{Periodic boundary conditions}

   %    http://thread.gmane.org/gmane.comp.python.fipy/135

   %    \subsection{Time dependent boundary conditions}

   %    http://thread.gmane.org/gmane.comp.python.fipy/2

   %    \subsection{Internal boundary conditions}

.. _RunningUnderPython3:

----------------------
Running under Python 3
----------------------

It is possible to run :term:`FiPy` scripts under :term:`Python 3`, but
there is admittedly little advantage in doing so at this time. We still
develop and use :term:`FiPy` under :term:`Python` 2.x. To use, you must
first convert :term:`FiPy`'s code to :term:`Python 3` syntax. From within
the main :term:`FiPy` directory::

    $ 2to3 --write .
    $ 2to3 --write --doctests_only .

You can expect some harmless warnings from this conversion.

The minimal prerequisites are:

 * :term:`NumPy` version 1.5 or greater.
 * :term:`SciPy` version 0.9 or greater.
 * :term:`Matplotlib` version 1.2 or greater (this hasn't been
   released yet, and we haven't been able to successfully test the
   :mod:`~.fipy.viewers.matplotlibViewer` classes with their
   development code).

------
Manual
------

You can view the manual online at <http://www.ctcms.nist.gov/fipy> or you
can `download the latest manual`_ from
<http://www.ctcms.nist.gov/fipy/download/>. Alternatively,
it may be possible to build a fresh copy by issuing the following
command in the base directory::

    $ python setup.py build_docs --pdf --html

.. note::

   This mechanism is intended primarily for the developers. At a minimum,
   you will need at least version 1.1.2 of `Sphinx
   <http://sphinx.pocoo.org/latest>`_, plus all of its prerequisites,
   although we build the documentation with the latest development code
   (you will need hg_ installed)::

   $ pip install --upgrade -e hg+https://bitbucket.org/birkenfeld/sphinx#egg=sphinx

   We use several contributed Sphinx plugins::

   $ hg clone https://bitbucket.org/birkenfeld/sphinx-contrib/

   $ cd sphinx-contrib/traclinks
   $ python setup.py install

   Bibliographic citations require the `sphinxcontrib-bibtex` package. For
   the moment, the development versions of several packages are required
   to properly render our bibliography (you will need both bzr_ and git_
   installed)::

   $ pip install -e bzr+lp:~pybtex-devs/pybtex/trunk
   $ pip install -e git+git@github.com:mcmtroffaes/pybtex-docutils.git#egg=pybtex-docutils
   $ pip install -e git+git@github.com:mcmtroffaes/sphinxcontrib-bibtex.git#egg=sphinxcontrib-bibtex

.. _download the latest manual:  http://www.ctcms.nist.gov/fipy/download/
.. _hg: http://mercurial.selenic.com
.. _bzr: http://bazaar.canonical.com
.. _git: http://git-scm.com
