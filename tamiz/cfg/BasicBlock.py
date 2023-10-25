from __future__ import annotations
import json
from networkx import DiGraph
import numpy as np

# from OperandType import OperandType
from .InstructionCategory import InstructionCategory
from typing import List, Dict
from .Instruction import Instruction
from tamiz.cfg.algorithms.local_efg import build_local_efg, convert_graph_to_json, calc_efg_id_sequence, \
    parse_local_efg_from_json, calc_adj_matrix, has_unambiguous_id_sequence as calc_if_unambiguous
from .storage.BasicBlockInfo import BasicBlockInfo


class BasicBlock:
    __slots__ = (
        "address",
        "instructions",
        "n_instructions",
        "local_edg",
        "edg_id_sequence",
        "has_unambiguous_id_sequence",
        "instruction_categories",
    )

    @classmethod
    def get_new_from_serialized(cls, basic_block_info: BasicBlockInfo) -> 'BasicBlock':
        instruction_categories: Dict[InstructionCategory, int] = {
            InstructionCategory.DATA_TRANSFER: basic_block_info.n_instr_data,
            InstructionCategory.ARITHMETIC: basic_block_info.n_instr_arithm,
            InstructionCategory.LOGICAL: basic_block_info.n_instr_logic,
            InstructionCategory.STRING: basic_block_info.n_instr_string,
            InstructionCategory.OTHER: basic_block_info.n_instr_other,
        }
        edg_id_sequence = basic_block_info.edg_id_sequence.split(',')
        flag_unambiguous_id_sequence = calc_if_unambiguous(edg_id_sequence)
        instructions = json.loads(basic_block_info.instructions_json)
        return cls(
            address=basic_block_info.address,
            local_edg=parse_local_efg_from_json(basic_block_info.local_edg_json),
            edg_id_sequence=edg_id_sequence,
            has_unambiguous_id_sequence=flag_unambiguous_id_sequence,
            instruction_categories=instruction_categories,
            n_instructions=basic_block_info.n_instructions,
            instructions=instructions,
        )

    @classmethod
    def get_new_from_parsed_data(cls,
                                 address: int,
                                 instructions: List[Instruction],
                                 instruction_categories: Dict[InstructionCategory, int],
                                 ) -> 'BasicBlock':
        """

                Args:
                    address: basic block address (offset)
                    instructions: list of mapped instructions objects
                    instruction_categories: dictionary of instr category to its quantity in block
                """
        local_efg = build_local_efg(instructions)
        efg_id_sequence = calc_efg_id_sequence(local_efg)
        flag_unambiguous_id_sequence = calc_if_unambiguous(efg_id_sequence)
        return cls(
            address=address,
            local_edg=local_efg,
            edg_id_sequence=efg_id_sequence,
            has_unambiguous_id_sequence=flag_unambiguous_id_sequence,
            instruction_categories=instruction_categories,
            n_instructions=len(instructions),
            instructions=instructions,
        )

    def __init__(self,
                 address: int,
                 local_edg: DiGraph,
                 edg_id_sequence: List[str],
                 has_unambiguous_id_sequence: bool,
                 instruction_categories: Dict[InstructionCategory, int],
                 n_instructions: int,
                 instructions: List[Instruction] = []
                 ):
        """

        Args:
            address:
                address of the first instruction in the basic block
            local_edg:
                execution dependency/flow graph of the basic block
            edg_id_sequence:
                sequence of hashes(IDs) of all the instructions in the block
            has_unambiguous_id_sequence:
                if any of edg_id_sequence ID is repeated
            instruction_categories:
                dictionary, category to the number of instructions in the category
            n_instructions:
                number of all instructions in the block
            instructions:
                list of instruction objects
        """
        self.address: int = address
        self.local_edg: DiGraph = local_edg
        self.edg_id_sequence: List[str] = edg_id_sequence
        self.has_unambiguous_id_sequence = has_unambiguous_id_sequence
        self.instruction_categories = instruction_categories
        # n_instructions is stored in the database,
        # and it equals the original number of instruction in the block
        # (before any optimization, right after the disassembling)
        self.n_instructions = n_instructions
        # instructions are only set after parsing the data
        # not relevant when restoring from the database, bk they are not stored
        self.instructions: List[Instruction] = instructions

    def basic_block_info(self, ) -> BasicBlockInfo:
        bb_info = BasicBlockInfo()
        bb_info.address = self.address
        bb_info.instructions_json = '[]' # json.dumps(self.instructions, cls=InstructionEncoder)
        bb_info.local_edg_json = convert_graph_to_json(self.local_edg)
        bb_info.edg_id_sequence = ','.join(self.edg_id_sequence)
        bb_info.has_unambiguous_id_sequence = self.has_unambiguous_id_sequence
        bb_info.n_instructions = self.n_instructions
        bb_info.n_instr_data = self.instruction_categories.get(InstructionCategory.DATA_TRANSFER)
        bb_info.n_instr_arithm = self.instruction_categories.get(InstructionCategory.ARITHMETIC)
        bb_info.n_instr_logic = self.instruction_categories.get(InstructionCategory.LOGICAL)
        bb_info.n_instr_string = self.instruction_categories.get(InstructionCategory.STRING)
        bb_info.n_instr_other = self.instruction_categories.get(InstructionCategory.OTHER)
        return bb_info

    def __repr__(self):
        instructions_repr = '\n'.join(instr.__repr__() for instr in self.instructions)
        return f"Address: {self.address}\nInstructions:\n{instructions_repr}"

    @property
    def adj_matrix(self) -> np.ndarray:
        return calc_adj_matrix(self.local_edg)
