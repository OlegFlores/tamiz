# Algorithm for Validating an Identification Result
from typing import List, Dict, Set, TypedDict, Union, Iterable
import networkx as nx
from .consts import CORRESPONDS_TO_PROPERTY_NAME, HASH_PROPERTY_NAME, \
    InstructionNodeDict, MNEMONIC_PROPERTY_NAME
from .match.BlockMatch import BlockMatch
from .match.MatchAccuracy import MatchAccuracy
from .match.IdSequenceMatch import IdSequenceMatch
from networkx import DiGraph
from tamiz.cfg.BinaryFunction import BinaryFunction
from tamiz.cfg.BasicBlock import BasicBlock
from networkx.algorithms import isomorphism

def is_found_subgraph_valid(superfunction: BinaryFunction, subfunction: BinaryFunction,
                            graph_candidate: DiGraph) -> bool:
    """
    Algorithm 5
    Args:
        superfunction:
        subfunction:
        graph_candidate:

    Returns: True if `reduced_subgraph` can be outlined, False otherwise
    """
    head_nodes = [node for node in graph_candidate.nodes if graph_candidate.in_degree(node) == 0]
    body_blocks = [node for node in graph_candidate.nodes if
                   graph_candidate.in_degree(node) > 0 and graph_candidate.out_degree(node) > 0]
    tail_nodes = [node for node in graph_candidate.nodes if graph_candidate.out_degree(node) == 0]

    block_matches: List[BlockMatch] = []

    for sup_block_addr in head_nodes:
        sup_block = superfunction.blocks.get(sup_block_addr)
        sub_block_addr = graph_candidate.nodes[sup_block_addr].get(CORRESPONDS_TO_PROPERTY_NAME)
        sub_block = subfunction.blocks.get(sub_block_addr)
        head_blocks_matches = find_matches_for_blocks(sup_block, sub_block)
        if len(head_blocks_matches) == 0:
            print(f'No obligatory matches found for the head block pair {hex(sup_block_addr)} -> {hex(sub_block_addr)}')
            return False
        block_matches.extend(head_blocks_matches)

    for sup_block_addr in body_blocks:
        sup_block = superfunction.blocks.get(sup_block_addr)
        sub_block_addr = graph_candidate.nodes[sup_block_addr].get(CORRESPONDS_TO_PROPERTY_NAME)
        sub_block = subfunction.blocks.get(sub_block_addr)
        body_block_match = BlockMatch(sup_block_addr=sup_block_addr, sub_block_addr=sub_block_addr)
        body_block_match.match_accuracy = MatchAccuracy.HIGH
        body_block_match.id_sequence_match = IdSequenceMatch(sup_block_id_sequence=sup_block.edg_id_sequence,
                                                             sub_block_id_sequence=sub_block.edg_id_sequence)
        block_matches.append(body_block_match)


    for sup_block_addr in tail_nodes:
        sup_block = superfunction.blocks.get(sup_block_addr)
        sub_block_addr = graph_candidate.nodes[sup_block_addr].get(CORRESPONDS_TO_PROPERTY_NAME)
        sub_block = subfunction.blocks.get(sub_block_addr)
        tail_blocks_matches = find_matches_for_blocks(sup_block, sub_block)
        if len(tail_blocks_matches) == 0:
            print(f'No obligatory matches found for the tail block pair {hex(sup_block_addr)} -> {hex(sub_block_addr)}')
            return False
        block_matches.extend(tail_blocks_matches)

    if len(block_matches) > 0:
        print(f'Found isomorphic paths in the blocks')
        for i, block_match in enumerate(block_matches):
            print(block_match)
        return True
    else:
        return False



def find_matches_for_blocks(sup_block: BasicBlock, sub_block: BasicBlock) -> List[BlockMatch]:
    """
    Encontrar
    Args:
        sup_block:
        sub_block:

    Returns: a subgraph in supergraph (if found) that is isomorphic to the `searched_subgraph`
    The nodes (=instructions) are compared by its hash id

    """
    supergraph = sup_block.local_edg
    searched_subgraph = sub_block.local_edg
    NodeArgument = Dict[str, any]

    def _node_match(node_sup: NodeArgument, node_sub: NodeArgument) -> bool:
        hash_sup = node_sup.get(HASH_PROPERTY_NAME)
        hash_sub = node_sub.get(HASH_PROPERTY_NAME)
        # if hash_sup == hash_sub:
        #     print(f'{node_sup.get(MNEMONIC_PROPERTY_NAME)} => {node_sub.get(MNEMONIC_PROPERTY_NAME)}')
        #     print(f'\t{node_sup.get(HASH_PROPERTY_NAME)} => {node_sub.get(HASH_PROPERTY_NAME)}')
        # else:
        #     print(f'{node_sup.get(MNEMONIC_PROPERTY_NAME)} != {node_sub.get(MNEMONIC_PROPERTY_NAME)}')
        #     print(f'\t{node_sup.get(HASH_PROPERTY_NAME)} != {node_sub.get(HASH_PROPERTY_NAME)}')
        return hash_sup == hash_sub
    matcher = isomorphism.MultiDiGraphMatcher(G1=supergraph, G2=searched_subgraph, node_match=_node_match)
    matches: List[BlockMatch] = []
    are_subgraph_isomorphic = matcher.subgraph_is_isomorphic()
    if not are_subgraph_isomorphic:
        return matches
    for match in matcher.subgraph_isomorphisms_iter():
        block_match = BlockMatch(sup_block_addr=sup_block.address, sub_block_addr=sub_block.address)
        block_match.match_accuracy = MatchAccuracy.MEDIMUM
        for sup_instr_addr in match.keys():
            sup_node: InstructionNodeDict = supergraph.nodes[sup_instr_addr]
            sub_node: InstructionNodeDict = searched_subgraph.nodes[match.get(sup_instr_addr)]
            block_match.add_instruction_match(sup_addr=sup_node['addr'], sup_mnemonic=sup_node['mnemonic'],
                                              sub_addr=sub_node['addr'], sub_mnemonic=sub_node['mnemonic'])
        matches.append(block_match)
    return matches
