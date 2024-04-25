#!/usr/bin/env python

from paraview.simple import *

loadpath = "C:/Users/Grace/Documents/Clemson/Spring 2024/CPSC 8030 Scientific Visualization/presentation/Isabel.cdb/data/"

savepath = "C:/Users/Grace/Documents/Clemson/Spring 2024/CPSC 8030 Scientific Visualization/presentation/trees/"

vti_files = [
    "isabel_02.vti",
    "isabel_03.vti",
    "isabel_04.vti",
    "isabel_05.vti",
    "isabel_30.vti",
    "isabel_31.vti",
    "isabel_32.vti",
    "isabel_33.vti",
    "isabel_45.vti",
    "isabel_46.vti",
    "isabel_47.vti",
    "isabel_48.vti",
]

for fileName in vti_files:
    # read vti
    reader = XMLImageDataReader(FileName=loadpath+fileName)

    save_name = fileName.split(".")
    save_name[-1] = 'vtm'
    save_name = ".".join(save_name)

    # create and save join tree
    join_tree = TTKMergeandContourTreeFTM(Input=reader)
    join_tree.ScalarField = ["POINTS", "velocityMag"]
    join_tree.TreeType = "Join Tree"
    jt_group = GroupDatasets(
        Input=[
            join_tree,
            OutputPort(join_tree, 1),
            OutputPort(join_tree, 2),
        ],
        BlockNames = ["Skeleton Nodes", "Skeleton Arcs", "Segmentation"]
    )
    SaveData(savepath+"join_trees/"+save_name, jt_group)

    # create and save split tree
    split_tree = TTKMergeandContourTreeFTM(Input=reader)
    split_tree.ScalarField = ["POINTS", "velocityMag"]
    split_tree.TreeType = "Split Tree"
    st_group = GroupDatasets(
        Input=[
            split_tree,
            OutputPort(split_tree, 1),
            OutputPort(split_tree, 2),
        ],
        BlockNames = ["Skeleton Nodes", "Skeleton Arcs", "Segmentation"]
    )
    SaveData(savepath+"split_trees/"+save_name, st_group)
