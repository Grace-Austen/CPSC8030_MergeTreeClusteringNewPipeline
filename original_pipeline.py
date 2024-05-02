#!/usr/bin/env python

from paraview.simple import *

basepath = "C:/Users/Grace/Documents/Clemson/Spring 2024/CPSC 8030 Scientific Visualization/presentation/CPSC8030_MergeTreeClusteringNewPipeline/"

# create a new 'TTK CinemaReader'
tTKCinemaReader1 = TTKCinemaReader(DatabasePath=basepath+"Isabel.cdb")

# create a new 'TTK CinemaProductReader'
tTKCinemaProductReader1 = TTKCinemaProductReader(Input=tTKCinemaReader1)
tTKCinemaProductReader1.AddFieldDataRecursively = 1

# create a new 'TTK Merge and Contour Tree'
tTKMergeandContourTreeFTM26 = TTKMergeandContourTreeFTM(Input=tTKCinemaProductReader1)
tTKMergeandContourTreeFTM26.ScalarField = ["POINTS", "velocityMag"]
tTKMergeandContourTreeFTM26.TreeType = "Join Tree"

# create a new 'Group Datasets'
mt_JT_all = GroupDatasets(
    Input=[
        tTKMergeandContourTreeFTM26,
        OutputPort(tTKMergeandContourTreeFTM26, 1),
        OutputPort(tTKMergeandContourTreeFTM26, 2),
    ]
)

# create a new 'TTK Merge and Contour Tree'
tTKMergeandContourTreeFTM25 = TTKMergeandContourTreeFTM(Input=tTKCinemaProductReader1)
tTKMergeandContourTreeFTM25.ScalarField = ["POINTS", "velocityMag"]
tTKMergeandContourTreeFTM25.TreeType = "Split Tree"

# create a new 'Group Datasets'
mT_all = GroupDatasets(
    Input=[
        tTKMergeandContourTreeFTM25,
        OutputPort(tTKMergeandContourTreeFTM25, 1),
        OutputPort(tTKMergeandContourTreeFTM25, 2),
    ]
)

# create a new 'TTK MergeTreeClustering'
tTKMergeTreeClustering1 = TTKMergeTreeClustering(
    Input=mT_all, OptionalInputclustering=mt_JT_all
)
tTKMergeTreeClustering1.ComputeBarycenter = 1
tTKMergeTreeClustering1.NumberOfClusters = 3
tTKMergeTreeClustering1.Deterministic = 1
tTKMergeTreeClustering1.DimensionSpacing = 0.1
tTKMergeTreeClustering1.PersistenceThreshold = 2.0
tTKMergeTreeClustering1.ImportantPairs = 34.0
tTKMergeTreeClustering1.MaximumNumberofImportantPairs = 3
tTKMergeTreeClustering1.MinimumNumberofImportantPairs = 2
tTKMergeTreeClustering1.ImportantPairsSpacing = 15.0
tTKMergeTreeClustering1.NonImportantPairsProximity = 0.15

original_clustering = GroupDatasets(
    Input=[
        tTKMergeTreeClustering1,
        OutputPort(tTKMergeTreeClustering1, 1),
        OutputPort(tTKMergeTreeClustering1, 2),
    ]
)

SaveData(basepath+"original_clustering.vtm", original_clustering)