import os
import glob 
import numpy as np
files = glob.glob("/local-scratch/localhome/xya120/studio/datasets/fusion_assembly/*/assembly.png")
choice = np.random.choice(len(files), 500, replace=False)
for i in choice:
    path = files[i]
    outpath = "/local-scratch/localhome/xya120/studio/datasets/fusionsubset/" + path.split("/")[-2] + ".png"
    print(path)
    print(outpath)
    os.system("cp " + path + " " + outpath)
