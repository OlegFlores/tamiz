from typing import Set
import networkx as nx
from networkx import DiGraph

from tamiz.cfg.BinaryFunction import BinaryFunction
from .consts import ADDRESS_PROPERTY_NAME, REDUCED_PROPERTY_NAME


def reduce(function: BinaryFunction, blocks_addrs_to_reduce: Set[int]) -> DiGraph:
    """
    Algorithm 2
    Args:
        function: BinaryFunction containing local function graph and the list of blocks
        blocks_addrs_to_reduce: int addresses of the blocks that should be reduced in the graph

    Returns:
        Graph with the nodes designated by `blocks_addrs_to_reduce`
        having an attribute `reduced_to` equal to the corresponding block's id sequence

    """
    func_graph_copy = function.function_graph.copy()  # G2(a copy of G1) in Algorithm 2
    blocks = function.blocks  # Corresponds to G1 in Algorithm 2

    attrs_to_set_reduced = {addr: blocks[addr].edg_id_sequence for addr in blocks_addrs_to_reduce}
    attrs_to_set_all = {node: node for node in func_graph_copy.nodes}

    nx.set_node_attributes(func_graph_copy, attrs_to_set_all, name=ADDRESS_PROPERTY_NAME)
    nx.set_node_attributes(func_graph_copy, attrs_to_set_reduced, name=REDUCED_PROPERTY_NAME)
    return func_graph_copy
