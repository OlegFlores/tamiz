from sqlite3 import Connection
from typing import Dict

from tamiz.cfg.storage.BasicBlockInfo import BasicBlockInfo


class BasicBlockStorage:
    __slots__ = (
        "_connection",
        "_table_name",
        "_functions_table_name"
    )

    def __init__(self, connection: Connection, table_name: str, functions_table_name: str):
        self._connection = connection
        self._table_name = table_name
        self._functions_table_name = functions_table_name

    def create_table(self):
        cursor = self._connection.cursor()
        fields = [
            "id INTEGER PRIMARY KEY",
            "file_id INTEGER",
            "function_id INTEGER",
            "address INT",
            "instructions_json TEXT",
            "local_edg_json TEXT",
            "edg_id_sequence TEXT",
            "has_unambiguous_id_sequence BOOLEAN",
            "n_instructions INT",
            "n_instr_data INT",
            "n_instr_arithm INT",
            "n_instr_logic INT",
            "n_instr_string INT",
            "n_instr_other INT",
            f"FOREIGN KEY(function_id) REFERENCES {self._functions_table_name}(id)",
        ]
        sql = (
            f"CREATE TABLE IF NOT EXISTS  {self._table_name} "
            f"({', '.join(fields)})"
        )
        # print(f'sql {sql}')
        cursor.execute(sql)
        self._connection.commit()

    def save_basic_block(self, file_id: int, function_id: int, basic_block_info: BasicBlockInfo) -> BasicBlockInfo:
        bi = basic_block_info
        cursor = self._connection.cursor()
        sql = f"INSERT INTO {self._table_name} " \
              f"(file_id, function_id, address, instructions_json, local_edg_json," \
              f" edg_id_sequence, has_unambiguous_id_sequence, n_instructions, n_instr_data," \
              f" n_instr_arithm, n_instr_logic, n_instr_string, n_instr_other) " \
              f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, (
            file_id, function_id, bi.address, bi.instructions_json, bi.local_edg_json,
            bi.edg_id_sequence, bi.has_unambiguous_id_sequence, bi.n_instructions,
            bi.n_instr_data, bi.n_instr_arithm, bi.n_instr_logic, bi.n_instr_string, bi.n_instr_other))
        self._connection.commit()
        bi.id = cursor.lastrowid
        return bi

    def find_basic_blocks(self, file_id: int = None, function_id: int = None) -> Dict[int, BasicBlockInfo]:
        """

        Args: 1 or 2 parameters should be passed
            file_id: file id in the DB table
            function_id: function id in the DB table (optional)

        Returns: a dict: function id (`id` column in functions table) to a list of corresponding basic blocks

        """
        cursor = self._connection.cursor()
        where_clauses = []
        sql_binding = ()
        if file_id is not None:
            where_clauses.append('file_id = ?')
            sql_binding += (file_id,)
        if function_id is not None:
            where_clauses.append('function_id = ?')
            sql_binding += (function_id,)
        if len(where_clauses) == 0:
            raise ValueError("The 'file_id' and 'function_id' parameters were not passed.")

        where_stmnt = ' AND '.join(where_clauses)
        sql = f'SELECT * FROM {self._table_name} WHERE {where_stmnt}'
        # print(f'Requesting with sql: {sql}')
        cursor.execute(sql, sql_binding)
        fetched_blocks = cursor.fetchall()
        func_id_to_bb_list: Dict[int, BasicBlockInfo] = dict()
        for fetched_block in fetched_blocks:
            bb_info = BasicBlockInfo()
            bb_info.id = fetched_block['id']
            bb_info.function_id = fetched_block['function_id']
            bb_info.file_id = fetched_block['file_id']
            bb_info.address = fetched_block['address']
            bb_info.instructions_json = fetched_block['instructions_json']
            bb_info.local_edg_json = fetched_block['local_edg_json']
            bb_info.edg_id_sequence = fetched_block['edg_id_sequence']
            bb_info.has_unambiguous_id_sequence = fetched_block['has_unambiguous_id_sequence']
            bb_info.n_instructions = fetched_block['n_instructions']
            bb_info.n_instr_data = fetched_block['n_instr_data']
            bb_info.n_instr_arithm = fetched_block['n_instr_arithm']
            bb_info.n_instr_logic = fetched_block['n_instr_logic']
            bb_info.n_instr_string = fetched_block['n_instr_string']
            bb_info.n_instr_other = fetched_block['n_instr_other']
            func_blocks = func_id_to_bb_list.get(bb_info.function_id, [])
            func_blocks.append(bb_info)
            func_id_to_bb_list[bb_info.function_id] = func_blocks
        return func_id_to_bb_list
