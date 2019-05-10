"""

Input file for chemotaxis modeling.

Here are some test cases for the model.

    >>> from builtins import range
    >>> for i in range(10):
    ...     for var, eqn in eqs:
    ...         var.updateOld()
    ...     for var, eqn in eqs:
    ...         eqn.solve(var, dt = 1.0)

    >>> accuracy = 1e-2
    >>> print(KMVar.allclose(params['KM'], atol = accuracy))
    1
    >>> print(TMVar.allclose(params['TM'], atol = accuracy))
    1
    >>> print(TCVar.allclose(params['TC'], atol = accuracy))
    1
    >>> print(P2Var.allclose(params['P2'], atol = accuracy))
    1
    >>> print(P3Var.allclose(params['P3'], atol = accuracy))
    1
    >>> print(KCVar.allclose(params['KC'], atol = accuracy))
    1

"""
from __future__ import division
from __future__ import unicode_literals

from builtins import input
from builtins import range
from examples.chemotaxis.parameters import parameters
from fipy import CellVariable, Grid2D, TransientTerm, DiffusionTerm, ImplicitSourceTerm, Viewer

params = parameters['case 2']

nx = 50
ny = 50
dx = 1.
L = nx * dx

mesh = Grid2D(nx = nx, ny = ny, dx = dx, dy = 1.)

shift = 1.

KMVar = CellVariable(mesh = mesh, value = params['KM'] * shift, hasOld = 1)
KCVar = CellVariable(mesh = mesh, value = params['KC'] * shift, hasOld = 1)
TMVar = CellVariable(mesh = mesh, value = params['TM'] * shift, hasOld = 1)
TCVar = CellVariable(mesh = mesh, value = params['TC'] * shift, hasOld = 1)
P3Var = CellVariable(mesh = mesh, value = params['P3'] * shift, hasOld = 1)
P2Var = CellVariable(mesh = mesh, value = params['P2'] * shift, hasOld = 1)
RVar = CellVariable(mesh = mesh, value = params['R'], hasOld = 1)

PN = P3Var + P2Var

KMscCoeff = params['chiK'] * (RVar + 1) * (1 - KCVar - KMVar.cellVolumeAverage)
KMspCoeff = params['lambdaK'] / (1 + PN / params['kappaK'])
KMEq = TransientTerm() - KMscCoeff + ImplicitSourceTerm(KMspCoeff)

TMscCoeff = params['chiT'] * (1 - TCVar - TMVar.cellVolumeAverage)
TMspCoeff = params['lambdaT'] * (KMVar + params['zetaT'])
TMEq = TransientTerm() - TMscCoeff + ImplicitSourceTerm(TMspCoeff)

TCscCoeff = params['lambdaT'] * (TMVar * KMVar).cellVolumeAverage
TCspCoeff = params['lambdaTstar']
TCEq = TransientTerm() - TCscCoeff + ImplicitSourceTerm(TCspCoeff)

PIP2PITP = PN / (PN / params['kappam'] + PN.cellVolumeAverage / params['kappac'] + 1) + params['zetaPITP']

P3spCoeff = params['lambda3'] * (TMVar + params['zeta3T'])
P3scCoeff = params['chi3'] * KMVar * (PIP2PITP / (1 + KMVar / params['kappa3']) + params['zeta3PITP']) + params['zeta3']
P3Eq = TransientTerm() - DiffusionTerm(params['diffusionCoeff']) - P3scCoeff + ImplicitSourceTerm(P3spCoeff)

P2scCoeff = scCoeff = params['chi2'] + params['lambda3'] * params['zeta3T'] * P3Var
P2spCoeff = params['lambda2'] * (TMVar + params['zeta2T'])
P2Eq = TransientTerm() - DiffusionTerm(params['diffusionCoeff']) - P2scCoeff + ImplicitSourceTerm(P2spCoeff)

KCscCoeff = params['alphaKstar'] * params['lambdaK'] * (KMVar / (1 + PN / params['kappaK'])).cellVolumeAverage
KCspCoeff = params['lambdaKstar'] / (params['kappaKstar'] + KCVar)
KCEq = TransientTerm() - KCscCoeff + ImplicitSourceTerm(KCspCoeff)

eqs = ((KMVar, KMEq), (TMVar, TMEq), (TCVar, TCEq), (P3Var, P3Eq), (P2Var, P2Eq), (KCVar, KCEq))

if __name__ == '__main__':

    PNView = PN / PN.cellVolumeAverage
    PNView.setName('PN')
    PNViewer = Viewer(PNView, datamax=2., datamin=0., title='')

    KMView = KMVar / KMVar.cellVolumeAverage
    KMView.setName('KM')
    KMViewer = Viewer(KMView, datamax=2., datamin=0., title='')

    TMView = TMVar / TMVar.cellVolumeAverage
    TMView.setName('TM')
    TMViewer = Viewer(TMView, datamax=2., datamin=0., title='')

    for i in range(100):
        for var, eqn in eqs:
            var.updateOld()
        for var, eqn in eqs:
            eqn.solve(var, dt = 1.)

    x, y = mesh.cellCenters

    RVar[:] = L / sqrt((x - L / 2)**2 + (y - 2 * L)**2)

    for i in range(100):
        for var, eqn in eqs:
            var.updateOld()
        for var, eqn in eqs:
            eqn.solve(var, dt = 1.)

        PNViewer.plot()
        KMViewer.plot()
        TMViewer.plot()

    input("finished")
