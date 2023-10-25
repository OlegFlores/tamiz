from typing import List
from networkx import DiGraph, has_path
from .reduce import reduce
from tamiz.cfg.BinaryFunction import BinaryFunction


def reduce_for_full(function: BinaryFunction) -> DiGraph:
    """
    Algorithm 4
    :param function:
    :return:
    """
    blocks = function.blocks  # blocks dictionary (addr -> block), corresponds to G in Algorithm 4
    marked_blocks_set = set()  # C in Algorithm 4
    marked_blocks_set.update({b.address for b in blocks.values() if b.has_unambiguous_id_sequence})
    return reduce(function, marked_blocks_set)
