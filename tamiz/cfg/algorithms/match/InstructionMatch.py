

class InstructionMatch:

    __slots__ = (
        "sup_addr",
        "sup_mnemonic",
        "sub_addr",
        "sub_mnemonic",
    )

    def __init__(self, sup_addr: int, sup_mnemonic: str, sub_addr: int, sub_mnemonic: str):
        self.sup_addr = sup_addr
        self.sup_mnemonic = sup_mnemonic
        self.sub_addr = sub_addr
        self.sub_mnemonic = sub_mnemonic

    def __repr__(self):
        return f'{hex(self.sup_addr)}: {self.sup_mnemonic}\t----->\t{hex(self.sub_addr)}: {self.sub_mnemonic}'