# CPSC8030_MergeTreeClusteringNewPipeline
This repository should contain the code you need to run the new MergeTreeClustering pipeline starting from vtm files of your join and split trees. The actual new pipeline is ontained in preprocessing.py; however, to test and compare the new and old pipelines, use the Test Running instructions below.

To compare the differences between the created merge trees, run "diff.sh". It also compares the saved data of the grouped trees using the original pipeline and the new pipeline. For some reason the segmentation files are different for both.

Grac'es to do list: finish other files notes, discoveries - discuss the weird mismatch thingy ^ in greater detail. Explain the original pipeline and its expectation, explain this new pipeline and how ti meets this expectation

## Discoveries
### Input Requirements
The "preprocess.py" python script contains a function `preprocess()` that can be used to load and preprocess join trees and split trees so they are formatted in a way that TTK's merge tree clustering filter can use. The function takes in a list of the join trees and a list of split trees in that order. The order of the join tree files should match the order of the split tree files so the join and split trees at index i correspond to the trees from that same input file. The files themselves should be vtm files. These vtm files should have a corresponding directory so the file \[file_name\].vtm has the accompanying directory \[file_name\]. Within the directory will be \[file_name\]_0_0.vtu which contains the tree's nodes, \[file_name\]_1_0.vtu which contains the tree's arcs, and \[file_name\]_2_0.vti which contains the segmentation for the original input vti file.
- The nodes file should specify an unstructured grid. Depending on the datamode, the specific structure could vary; however a few things should stay consistent. Within the Piece tag NumberOfCells should be 1. 
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
    - The Cells should contain the three expected DataArrays required for UnstructuredGrids: connectivity, offsets, and types. Since this file is representing nodes, the types should all by type 2 or VTK_POLY_VERTEX. See VTK's file structure documentation for more information.
 - The arcs file should specify an unstructured grid. Depending on the datamode, the specific structure could vary; however a few things should stay consistent. It appears the number of cells is one less than the number of points
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
    - The Cells should contain the three expected DataArrays required for UnstructuredGrids: connectivity, offsets, and types. Since this file is representing arcs, the types should all by type 3 or VTK_LINE. See VTK's file structure documentation for more information.
 - The segmentation file should specify an image file. Depending on the datamode, the specific structure could vary; however a few things should stay consistent. First there is the FieldData section which appears to be copied from the original vti file. Then, there is the Piece section with PointData and CellData.
    - PointData should have the attribute Scalars="SegmentationId" and 5 DataArray tags.
        - name_of_scalar_field_merge_tree_is_computed_on (this DataArray should also be copied from the original vti file and is the scalar field that the merge tree is calculated on)
        - SegmentationId (appears to map the points to a segment)
        - RegionSize (I believe this is the number of vertex in each segment)
        - RegionSpan (unclear - related to segmentation)
        - RegionType (can be set to Min_arc, Max_arc, Saddle1_arc, Saddle2_arc, and Saddle1_saddle2_arc)
    - There should be no CellData, just an opening and closing tag
## Test Running
 - Open Paraview
 - Ensure the paths to the data
 - Run script "ideal_pre-pipeline.py"
 - Run script "new_pipeline.py"
 - Run script "original_pipeline.py"

### Explanation of output from "Test Running"
Test Running will create many files and folders. 
 - "ideal_pre-pipeline.py" will save the join trees and split trees generated for each of the individual vti files that are found in "Isabel.cdb/data". These join trees and splits trees will be found in the directory "trees/join_trees" and "trees/split_trees" respectively. These trees will be saved as a \[file_name\].vtm with an accompanying directory \[file_name\]. Within the directory will be \[file_name\]_0_0.vtu which contains the tree's nodes, \[file_name\]_1_0.vtu which contains the tree's arcs, and \[file_name\]_2_0.vti which contains the segmentation for the original input vti file.
 - "new_pipeline.py" will take the join trees and split trees created and saved above, and reformat the nodes, arcs and segmentations to be compatible with TTK's merge tree clustering filter. Then, it will save the merge tree clustering data output. This is saved to new_clustering.vtm and the actual data files will be in the directory new_clustering. The input join trees and split trees are combined to create the merge tree and those merge trees are saved as nodes and arcs. The input merge trees nodes are stored in new_clustering_\[a\]\_0.vtu where \[a\] is between 0 and 11. The arcs are stored in new_clustering_\[b\]\_0.vtu where \[b\] is between 12 and 23. The merge tree clustering was calculated with 3 centroids. The 3 cluster centroids are also merge trees represented by their nodes and arcs. The cluster centroid nodes are stored in new_clustering_\[c\]\_0.vtu where \[c\] is between 24 and 26. The cluster centroid arcs are stored in new_clustering_\[d\]\_0.vtu where \[d\] is between 27 and 29. There are also mappings between each merge tree and the centroid of the cluster they belong to. These mappings are found in new_clustering_\[e\]\_0.vtu where \[e\] is between 30 and 41. 
 - "original_pipeline.py" will take Isabel.cdb as an input. After creating join trees and split trees from the database, it will input the trees to the TTK's merge tree clustering filter. Then, it will save the merge tree clustering data output. This is saved to original_clustering.vtm and the actual data files will be in the directory original_clustering. The input join trees and split trees are combined to create the merge tree and those merge trees are saved as nodes and arcs. The input merge trees nodes are stored in original_clustering_\[a\]\_0.vtu where \[a\] is between 0 and 11. The arcs are stored in original_clustering_\[b\]\_0.vtu where \[b\] is between 12 and 23. The merge tree clustering was calculated with 3 centroids. The 3 cluster centroids are also merge trees represented by their nodes and arcs. The cluster centroid nodes are stored in original_clustering_\[c\]\_0.vtu where \[c\] is between 24 and 26. The cluster centroid arcs are stored in original_clustering_\[d\]\_0.vtu where \[d\] is between 27 and 29. There are also mappings between each merge tree and the centroid of the cluster they belong to. These mappings are found in original_clustering_\[e\]\_0.vtu where \[e\] is between 30 and 41. 

### Other files of note
There are four files and directories not produced by the test running pipeline. That would be join_tree_single.vtm, join_tree_db.vtm, split_tree_single.vtm, and split_tree_db.vtm. These were used to debug the differences found between the clustered merge tree output produced by new_pipeline.py and original_pipeline.py. 
 - join_tree_single.vtm is the paraview multiblock save file for the grouped join trees created by loading in each of the 12 individual vti image files, performing a join tree on them, saving each individual join tree, reloading the saved join trees, using "Group Dataset" to group all the nodes, all the arcs, and all the segments with each other, and then using "Group Dataset" again to group the grouped nodes, arcs, and segments into a final multiblock datset. 
 - join_tree_db.vtm is the paraview multiblock save file for the grouped join trees created by loading the Isabel.cdb database, performing a join tree on it, and then using "Group Dataset" on the nodes, arcs, and segments. 
