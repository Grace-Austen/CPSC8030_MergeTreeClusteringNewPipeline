# CPSC8030_MergeTreeClusteringNewPipeline
The Topology Toolkit (TTK) contains many useful data filters and has been designed to work as a Paraview plugin. One such filter is MergeTreeClustering. One limitation of TTK's MergeTreeClustering filter is that their proposed pipeline expects a cinema database (cdb) which contains the data files to compute the merge trees that will then be clustered. This repository explores a pipeline that will start with files that contain trees rather than the raw data. One thing to note is that MergeTreeClustering takes in the join and split trees of the data files rather than the whole merge tree, so both join and split trees will be needed as input to this new pipeline.

Included in this README are the following topics:
1. A brief overview of the original MergeTreeClustering pipeline
2. Details on the new MergeTreeClustering pipeline and input requirements
3. Example comparing the original and new pipelines

Included in this repository are the following:
- This README
- Python scripts to be used with Paraview to run the original and new pipelines
- Data for the example (Isabel.cdb) and a subset of the data (Isabel_small.cdb)
- Saved MergeTreeClustering output from pipelines
- Bash script to compare the saved data files produced by the pipelines using diff
- Saved join and split trees to explore the differences between the MergeTreeClustering files from the pipelines

## Original MergeTreeClustering Pipeline
See TTK's MergeTreeClustering example at https://topology-tool-kit.github.io/examples/mergeTreeClustering/.
- Read in data from the cdb database
    - Use TTKCinemaReader, and set the Database Path as \[name\].cdb directory
    - Apply TTKCinemaProductReader filter to the TTKCinemaReader
- Apply TTKMergeandContourTreeFTM twice to TTKCinemaProductReader
    - Set one TTKMergeandContourTreeFTM tree type to join tree
    - Set the other TTKMergeandContourTreeFTM tree type to split tree
- Apply GroupDatasets filter to the outputs of both the TTKMergeandContourTreeFTM 
    - Select the Skeleton Nodes, Skeleton Arcs, and Segmentation in that order
    - Apply GroupDatasets
    - Perform for both the join tree and split tree TTKMergeandContourTreeFTM
- Apply TTKMergeTreeClustering filter
    - Select the split tree GroupDatasets as the main required input
    - Select the join tree GroupDatasets as the optional input

### MergeTreeClustering Input Requirements
MergeTreeClustering requires the join and split trees of the datasets you wish to cluster the merge trees of. The join and split trees should be formatted so it's vtkMultiBlockDataset containing 3 sub vtkMultiBlockDatasets. The 3 sub vtkMultiBlockDatasets should be the nodes, arcs, and segmentation of the join or split trees.  

## New MergeTreeClustering Pipeline
The new pipeline needs to take in multiple join and split trees of the desired input datasets. This pipeline will separate the nodes, arcs, and segmentations for each tree and GroupDataset each together. This will result in 6 vtkMultiBlockDataSets: join tree nodes, join tree arcs, join tree segmentations, split tree nodes, split tree arcs, and split tree segmentations. Then, it will GroupDataset the join tree MultiBlockDataSets together and the split tree MultiBlockDataSets together. This will result in two MultiBlockDataSets, one for join trees and one for split trees. 

The function containing this new pipeline is contained in "preprocessing.py" in the function `preprocess()`. To see the details on the input requirements, refer to the section below.

