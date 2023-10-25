
class BasicBlockInfo:

    __slots__ = (
        "id",
        "file_id",
        "function_id",
        "address",
        "instructions_json",
        "local_edg_json",
        "edg_id_sequence",
        "has_unambiguous_id_sequence",
        "n_instructions",
        "n_instr_data",
        "n_instr_arithm",
        "n_instr_logic",
        "n_instr_string",
        "n_instr_other",
    )

    def __init__(self, ):
        self.id: int = None
        self.file_id: int = None
        self.function_id: int = None
        self.address: int = None
        self.instructions_json: str = None
        self.local_edg_json: str = None
        self.edg_id_sequence: str = None
        self.has_unambiguous_id_sequence: bool = None
        self.n_instructions: int = None
        self.n_instr_data: int = None
        self.n_instr_arithm: int = None
        self.n_instr_logic: int = None
        self.n_instr_string: int = None
        self.n_instr_other: int = None

    def text_summary(self):
        return f"""Basic block at addr {hex(self.address)},
                    having {self.n_instructions} instructions,
                    ID sequence {self.edg_id_sequence}
                """
