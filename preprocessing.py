from paraview.simple import *

def preprocess(jt_files, st_files):

    if len(jt_files) > len(st_files):
        raise RuntimeError(f"More join tree files: {set(jt_files) - set(st_files)}")
    if len(jt_files) < len(st_files):
        raise RuntimeError(f"More join tree files: {set(st_files) - set(jt_files)}")

    jt_nodes = []
    jt_arcs = []
    jt_segs = []

    st_nodes = []
    st_arcs = []
    st_segs = []

    for fn in jt_files:
        base_fn = ".".join(fn.split(".")[:-1]) # cut off the .vtm
        # get nodes
        node_fn = f"{base_fn}/{base_fn}_0_0.vtu"
        jt_node = XMLUnstructuredGridReader(FileName=load_join_trees+node_fn) # u because unstructured grid, vtm is multiblock
        jt_nodes.append(jt_node)
        st_node = XMLUnstructuredGridReader(FileName=load_split_trees+node_fn) # u because unstructured grid, vtm is multiblock
        st_nodes.append(st_node)

        # get arcs
        arc_fn = f"{base_fn}/{base_fn}_1_0.vtu"
        jt_arc = XMLUnstructuredGridReader(FileName=load_join_trees+arc_fn) # u because unstructured grid, vtm is multiblock
        jt_arcs.append(jt_arc)
        st_arc = XMLUnstructuredGridReader(FileName=load_split_trees+arc_fn) # u because unstructured grid, vtm is multiblock
        st_arcs.append(st_arc)

        # get segments
        seg_fn = f"{base_fn}/{base_fn}_2_0.vti"
        jt_seg = XMLImageDataReader(FileName=load_join_trees+seg_fn)
        jt_segs.append(jt_seg)
        st_seg = XMLImageDataReader(FileName=load_split_trees+seg_fn)
        st_segs.append(st_seg)

    jt_nodes_group = GroupDatasets(registrationName='JT Skeleton Nodes', Input=jt_nodes)
    jt_arcs_group = GroupDatasets(registrationName='JT Skeleton Arcs', Input=jt_arcs)
    jt_segs_group = GroupDatasets(registrationName='JT Segmentation', Input=jt_segs)

    st_nodes_group = GroupDatasets(registrationName='ST Skeleton Nodes', Input=st_nodes)
    st_arcs_group = GroupDatasets(registrationName='ST Skeleton Arcs', Input=st_arcs)
    st_segs_group = GroupDatasets(registrationName='ST Segmentation', Input=st_segs)

    jt_group = GroupDatasets(
        registrationName='JT Trees',
        Input=[
            jt_nodes_group,
            jt_arcs_group,
            jt_segs_group
        ],
        BlockNames=["Skeleton Nodes", "Skeleton Arcs", "Segmentation"]
    )

    st_group = GroupDatasets(
        registrationName='ST Trees',
        Input=[
            st_nodes_group,
            st_arcs_group,
            st_segs_group
        ],
        BlockNames=["Skeleton Nodes", "Skeleton Arcs", "Segmentation"]
    )

    return {"Join Tree Group": jt_group, "Split Tree Group": st_group}