### Input Requirements
`preprocess()` takes in a list of the join trees and a list of split trees in that order. The order of the join tree files should match the order of the split tree files so the join and split trees at index i correspond to the trees from that same input file. The files themselves should be vtm files. These vtm files should have a corresponding directory so the file \[file_name\].vtm has the accompanying directory \[file_name\]. Within the directory will be \[file_name\]_0_0.vtu which contains the tree's nodes, \[file_name\]_1_0.vtu which contains the tree's arcs, and \[file_name\]_2_0.vti which contains the segmentation for the original input vti file.
- The nodes file should specify an unstructured grid. Depending on the datamode, the specific structure could vary; however, a few things should stay consistent. Within the Piece tag, NumberOfCells should be 1. 
    - The PointData tag should have the attribute Scalars="CriticalType". Within PointData there should be 6 DataArray tags.
        - NodeId (node id's, should be the same as range(# of nodes))
        - Scalar (scalar values for each of the nodes)
        - VertexId (I believe this maps nodes to a vertex in the original image file)
        - CriticalType (type of critical point)
        - RegionSize (I believe this is the number of vertex in each segment)
        - RegionSpan (unclear - related to segmentation)
    - There should be no CellData, just an opening and closing tag
    - Points should have one DataAray "Points" describing the location of the points of each node. There should be two information keys, "L2_NORM_RANGE" and "L2_NORM_FINITE_RANGE". Both keys refer to the L2 norm of the points' coordinates. 
        - InformationKey name=[one of the names] location="vtkDataArray" length="2"
            - Value index="0" (lower value of the range)
            - Value index="1" (upper value of the range)
    - The Cells should contain the three expected DataArrays required for UnstructuredGrids: connectivity, offsets, and types. Since this file represents nodes, the types should all be type 2 or VTK_POLY_VERTEX. See VTK's file structure documentation for more information.
- The arcs file should specify an unstructured grid. Depending on the datamode, the specific structure could vary; however, a few things should stay consistent. It appears the number of cells is one less than the number of points
    - The PointData should have two DataArrays.
        - Scalar (scalar values for each of the nodes)
        - ttkMaskScalarField (don't know what this is for, appears to be all 0's)
    - CellData should have the attribute Scalars="SegmentationId" and 5 DataArrays
        - SegmentationId (I believe this is what segment the cell belongs to)
        - upNodeId (I believe this is the one end of an arc)
        - downNodeId (I believe this is the other end of an arc, but should be the same as range(# of cells-1))
        - RegionSize (I believe this is the number of vertex in each segment)
        - RegionSpan (unclear - related to segmentation)
    - Points should have one DataAray "Points" describing the location of the points of each node. There should be two information keys, "L2_NORM_RANGE" and "L2_NORM_FINITE_RANGE". Both keys refer to the L2 norm of the points' coordinates. 
        - InformationKey name=[one of the names] location="vtkDataArray" length="2"
            - Value index="0" (lower value of the range)
            - Value index="1" (upper value of the range)
    - The Cells should contain the three expected DataArrays required for UnstructuredGrids: connectivity, offsets, and types. Since this file represents arcs, the types should all be type 3 or VTK_LINE. See VTK's file structure documentation for more information.
- The segmentation file should specify an image file. Depending on the datamode, the specific structure could vary; however, a few things should stay consistent. First, there is the FieldData section which appears to be copied from the original vti file. Then, there is the Piece section with PointData and CellData.
    - PointData should have the attribute Scalars="SegmentationId" and 5 DataArray tags.
        - name_of_scalar_field_merge_tree_is_computed_on (this DataArray should also be copied from the original vti file and is the scalar field that the merge tree is calculated on)
        - SegmentationId (appears to map the points to a segment)
        - RegionSize (I believe this is the number of vertex in each segment)
        - RegionSpan (unclear - related to segmentation)
        - RegionType (can be set to Min_arc, Max_arc, Saddle1_arc, Saddle2_arc, and Saddle1_saddle2_arc)
    - There should be no CellData, just an opening and closing tag

## Comparison Example
To run the scripts that will compare the original and new pipelines, see the instructions below.
- Open Paraview
- Ensure the paths in the Python files match the path to your data and where you want to save and load your trees (use absolute paths for the least amount of headache)
    - loadpath is the path to Isabel.cdb
    - savepath is where you want to save your join and split trees from the "pre-pipeline.py" file
        - I've saved mine to CPSC8030_MergeTreeClusteringNewPipeline/trees
        - Whatever directory you choose to save your join and split trees in, a join_trees and a split_trees directory will be created
    - basepath is where the directory that you will save the new and original clustered merge tree data as well as where Isabel.cdb should be located
    - load_join_trees is the path to the join_trees directory where the generated join trees were saved to
    - load_split_trees is the path to the split_trees directory where the generated split trees were saved to
- Run script "ideal_pre-pipeline.py"
- Run script "new_pipeline.py"
- Run script "original_pipeline.py"
- Navigate to the directory with "diff.sh" and run "diff.sh"

You will see in Paraview that the resulting MergeTreeClusterings visually look the same and the cluster membership is the same. However, at the file level, there are some discrepancies with the nodes; however, this may stem from the input trees (see Explanation of output from the example -"diff.sh").

### Explanation of Output
Test Running will create many files and folders. 
- "ideal_pre-pipeline.py" will save the join trees and split trees generated for each of the individual vti files that are found in "Isabel.cdb/data". These join trees and split trees will be found in the directory "trees/join_trees" and "trees/split_trees" respectively. These trees will be saved as a \[file_name\].vtm with an accompanying directory \[file_name\]. Within the directory will be \[file_name\]_0_0.vtu which contains the tree's nodes, \[file_name\]_1_0.vtu which contains the tree's arcs, and \[file_name\]_2_0.vti which contains the segmentation for the original input vti file.
- "new_pipeline.py" will take the join trees and split trees created and saved above, and reformat the nodes, arcs, and segmentations to be compatible with TTK's merge tree clustering filter. Then, it will save the merge tree clustering data output. This is saved to new_clustering.vtm and the actual data files will be in the directory new_clustering. The input join trees and split trees are combined to create the merge tree and those merge trees are saved as nodes and arcs. The input merge trees' nodes are stored in new_clustering_\[a\]\_0.vtu where \[a\] is between 0 and 11. The arcs are stored in new_clustering_\[b\]\_0.vtu where \[b\] is between 12 and 23. The merge tree clustering was calculated with 3 centroids. The 3 cluster centroids are also merge trees represented by their nodes and arcs. The cluster centroid nodes are stored in new_clustering_\[c\]\_0.vtu where \[c\] is between 24 and 26. The cluster centroid arcs are stored in new_clustering_\[d\]\_0.vtu where \[d\] is between 27 and 29. There are also mappings between each merge tree and the centroid of the cluster they belong to. These mappings are found in new_clustering_\[e\]\_0.vtu where \[e\] is between 30 and 41. 
- "original_pipeline.py" will take Isabel.cdb as an input. After creating join trees and split trees from the database, it will input the trees to the TTK's merge tree clustering filter. Then, it will save the merge tree clustering data output. This is saved to original_clustering.vtm and the actual data files will be in the directory original_clustering. The input join trees and split trees are combined to create the merge tree and those merge trees are saved as nodes and arcs. The input merge trees' nodes are stored in original_clustering_\[a\]\_0.vtu where \[a\] is between 0 and 11. The arcs are stored in original_clustering_\[b\]\_0.vtu where \[b\] is between 12 and 23. The merge tree clustering was calculated with 3 centroids. The 3 cluster centroids are also merge trees represented by their nodes and arcs. The cluster centroid nodes are stored in original_clustering_\[c\]\_0.vtu where \[c\] is between 24 and 26. The cluster centroid arcs are stored in original_clustering_\[d\]\_0.vtu where \[d\] is between 27 and 29. There are also mappings between each merge tree and the centroid of the cluster they belong to. These mappings are found in original_clustering_\[e\]\_0.vtu where \[e\] is between 30 and 41. 
- "diff.sh" will compare the files found in the directories original_clustering and new_clustering to see if the merge tree clusters are the same. "diff.sh" also compares the grouped join and split tree files that were manually saved from the original and new pipeline (see details below). When "diff.sh" was run, the nodes for both trees were not the same, but the arcs and mappings were. Another difference found was between the original and new trees' segmentations. All of those files were different, but not the node and arc files.

### Additional File Details
There are four files and directories not produced by the original and new pipelines. They are join_tree_single.vtm, join_tree_db.vtm, split_tree_single.vtm, and split_tree_db.vtm. These were used to debug the differences found between the clustered merge tree output produced by new_pipeline.py and original_pipeline.py. 
 - join_tree_single.vtm is the Paraview multiblock save file for the grouped join trees created by loading in each of the 12 individual vti image files, performing a join tree on them, saving each join tree, reloading the saved join trees, using "Group Dataset" to group all the nodes, all the arcs, and all the segments with each other, and then using "Group Dataset" again to group the grouped nodes, arcs, and segments into a final vtkMultiBlockDataset. The data files are found in the join_tree_single directory. 
 - join_tree_db.vtm is the Paraview multiblock save file for the grouped join trees created by loading the Isabel.cdb database, performing a join tree on it, and then using "Group Dataset" on the nodes, arcs, and segments. The data files are found in the join_tree_db directory.
  - split_tree_single.vtm is the Paraview multiblock save file for the grouped split trees created by loading in each of the 12 individual vti image files, performing a split tree on them, saving each split tree, reloading the saved split trees, using "Group Dataset" to group all the nodes, all the arcs, and all the segments with each other, and then using "Group Dataset" again to group the grouped nodes, arcs, and segments into a final vtkMultiBlockDataset. The data files are found in the split_tree_single directory.
 - split_tree_db.vtm is the Paraview multiblock save file for the grouped join trees created by loading the Isabel.cdb database, performing a split tree on it, and then using "Group Dataset" on the nodes, arcs, and segments. The data files are found in the split_tree_db directory.

## Notes
Due to space and computational constraints, I am saving off files using Paraview's default datamode. The diff comparison would be more useful if DataMode='Ascii'.