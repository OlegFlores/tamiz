class FunctionInfo:
    __slots__ = (
        "id",
        "file_id",
        "function_graph_json",
        "function_name",
        "first_addr",
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
        self.function_graph_json: str = None
        self.function_name: str = None
        self.first_addr: int = None
        self.n_instructions: int = None
        self.n_instr_data: int = None
        self.n_instr_arithm: int = None
        self.n_instr_logic: int = None
        self.n_instr_string: int = None
        self.n_instr_other: int = None
