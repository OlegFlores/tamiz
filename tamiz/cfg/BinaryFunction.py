from __future__ import annotations
from typing import Dict, List
from collections import Counter
import networkx as nx
from networkx import DiGraph
from .BasicBlock import BasicBlock
from .InstructionCategory import InstructionCategory
from .storage.FunctionInfo import FunctionInfo
from .storage.BasicBlockInfo import BasicBlockInfo
import json


def _convert_graph_to_json(local_edg: DiGraph) -> str:
    data = nx.node_link_data(local_edg)
    json_str = json.dumps(data)
    return json_str


def _restore_graph_from_json(graph_json: str) -> DiGraph:
    graph_dict = json.loads(graph_json)
    graph = nx.node_link_graph(graph_dict)
    return graph


def _calc_instructions_stats(blocks: Dict[int, BasicBlock]) -> tuple[
    int, Dict[int, int], Dict[InstructionCategory, int]]:
    """
    Calculates instructions number in all the blocks and in each one individually.
    Returns:
        tuple of:
        int - overall blocks number;
        Dict[int,int] - dictionary of block address to instructions count in the block.
        Dict[InstructionCategory,int] - dictionary of InstructionCategory to instructions count in the block.
    """
    n_instructions = 0
    n_instructions_per_block = {}
    instruction_categories: Dict[InstructionCategory, int] = {
        InstructionCategory.DATA_TRANSFER: 0,
        InstructionCategory.ARITHMETIC: 0,
        InstructionCategory.LOGICAL: 0,
        InstructionCategory.STRING: 0,
        InstructionCategory.OTHER: 0,
    }
    for b_addr in blocks.keys():
        block = blocks[b_addr]
        curr_b_ins_n = len(block.instructions)
        instruction_categories = dict(Counter(instruction_categories) + Counter(block.instruction_categories))
        n_instructions += curr_b_ins_n
        n_instructions_per_block[b_addr] = curr_b_ins_n

    for i_category in InstructionCategory:
        if i_category not in instruction_categories:
            instruction_categories[i_category] = 0

    return n_instructions, n_instructions_per_block, instruction_categories


def _simplify_function_graph(parsed_graph: DiGraph) -> DiGraph:
    """

    Args:
        parsed_graph:

    Returns: simplified graph. Each node representing a basic block separated by capstone during the parsing,
    contains a single attribute `address` which is the address of the corresponding basic block

    """
    function_efg = nx.DiGraph()
    for n1, n2 in parsed_graph.edges:
        addr1 = n1.addr
        addr2 = n2.addr
        function_efg.add_node(addr1)
        function_efg.add_node(addr2)
        function_efg.add_edge(addr1, addr2)
    return function_efg


class BinaryFunction:
    __slots__ = (
        "function_graph",
        "function_name",
        "first_address",
        "blocks",
        "n_instructions",
        "n_instructions_per_block",
        "instruction_categories"
    )

    @classmethod
    def get_new_from_serialized(cls, function_info: FunctionInfo, blocks: List[BasicBlockInfo]) -> 'BinaryFunction':
        # print(f'BinaryFunction.getNewFromSerialized func@{hex(function_info.first_addr)} len(blocks)={len(blocks)}')
        function_graph = _restore_graph_from_json(function_info.function_graph_json)
        binary_blocks: dict[int, BasicBlock] = {bi.address: BasicBlock.get_new_from_serialized(basic_block_info=bi) for
                                                bi in blocks}
        n_instructions_per_block = {bi.address: bi.n_instructions for bi in blocks}
        instruction_categories: Dict[InstructionCategory, int] = {
            InstructionCategory.DATA_TRANSFER: function_info.n_instr_data,
            InstructionCategory.ARITHMETIC: function_info.n_instr_arithm,
            InstructionCategory.LOGICAL: function_info.n_instr_logic,
            InstructionCategory.STRING: function_info.n_instr_string,
            InstructionCategory.OTHER: function_info.n_instr_other,
        }
        return cls(
            function_graph=function_graph,
            function_name=function_info.function_name,
            blocks=binary_blocks,
            first_address=function_info.first_addr,
            n_instructions=function_info.n_instructions,
            n_instructions_per_block=n_instructions_per_block,
            instruction_categories=instruction_categories,
        )

    @classmethod
    def get_new_from_parsed_data(cls,
                                 angr_func_graph: DiGraph,
                                 function_name: str,
                                 blocks: Dict[int, BasicBlock],
                                 first_address: int,
                                 ) -> 'BinaryFunction':
        function_graph: DiGraph = _simplify_function_graph(angr_func_graph)
        if first_address is None:
            raise Exception('No first node in the graph')
        n_instructions, n_instructions_per_block, instruction_categories = _calc_instructions_stats(blocks)
        return cls(
            function_graph=function_graph,
            function_name=function_name,
            blocks=blocks,
            first_address=first_address,
            n_instructions=n_instructions,
            n_instructions_per_block=n_instructions_per_block,
            instruction_categories=instruction_categories,
        )

    def __init__(self,
                 function_graph: DiGraph,
                 function_name: str,
                 blocks: Dict[int, BasicBlock],
                 first_address: int,
                 n_instructions: int,
                 n_instructions_per_block: Dict[int, int],
                 instruction_categories: Dict[InstructionCategory, int],
                 ):
        self.function_graph: DiGraph = function_graph
        self.function_name: str = function_name
        self.blocks: Dict[int, BasicBlock] = blocks
        self.first_address: int = first_address
        self.n_instructions = n_instructions
        self.n_instructions_per_block = n_instructions_per_block
        self.instruction_categories = instruction_categories

    @property
    def function_info(self) -> FunctionInfo:
        fi = FunctionInfo()
        fi.id = None
        fi.file_id = None
        fi.function_graph_json = _convert_graph_to_json(self.function_graph)
        fi.function_name = self.function_name
        fi.first_addr = self.first_address
        fi.n_instructions = self.n_instructions
        fi.n_instr_data = self.instruction_categories.get(InstructionCategory.DATA_TRANSFER)
        fi.n_instr_arithm = self.instruction_categories.get(InstructionCategory.ARITHMETIC)
        fi.n_instr_logic = self.instruction_categories.get(InstructionCategory.LOGICAL)
        fi.n_instr_string = self.instruction_categories.get(InstructionCategory.STRING)
        fi.n_instr_other = self.instruction_categories.get(InstructionCategory.OTHER)
        return fi

    def text_summary(self):
        return f"""Function `{self.function_name} @ {hex(self.first_address)}`,
            having {len(self.blocks)} blocks,
            {self.n_instructions} instructions in total,
            instructions per blocks: {self.n_instructions_per_block}
            instructions per categories: {self.instruction_categories}
        """
