from typing import List, Iterable, Dict, Tuple
from angr.knowledge_plugins import Function
from angr.codenode import BlockNode
from angr import Project

from .BasicBlock import BasicBlock
from .map_node_to_basic_block import map_node_to_basic_block
from angr.analyses import CFGFast
from .BinaryFunction import BinaryFunction
from networkx.readwrite import json_graph
from networkx import DiGraph, is_isomorphic


def _map_nodes_to_basic_blocks_dict(cfg: CFGFast, nodes: Iterable[BlockNode]) -> \
        Tuple[Dict[int, BasicBlock], List[BlockNode]]:
    res_dict: Dict[int, BasicBlock] = {}
    nodes_to_remove: List[BlockNode] = []
    for node in nodes:
        bblock = map_node_to_basic_block(cfg.get_any_node(node.addr))
        if len(bblock.instructions) > 0:
            res_dict[node.addr] = bblock
        else:
            nodes_to_remove.append(node)
            # print(f'Excluding basic block @ {hex(node.addr)}, it doesn\'t have functional instructions')
    return res_dict, nodes_to_remove


def angr_extract_binary_functions(file_path: str) -> Tuple[List[BinaryFunction], CFGFast, List[DiGraph]]:
    # print('angr_extract_functions:')
    # print(file_path)
    project = Project(file_path, load_options={'auto_load_libs': False})
    cfg: CFGFast = project.analyses.CFGFast()
    funcs_dict: Dict[int, Function] = cfg.kb.functions
    res_funcs = []
    res_cfgs = []
    for func_addr in funcs_dict.keys():
        func = funcs_dict[func_addr]
        nodes: Iterable[BlockNode] = func.graph.nodes
        blocks, nodes_to_remove = _map_nodes_to_basic_blocks_dict(cfg, nodes)
        # remove empty blocks from the graph
        for node in nodes_to_remove:
            func.graph.remove_node(node)
        targ_func = BinaryFunction.get_new_from_parsed_data(angr_func_graph=func.graph,
                                                            function_name=func.name,
                                                            blocks=blocks,
                                                            first_address=func_addr)
        res_funcs.append(targ_func)
        res_cfgs.append(func.graph)
    return res_funcs, cfg, res_cfgs
