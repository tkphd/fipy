from __future__ import unicode_literals
from fipy.solvers.scipy.linearCGSSolver import LinearCGSSolver as ScipyLinearCGSSolver
from fipy.solvers.pyAMG.preconditioners.smoothedAggregationPreconditioner import SmoothedAggregationPreconditioner

__all__ = ["LinearCGSSolver"]
from future.utils import text_to_native_str
__all__ = [text_to_native_str(n) for n in __all__]

class LinearCGSSolver(ScipyLinearCGSSolver):
    """
    The `LinearCGSSolver` is an interface to the CGS solver in Scipy,
    using the pyAMG `SmoothedAggregationPreconditioner` by default.
    """

    def __init__(self, tolerance=1e-15, iterations=2000, precon=SmoothedAggregationPreconditioner()):
        """
        :Parameters:
          - `tolerance`: The required error tolerance.
          - `iterations`: The maximum number of iterative steps to perform.
          - `precon`: Preconditioner to use.

        """

        super(LinearCGSSolver, self).__init__(tolerance=tolerance, iterations=iterations, precon=precon)
