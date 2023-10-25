from typing import Iterable, TypedDict, Dict

from angr import Block
from angr.block import CapstoneBlock, CapstoneInsn
from capstone import CsInsn

from .BasicBlock import BasicBlock
from .Instruction import Instruction
from .InstructionCategory import InstructionCategory

AngrNodeArgument = TypedDict('AngrNodeArgument', addr=int, block=Block)
"""
Type hint for node passed from Angr. Should contain address offset and block: Block object
"""


def map_node_to_basic_block(node: AngrNodeArgument) -> BasicBlock:
    """
    Maps angr CFG node to internal class BasicBlock

    Args:
        node:

    Returns: BasicBlock instance
    """
    angr_block: Block = node.block
    if angr_block is None:
        return BasicBlock.get_new_from_parsed_data(address=node.addr, instructions=[], instruction_categories=dict())

    capstone_block: CapstoneBlock = angr_block.capstone
    instructions: Iterable[CapstoneInsn] = capstone_block.insns
    mapped_instructions = []
    instruction_categories: Dict[InstructionCategory, int] = {
        InstructionCategory.DATA_TRANSFER: 0,
        InstructionCategory.ARITHMETIC: 0,
        InstructionCategory.LOGICAL: 0,
        InstructionCategory.STRING: 0,
        InstructionCategory.OTHER: 0,
    }
    for instruction in instructions:
        insn: CsInsn = instruction.insn
        instruction = Instruction(insn)
        if not instruction.is_functional or not instruction.is_in_body:
            continue
        instruction_categories[instruction.category] += 1
        mapped_instructions.append(instruction)
    return BasicBlock.get_new_from_parsed_data(address=node.addr, instructions=mapped_instructions,
                                               instruction_categories=instruction_categories)
