# Reduced EFG
from typing import TypedDict, Union

# For both basic block and instruction:
ADDRESS_PROPERTY_NAME = 'addr'
# For basic blocks in function graph:
REDUCED_PROPERTY_NAME = 'reduced_to'

# Local EDG, nodes attributes:
HASH_PROPERTY_NAME = 'hash'
MNEMONIC_PROPERTY_NAME = 'mnemonic'
FUNCTIONAL_PROPERTY_NAME = 'functional'

# Isomorphic graph results
CORRESPONDS_TO_PROPERTY_NAME = 'corresponds_to'


class InstructionNodeDict(TypedDict):
    addr: Union[str, int]
    hash: Union[str, int]
    mnemonic: Union[str, int]
    functional: Union[str, int]
