from typing import List
from .InstructionMatch import InstructionMatch
from .MatchAccuracy import MatchAccuracy
from .IdSequenceMatch import IdSequenceMatch


class BlockMatch:
    __slots__ = (
        "sup_block_addr",
        "sub_block_addr",
        "match_accuracy",
        "instruction_matches",
        "id_sequence_match",
    )

    def __init__(self, sup_block_addr: int, sub_block_addr: int):
        self.sup_block_addr: int = sup_block_addr
        self.sub_block_addr: int = sub_block_addr
        self.instruction_matches: List[InstructionMatch] = []
        self.match_accuracy: MatchAccuracy = None
        self.id_sequence_match: IdSequenceMatch = None

    def add_instruction_match(self, sup_addr: int, sup_mnemonic: str, sub_addr: int, sub_mnemonic: str):
        instr_match = InstructionMatch(sup_addr=sup_addr, sup_mnemonic=sup_mnemonic,
                                       sub_addr=sub_addr, sub_mnemonic=sub_mnemonic)
        self.instruction_matches.append(instr_match)



    def __repr__(self):
        instrs = '\n'.join([i_match.__repr__() for i_match in self.instruction_matches])
        res = f'= Sup block {hex(self.sup_block_addr)} ={self.match_accuracy.name}=> Sub block {hex(self.sub_block_addr)} ='
        if self.id_sequence_match:
            res += f'\n{self.id_sequence_match.__repr__()}'
        else:
            res += f'\n{instrs}'
        return res
