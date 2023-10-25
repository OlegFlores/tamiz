import json
import zlib
from enum import Enum
from typing import Tuple, Set

from capstone import CsInsn, CS_AC_READ, CS_AC_WRITE
from capstone.x86_const import X86_REG_RAX

from .InstructionCategory import InstructionCategory

from capstone.x86_const import \
    X86_OP_REG, \
    X86_OP_IMM, \
    X86_OP_MEM, \
    X86_OP_INVALID


CAT_DATA_TRANSFER_INSTR = {"MOV", "CMOV", "XCHG", "PUSH", "POP", "LEA", "LDS", "LES", "LFS", "LGS", "LSS",
                           "LAHF", "SAHF", "PUSHF", "POPF", "MOVSX", "MOVZX", "MOVSXD", "MOVSB", "MOVSW",
                           "MOVSD", "MOVSW", "MOVSQ", "XLAT", "IN", "OUT", "LTR", "VERR", "VERW",
                           "SMSW", "LMSW", "INVLPG", "LGDT", "SGDT", "LLDT", "SLDT", "LIDT", "SIDT", "LTR",
                           "VERR", "VERW", "MOVNTI", "MOVNTQ", "MOVNTDQ", "MOVNTSS", "MOVNTSD", "CLFLUSH",
                           "CLFLUSHOPT", "LFENCE", "MFENCE", "SFENCE", "POPCNT", "POPCNT", }
CAT_ARITHM_INSTR = {"ADD", "SUB", "ADC", "SBB", "INC", "DEC", "NEG", "MUL", "IMUL", "DIV", "IDIV", "DAA",
                    "DAS", "AAA", "AAS", "AAM", "AAD", "CBW", "CWDE", "CDQE", "CWD", "CDQ", "CQO",
                    "SHL", "SAL", "SHR", "SAR", "RCL", "RCR", "ROL", "ROR",
                    "BSF", "BSR", "CMC", "CLC", "STC", "CLD", "STD", "CLI",
                    "STI", "CMC", "CLC", "STC", "CLD", "STD", "CLI", "STI", }
CAT_LOGICAL_INSTR = {"AND", "OR", "XOR", "NOT", "TEST", "BT", "BTS", "BTR", "BTC", "SETcc", }
CAT_STRING_INSTR = {"MOVS", "MOVSB", "MOVSW", "MOVSD", "MOVSQ", "LODS", "STOS", "CMPS", "SCAS", "INS", "OUTS", "REP",
                    "REPE", "REPZ", "REPNE", "REPNZ", }

CTI_INSTR = {"SYSCALL", "CALL", "RET", "LOOP", "LOOPZ", "LOOPE", "LOOPNZ", "LOOPNE", "IRET", "INT", "INTO", "BOUND",
             "ENTER", "LEAVE"}

CET_INSTR = {"ENDBR32", "ENDBR64"}


def _normalized_operands(operands_simplified: list[str]):
    op_type_d = {
        'N': 0,
        'R': 1,
        'M': 4,
        'I': 5
    }
    ops_d = dict(enumerate(operands_simplified))
    first_op = ops_d.get(0, 'N')  # N is for None
    secnd_op = ops_d.get(1, 'N')

    first_op_int = op_type_d.get(first_op[0]) << 4
    secnd_op_int = op_type_d.get(secnd_op[0])

    # TODO: add check for the third operand

    res = first_op_int + secnd_op_int

    if res == 0x11:
        if first_op != secnd_op:
            res = 0x21

    return res


def extract_map_read_written_resources(insn: CsInsn) -> Tuple[Set[str], Set[str]]:
    read_memory = False
    written_memory = False

    for op in insn.operands:
        if op.type == X86_OP_MEM:  # Memory operand
            if op.access == CS_AC_READ:
                read_memory = True
            if op.access == CS_AC_WRITE:
                written_memory = True

    regs_read, regs_written = insn.regs_access()
    str_read, str_write = {insn.reg_name(r) for r in regs_read}, {insn.reg_name(r) for r in regs_written}
    if read_memory:
        str_read.add('MEM')
    if written_memory:
        str_write.add('MEM')
    return str_read, str_write


def _map_operand(ins_operand):
    if ins_operand.type == X86_OP_REG:
        return f"R{ins_operand.value.reg}"
    if ins_operand.type == X86_OP_IMM:
        # or ins_operand.type == ARM64_OP_CIMM:
        return 'I'
    if ins_operand.type == X86_OP_MEM:
        return 'M'
    return "not supported"


def _map_mnemonic(insn: CsInsn):
    opcode_hash = zlib.crc32(bytes(insn.opcode)) & 0xFFFF
    operands = _normalized_operands(map(_map_operand, insn.operands))
    opcode_id = opcode_hash | operands << 16
    return f"{hex(opcode_id)}"


