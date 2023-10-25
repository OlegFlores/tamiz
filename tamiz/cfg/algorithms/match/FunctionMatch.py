from typing import List

from .BlockMatch import BlockMatch


class FunctionMatch:
    __slots__ = (
        "sup_function_addr",
        "sup_function_symbol",
        "sub_function_addr",
        "sub_function_symbol",
        "block_matches",
    )

    def __init__(self, sup_function_addr: int, sup_function_symbol: str,
                 sub_function_addr: int, sub_function_symbol: str,
                 block_matches: List[BlockMatch],
                 ):
        self.sup_function_addr = sup_function_addr
        self.sup_function_symbol = sup_function_symbol
        self.sub_function_addr = sub_function_addr
        self.sub_function_symbol = sub_function_symbol
        self.block_matches = []

    def add_block_match(self, block_match: BlockMatch):
        self.block_matches.append(block_match)

    def __repr__(self):
        blocks = '\n'.join([b_match.__repr__() for b_match in self.block_matches])
        return f'=== Sup function {self.sup_function_symbol}@{hex(self.sup_function_addr)} ' \
               f'matched to sub function {self.sub_function_symbol}@{hex(self.sub_function_addr)} ===\n{blocks}'
