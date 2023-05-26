import pathlib

from occwl.compound import Compound
from occwl.viewer import Viewer


# Returns a list of bodies from the step file, we only need the first one
compound = Compound.load_from_step(pathlib.Path(__file__).resolve().parent.joinpath("/local-scratch/localhome/xya120/studio/datasets/fatemp/19518_f220b68a/assembly.step"))
iters = compound.solids()
solid = next(iters)

v = Viewer(backend="wx")
v.display(compound)
v.fit()
v.show()
