#!/usr/bin/env python

##
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 #
 #  FILE: "cylindricalMesh2D.py"
 #
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # of Standards and Technology, an agency of the Federal Government.
 # Pursuant to title 17 section 105 of the United States Code,
 # United States Code this software is not subject to copyright
 # protection, and this software is considered to be in the public domain.
 # FiPy is an experimental system.
 # NIST assumes no responsibility whatsoever for its use by whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 #
 # To the extent that NIST may hold copyright in countries other than the
 # United States, you are hereby granted the non-exclusive irrevocable and
 # unconditional right to print, publish, prepare derivative works and
 # distribute this software, in any medium, or authorize others to do so on
 # your behalf, on a royalty-free basis throughout the world.
 #
 # You may improve, modify, and create derivative works of the software or
 # any portion of the software, and you may copy and distribute such
 # modifications or works.  Modified works should carry a notice stating
 # that you changed the software and should note the date and nature of any
 # such change.  Please explicitly acknowledge the National Institute of
 # Standards and Technology as the original source.
 #
 # This software can be redistributed and/or modified freely provided that
 # any derivative works bear some notice that they are derived from it, and
 # any modified versions bear some notice that they have been modified.
 # ========================================================================
 #
 # ###################################################################
 ##

r"""

This example solves the steady-state cylindrical convection-diffusion equation
given by:

.. math::

   \nabla \cdot \left(D \nabla \phi + \vec{u} \phi \right) = 0

with coefficients :math:`D = 1` and :math:`\vec{u} = (10,)`, or

>>> diffCoeff = 1.
>>> convCoeff = ((10.,),(0.,))

We define a 2D cylindrical mesh representing an annulus. The mesh is a
pseudo-1D mesh, but is a good test case for the :class:`~fipy.meshes.cylindricalGrid2D.CylindricalGrid2D`
mesh. The mesh has a non-constant cell spacing.

>>> from fipy import CellVariable, CylindricalGrid2D, DiffusionTerm, ExponentialConvectionTerm, Viewer
>>> from fipy.tools import numerix

>>> r0 = 1.
>>> r1 = 2.
>>> nr = 100
>>> Rratio = (r1 / r0)**(1 / float(nr))
>>> dr = r0 * (Rratio - 1) * Rratio**numerix.arange(nr)
>>> mesh = CylindricalGrid2D(dr=dr, dz=1., nz=1) + ((r0,), (0.,))

The solution variable is initialized to ``valueLeft``:

>>> valueLeft = 0.
>>> valueRight = 1.
>>> var = CellVariable(mesh=mesh, name = "variable")

and impose the boundary conditions

.. math::

   \phi = \begin{cases}
   0& \text{at $r = r_0$,} \\
   1& \text{at $r = r_1$,}
   \end{cases}

with

>>> var.constrain(valueLeft, mesh.facesLeft)
>>> var.constrain(valueRight, mesh.facesRight)

The equation is created with the :class:`~fipy.terms.diffusionTerm.DiffusionTerm` and
:class:`~fipy.terms.exponentialConvectionTerm.ExponentialConvectionTerm`.

>>> eq = (DiffusionTerm(coeff=diffCoeff)
...       + ExponentialConvectionTerm(coeff=convCoeff))

More details of the benefits and drawbacks of each type of convection
term can be found in :ref:`sec:NumericalSchemes`.
Essentially, the :class:`~fipy.terms.exponentialConvectionTerm.ExponentialConvectionTerm` and :class:`~fipy.terms.powerLawConvectionTerm.PowerLawConvectionTerm` will
both handle most types of convection-diffusion cases, with the
:class:`~fipy.terms.powerLawConvectionTerm.PowerLawConvectionTerm` being more efficient.

We solve the equation

>>> eq.solve(var=var)

and test the solution against the analytical result

.. math::

   \phi = \exp{\frac{u}{D} \left(r_1 - r\right)} \left( \frac{ \ei{\frac{u r_0}{D}} - \ei{\frac{u r}{D}} }{ \ei{\frac{u r_0}{D}} - \ei{\frac{u r_1}{D}} } \right)

.. index:: exp

>>> axis = 0
>>> try:
...     from scipy.special import expi # doctest: +SCIPY
...     r = mesh.cellCenters[axis]
...     U = convCoeff[0][0]
...     AA = numerix.exp(U / diffCoeff * (r1 - r))
...     BB = expi(U * r0 / diffCoeff) - expi(U * r / diffCoeff) # doctest: +SCIPY
...     CC = expi(U * r0 / diffCoeff) - expi(U * r1 / diffCoeff) # doctest: +SCIPY
...     analyticalArray = AA * BB / CC # doctest: +SCIPY
... except ImportError:
...     print "The SciPy library is unavailable. It is required for testing purposes."

>>> print var.allclose(analyticalArray, atol=1e-3) # doctest: +SCIPY
1

If the problem is run interactively, we can view the result:

.. index::
   module: fipy.viewers

>>> if __name__ == '__main__':
...     viewer = Viewer(vars=var)
...     viewer.plot()
"""
__docformat__ = 'restructuredtext'

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())

    raw_input('finished')