def _map_instr_category(mnemonic: str) -> InstructionCategory:
    mnemonic_upper = mnemonic.upper()
    if mnemonic_upper in CAT_DATA_TRANSFER_INSTR:
        return InstructionCategory.DATA_TRANSFER
    if mnemonic_upper in CAT_ARITHM_INSTR:
        return InstructionCategory.ARITHMETIC
    if mnemonic_upper in CAT_LOGICAL_INSTR:
        return InstructionCategory.LOGICAL
    if mnemonic_upper in CAT_STRING_INSTR:
        return InstructionCategory.STRING
    return InstructionCategory.OTHER


def is_control_transfer_instr(insn: CsInsn) -> bool:
    mnemonic: str = str(insn.mnemonic).upper()
    return mnemonic.startswith('J') or mnemonic in CTI_INSTR


def is_control_transfer_enforcement_instr(insn: CsInsn) -> bool:
    mnemonic: str = str(insn.mnemonic).upper()
    return mnemonic in CET_INSTR



class Instruction:
    __slots__ = (
        "addr",
        "type",
        "resources_read",  # a set of registers and memory read within the instruction (impl & expl)
        "resources_written",  # a set of registers and memory written within the instruction (impl & expl)
        "goes_after",  # when comparing 2 instructions, this one goes after (CTI like JMP, CALL, RET, etc...)
        "goes_before",  # when comparing 2 instructions, this one goes before (CET like ENDBR32, ENDBR64)
        "ins_hash",
        "is_functional",
        "is_in_body",
        "text",
        "category"
    )

    def __init__(self, cs_insn: CsInsn):
        addr: int = cs_insn.address
        mnemonic = cs_insn.mnemonic
        ops = cs_insn.op_str
        # ops = ','.join([instr_op.strip() for instr_op in str(cs_insn.op_str).split(',')[::-1]])

        ins_hash = _map_mnemonic(cs_insn)
        text_instruction = "%s %s" % (mnemonic, ops)
        self.addr: int = addr
        self.type = 'type'
        self.resources_read, self.resources_written = extract_map_read_written_resources(cs_insn)
        self.goes_after = is_control_transfer_instr(cs_insn)
        self.goes_before = is_control_transfer_enforcement_instr(cs_insn)
        self.ins_hash = ins_hash
        self.is_functional = Instruction._is_functional_instruction(cs_insn)
        self.is_in_body = Instruction._is_function_body_instruction(cs_insn)
        self.text = text_instruction
        self.category = _map_instr_category(cs_insn.mnemonic)

    @staticmethod
    def _is_functional_instruction(cs_insn: CsInsn) -> bool:
        # List of meaningless instructions and alignment instructions
        meaningless_instructions = ["nop"]
        # Check if the instruction mnemonic is in the list of meaningless instructions
        if cs_insn.mnemonic in meaningless_instructions:
            return False
        return True


    @staticmethod
    def _is_function_body_instruction(cs_insn: CsInsn) -> bool:
        def _is_instruction(cs_insn: CsInsn, mnemonic: str, op_str: str) -> bool:
            return cs_insn.mnemonic == mnemonic and cs_insn.op_str == op_str
        # List of x86-64 ABI prologue/epilogue instructions
        prologue_instructions = ["enbr32", "endbr64", "enter"]
        epilogue_instructions = ["leave", "ret", "retn"]

        # Check if the instruction mnemonic is in the prologue or epilogue lists
        if cs_insn.mnemonic in prologue_instructions or cs_insn.mnemonic in epilogue_instructions:
            return False

        if _is_instruction(cs_insn, 'push', 'rbp') or \
                _is_instruction(cs_insn, 'mov', 'rbp, rsp') or \
                _is_instruction(cs_insn, 'pop', 'rbp') or \
                _is_instruction(cs_insn, 'push', 'ebp') or \
                _is_instruction(cs_insn, 'mov', 'ebp, esp') or \
                _is_instruction(cs_insn, 'pop', 'ebp'):
            return False

        return True

    def __repr__(self):
        return f"{hex(self.addr)}: {self.text} -> {self.ins_hash} (R: {', '.join(self.resources_read)}, W:{', '.join(self.resources_written)}) type:{self.type} category:{self.category}"


class InstructionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Instruction):
            instr: Instruction = obj
            return {
                "addr": instr.addr,
                # "type" not used
                "resources_read": instr.resources_read,
                "resources_written": instr.resources_written,
                "goes_after": instr.goes_after,
                "goes_before": instr.goes_before,
                "ins_hash": instr.ins_hash,
                "is_functional": instr.is_functional,
                "is_in_body": instr.is_in_body,
                "text": instr.text,
                "category": instr.category
            }
        return super().default(obj)

# def instruction_decoder(obj: Dict[str, str]) -> Instruction:
#     if 'name' in obj and 'age' in obj and 'city' in obj:
#         return Person(obj['name'], obj['age'], obj['city'])
#     return obj