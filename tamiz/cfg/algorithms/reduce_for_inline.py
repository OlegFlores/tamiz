from typing import List
from networkx import DiGraph, has_path
from .reduce import reduce
from tamiz.cfg.BinaryFunction import BinaryFunction
from .list_includes import list_includes


def reduce_for_inline(function1: BinaryFunction, function2: BinaryFunction) -> DiGraph:
    """
    Algorithm 3
    :param function1:
    :param function2:
    :return:
    """
    graph1 = function1.function_graph  # G1 in Algorithm 3
    blocks1 = function1.blocks  # blocks dictionary (addr -> block), corresponds to G1
    graph2 = function2.function_graph  # G2 in Algorithm 3
    blocks2 = function2.blocks  # blocks dictionary (addr -> block), corresponds to G2
    marked_blocks_set = set()  # C in Algorithm 3
    heads_set = set()  # H in Algorithm 3. In our implementation contains addresses  of the blocks
    tails_set = set()  # T in Algorithm 3. In our implementation contains addresses  of the blocks
    found = False
    # 1. Assume all local EFGs in G1 are reducible
    marked_blocks_set.update({b.address for b in blocks1.values() if b.has_unambiguous_id_sequence})
    # 2. Identify head blocks of G1
    g2_head_nodes = {node for node, in_degree in graph2.in_degree() if in_degree == 0}
    g1_nodes = graph1.nodes
    for h in g2_head_nodes:  # h equals address of a basic block in graph 2
        h_id_seq = blocks2[h].edg_id_sequence
        for b in g1_nodes:  # b equals address of a basic block in graph 1
            b_id_seq = blocks1[b].edg_id_sequence
            if list_includes(superlist=b_id_seq, sublist=h_id_seq):
                found = True
                heads_set.add(b)
    if len(g2_head_nodes) > 0 and not found:
        return None
    # 3. Identify the tail blocks in G1
    g2_tail_nodes = {node for node, in_degree in graph2.out_degree() if in_degree == 0}
    if len(blocks2) > 2:
        found = False
        for t in g2_tail_nodes:  # t equals address of a basic block in graph 2
            t_id_seq = blocks2[t].edg_id_sequence
            for b in g1_nodes:  # b equals address of a basic block in graph 1
                b_id_seq = blocks1[b].edg_id_sequence
                if list_includes(superlist=b_id_seq, sublist=t_id_seq):
                    found = True
                    tails_set.add(b)
        if len(g2_tail_nodes) > 0 and not found:
            return None
    # 4. Reduce isolated head and tail blocks in G1
    if len(g2_head_nodes) > 0 and len(g2_tail_nodes) > 0:
        found = False
        for h in heads_set:
            for t in tails_set:
                # not clear what does it mean that the nodes are connected?
                # if graph1.has_edge(h, t):  # if they are adjacent
                if has_path(graph1, source=h, target=t):  # or if they have a path between them
                    marked_blocks_set.discard(h)  # removes or does nothing if not found
                    marked_blocks_set.discard(t)
                    found = True
        if not found:
            return None
    return reduce(function1, marked_blocks_set)
