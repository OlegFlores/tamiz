from typing import List


class IdSequenceMatch:
    __slots__ = (
        "sup_block_id_sequence",
        "sub_block_id_sequence",
    )

    def __init__(self, sup_block_id_sequence: List[str], sub_block_id_sequence: List[str]):
        self.sup_block_id_sequence: List[str] = sup_block_id_sequence
        self.sub_block_id_sequence: List[str] = sub_block_id_sequence



    def __repr__(self):
        sup_id_seq = ','.join(self.sup_block_id_sequence)
        sub_id_seq = ','.join(self.sub_block_id_sequence)
        return f'Sup id seq {sup_id_seq} --> Sub id seq {sub_id_seq}'
