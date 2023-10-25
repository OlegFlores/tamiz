from typing import List

import numpy as np
import networkx as nx
import json
from networkx import DiGraph

from tamiz.cfg.Instruction import Instruction


def _instructions_dependant(instr1: Instruction, instr2: Instruction) -> bool:
    read1 = instr1.resources_read
    written1 = instr1.resources_written
    read2 = instr2.resources_read
    written2 = instr2.resources_written
    dependency_cases = [
        instr1.goes_before,
        len(written1.intersection(read2)) > 0,
        len(read1.intersection(written2)) > 0,
        len(written1.intersection(written2)) > 0,
        instr2.goes_after
    ]
    if True in dependency_cases:
        return True
    else:
        return False


def is_functional_instruction(instruction: Instruction) -> bool:
    """
    Filter out:
        - prologue
        - epilogue
        - NOPs
        - meaningless instructions
    Args:
        instruction:

    Returns:

    """
    pass


def build_local_efg(instructions: list[Instruction]) -> DiGraph:
    """
    Algorithm 1. Algorithm to Construct a Local EFG
    alg:build_local_efg

    Args:
        instructions:

    Returns: DiGraph instance
    """
    local_edg = nx.DiGraph()
    n_nodes = len(instructions)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            instr1 = instructions[i]
            instr2 = instructions[j]
            if _instructions_dependant(instr1=instr1, instr2=instr2):
                instr1_is_functional = instr1.is_functional and instr1.is_in_body
                instr2_is_functional = instr2.is_functional and instr2.is_in_body
                if instr1_is_functional:
                    local_edg.add_node(i, hash=instr1.ins_hash,
                                       mnemonic=instr1.text,
                                       functional=instr1_is_functional,
                                       addr=instr1.addr)
                if instr2_is_functional:
                    local_edg.add_node(j, hash=instr2.ins_hash,
                                       mnemonic=instr2.text,
                                       functional=instr2_is_functional,
                                       addr=instr2.addr)
                if instr1_is_functional and instr2_is_functional:
                    local_edg.add_edge(i, j)
    for i in range(n_nodes):
        for j in range(i + 2, n_nodes):
            if local_edg.has_edge(i, j):
                for k in range(i + 1, j):
                    instr_i = instructions[i]
                    instr_k = instructions[k]
                    instr_j = instructions[j]
                    if _instructions_dependant(instr1=instr_i, instr2=instr_k) \
                            and _instructions_dependant(instr1=instr_k, instr2=instr_j):
                        if local_edg.has_edge(i, j):  # the edge might have been deleted in prev iteration
                            local_edg.remove_edge(i, j)
    return local_edg


def calc_efg_id_sequence(local_efg: DiGraph) -> List[str]:
    """

    Args:
        local_efg:

    Returns:

    """
    graph = local_efg.copy()
    res: List[str] = []
    while True:
        head_nodes = [node for node, in_degree in graph.in_degree() if in_degree == 0]
        if len(head_nodes) == 0:
            break
        hashes = [graph.nodes[node].get('hash') for node in head_nodes]
        sorted_hashes = sorted(hashes)
        res.extend(sorted_hashes)
        graph.remove_nodes_from(head_nodes)
    return res


def calc_adj_matrix(graph: DiGraph) -> np.ndarray:
    """
    Calculate the ordered adjacency matrix for a directed graph.

    Parameters:
        graph (DiGraph): The directed graph.

    Returns:
        np.ndarray: The ordered adjacency matrix as a NumPy array.
    """
    adj_matrix = nx.to_numpy_array(graph, nodelist=sorted(graph.nodes()))
    return adj_matrix


def adj_matrices_equal(matrix1: np.ndarray, matrix2: np.ndarray):
    return np.array_equal(matrix1, matrix2)


def build_local_edg_and_json(instructions: list[Instruction]) -> (DiGraph, str):
    local_edg = build_local_efg(instructions)
    json_str = convert_graph_to_json(local_edg)
    return local_edg, json_str


def convert_graph_to_json(local_edg: DiGraph) -> str:
    data = nx.node_link_data(local_edg)
    json_str = json.dumps(data)
    return json_str


def parse_local_efg_from_json(json_str: str) -> DiGraph:
    graph_dict = json.loads(json_str)
    local_edg = nx.node_link_graph(graph_dict)
    return local_edg


def has_unambiguous_id_sequence(id_sequence: List[str]) -> bool:
    """
    Returns:
        True if edg_id_sequence has repeated elements
        False if every element in edg_id_sequence is unique
    """
    # TODO: check if the rule should be more narrow: only adjacent identical IDs flag ambiguity, not any repeated ID
    seen = set()
    for instruction_hash in id_sequence:
        if instruction_hash in seen:
            return False
        else:
            seen.add(instruction_hash)
    return True
