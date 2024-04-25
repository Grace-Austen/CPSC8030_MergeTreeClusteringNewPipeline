# CPSC8030_MergeTreeClusteringNewPipeline
This repository should contain the code you need to run the new MergeTreeClustering pipeline starting from vtm files of your join and split trees. The actual new pipeline is ontained in preprocessing.py; however, to test and compare the new and old pipelines, use the Test Running instructions below.

To compare the differences between the created merge trees, run "diff.sh". It also compares the saved data of the grouped trees using the original pipeline and the new pipeline. For some reason the segmentation files are different for both.

More information on input requirements to come.

## Test Running
 - Open Paraview
 - Run script "ideal_pre-pipeline.py"
 - Run script "new_pipeline.py"
 - Run script "original_pipeline.py"