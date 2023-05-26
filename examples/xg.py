import numpy as np
import pathlib
from occwl.compound import Compound
from occwl.solid import Solid
from occwl.viewer import Viewer
from occwl.graph import face_adjacency
from occwl.viewer import OffscreenRenderer

def vis(path, outpath, offline=True, vis_graph=False):

    #compound = Compound.load_from_step(pathlib.Path(__file__).resolve().parent.joinpath("/local-scratch/localhome/xya120/studio/datasets/fatemp/19518_f220b68a/assembly.step"))
    #compound = Compound.load_from_step(pathlib.Path(__file__).resolve().parent.joinpath("/local-scratch/localhome/xya120/studio/datasets/fatemp/23184_731e5af0/assembly.step"))
    compound = Compound.load_from_step(pathlib.Path(__file__).resolve().parent.joinpath(path) )

    #example = Solid.make_box(10, 10, 10)
    # example = Solid.make_sphere(10, (0, 0, 0))
    example = compound

    solids = list(compound.solids())
    faces = list(compound.faces())
    shells = list(compound.shells())
    example = compound

    #v = Viewer(backend="wx")

    if offline == False:
        v = Viewer(backend="wx")
    else:
        v = OffscreenRenderer()

    if vis_graph == True:
        for face in compound.faces():
            v.display(face, color=tuple(np.random.rand(3)*.5), transparency=0.8)
        g = face_adjacency(compound, self_loops=False)

        print(f"Number of nodes (faces): {len(g.nodes)}")
        print(f"Number of edges: {len(g.edges)}")
        # Get the points at each face's center
        face_centers = {}
        for face_idx in g.nodes():
            # Display a sphere for each face's center
            face = g.nodes[face_idx]["face"]
            parbox = face.uv_bounds()
            umin, vmin = parbox.min_point()
            umax, vmax = parbox.max_point()
            center_uv = (umin + 0.5 * (umax - umin), vmin + 0.5 * (vmax - vmin))
            center = face.point(center_uv)
            v.display(Solid.make_sphere(center=center, radius=0.25))
            face_centers[face_idx] = center

        for fi, fj in g.edges():
            pt1 = face_centers[fi]
            pt2 = face_centers[fj]
            # Make a cylinder for each edge connecting a pair of faces
            up_dir = pt2 - pt1
            height = np.linalg.norm(up_dir)
            if height > 1e-3:
                v.display(
                    Solid.make_cylinder(
                        radius=5.2, height=height, base_point=pt1, up_dir=up_dir
                    )
                )
    else:
        for face in compound.faces():
            v.display(face, color=tuple(np.random.rand(3)*.5))
        #v.display(example)
    # Show the viewer
    v.fit()
    if offline == True:
        v.save_image(outpath)
    else:
        v.show()
import os
import glob 
import tqdm
def render_dataset(outname="vis_graph", max_num=400, offline=True, vis_graph=True):
    if os.path.exists(outname) == False:
        os.mkdir(outname)
    shapes = glob.glob("/local-scratch/localhome/xya120/studio/datasets/fusion_assembly/*")
    for shape in tqdm.tqdm(shapes[:1000]):
        path = shape + "/assembly.step"
        if os.path.exists(path) == False:
            continue
        outpath = f"{outname}/" + shape.split("/")[-1] + ".png"
        try:
            vis(path, outpath, offline=offline, vis_graph=vis_graph)
        except Exception as e:
            print(e)
            print("skipping")
            continue
#render_dataset("vis", offline=True, vis_graph=False)
render_dataset("vis_graph", offline=True, vis_graph=True)
