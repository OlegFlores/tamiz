from typing import List, Dict

from networkx import DiGraph

from .consts import ADDRESS_PROPERTY_NAME, REDUCED_PROPERTY_NAME, CORRESPONDS_TO_PROPERTY_NAME
from networkx.algorithms import isomorphism
from .reduce_for_inline import reduce_for_inline
from .reduce_for_full import reduce_for_full
from .list_includes import list_includes
from tamiz.cfg.BinaryFunction import BinaryFunction

NodeArgument = Dict[str, any]


def find_isomorphic_subgraphs_candidates(superfunction: BinaryFunction, subfunction: BinaryFunction) -> set[DiGraph]:
    """

    Args:
        superfunction:
        subfunction:

    Returns: a set of graphs that represents possible block sequences in the super function
    that are isomorphic to the block sequences of the sub function.
    These are only candidates for real graph isomorphism, because head and tail blocks should be checked internally
    (should contain outlinable graphs of instructions).
    Each node of the graph is an address of the block in super function.
    Also, each node contains an attribute `corresponds_to` (use CORRESPONDS_TO_PROPERTY_NAME constant instead)
    which is an address of the block in the sub function.

    """
    superfunction_refg = reduce_for_inline(function1=superfunction, function2=subfunction)
    subfunction_refg = reduce_for_inline(function1=subfunction, function2=subfunction)
    # superfunction_refg = reduce_for_full(function=superfunction)
    # subfunction_refg = reduce_for_full(function=subfunction)
    if superfunction_refg is None or subfunction_refg is None:
        return set()
    reason: str = None
    def _node_match(node_sup: NodeArgument, node_sub: NodeArgument) -> bool:
        block_sup = superfunction.blocks[node_sup.get(ADDRESS_PROPERTY_NAME)]
        reduced_id_seq_sup = node_sup.get(REDUCED_PROPERTY_NAME, None)
        block_sub = subfunction.blocks[node_sub.get(ADDRESS_PROPERTY_NAME)]
        reduced_id_seq_sub = node_sub.get(REDUCED_PROPERTY_NAME, None)
        # BEGIN DEBUG

        # print(f'node 1:')
        # print(node_sup['addr'], node_sup.get('reduced_to', None))
        # print(f'node 2:')
        # print(node_sub['addr'], node_sub.get('reduced_to', None))
        #END DEBUG
        result = False
        # Case 1. Nodes are of different types: reduced and not reduced
        if reduced_id_seq_sup != reduced_id_seq_sub:
            reason = 'Nodes of different types: reduced and not reduced'
            result = False
        # Case 2. Both nodes are reduced
        # Need to compare ID sequences and Ordered Adjacency Matrices
        elif reduced_id_seq_sup and reduced_id_seq_sub:
            adj_matrix_sup = block_sup.adj_matrix
            adj_matrix_sub = block_sub.adj_matrix
            result = (adj_matrix_sup == adj_matrix_sub).all() and reduced_id_seq_sup == reduced_id_seq_sub
            reason = 'Result of comparing ID sequence and OAM'
        # Case 3. Both nodes are regular basic blocks with instructions' IDs.
        # We just need to ensure that the supergraph instructions include the subgraph ones.
        # This is because they may be scattered throughout the code mixed with target function instructions
        # that are not related to the library function.
        elif not reduced_id_seq_sup and not reduced_id_seq_sub:
            result = list_includes(superlist=block_sup.edg_id_sequence, sublist=block_sub.edg_id_sequence)
        # Otherwise return False
        return result

    matcher = isomorphism.DiGraphMatcher(G1=superfunction_refg, G2=subfunction_refg, node_match=_node_match)
    are_subgraph_isomorphic = matcher.subgraph_is_isomorphic()
    result_subgraphs = set()
    for match in matcher.subgraph_isomorphisms_iter():
        result_subgraph = superfunction.function_graph.subgraph(match.keys())
        for node in result_subgraph.nodes:
            isomorphic_node = match[node]  # Get the corresponding isomorphic node
            result_subgraph.nodes[node][CORRESPONDS_TO_PROPERTY_NAME] = isomorphic_node
        result_subgraphs.add(result_subgraph)
    return result_subgraphs
