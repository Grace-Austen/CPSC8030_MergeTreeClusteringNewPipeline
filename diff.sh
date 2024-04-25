for VARIABLE in `seq 0 1 41`
do
    diff original_clustering/original_clustering_$VARIABLE\_0.vtu new_clustering/new_clustering_$VARIABLE\_0.vtu
done

for VARIABLE in `seq 0 1 35`
do
    diff join_tree_db/join_tree_db_$VARIABLE\_0.vt* join_tree_single/join_tree_single_$VARIABLE\_0.vt*
    diff split_tree_db/split_tree_db_$VARIABLE\_0.vt* split_tree_single/split_tree_single_$VARIABLE\_0.vt*
done