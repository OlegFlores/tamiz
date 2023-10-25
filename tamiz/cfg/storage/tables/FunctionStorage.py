from sqlite3 import Cursor, Connection
from typing import List

from tamiz.cfg.storage.FunctionInfo import FunctionInfo


class FunctionStorage:
    __slots__ = (
        "_connection",
        "_table_name",
        "_files_table_name"
    )

    def __init__(self, connection: Connection, table_name: str, files_table_name: str):
        self._connection = connection
        self._table_name = table_name
        self._files_table_name = files_table_name

    def create_table(self):
        cursor = self._connection.cursor()
        fields = [
            "id INTEGER PRIMARY KEY",
            "file_id INTEGER",
            "function_graph_json TEXT",
            "function_name TEXT",
            "first_addr INT",
            "n_instructions INT",
            "n_instr_data INT",
            "n_instr_arithm INT",
            "n_instr_logic INT",
            "n_instr_string INT",
            "n_instr_other INT",
            f"FOREIGN KEY(file_id) REFERENCES {self._files_table_name}(id)",
        ]
        sql = (
            f"CREATE TABLE IF NOT EXISTS  {self._table_name} "
            f"({', '.join(fields)})"
        )
        # print(f'sql {sql}')
        cursor.execute(sql)
        self._connection.commit()

    def save_function(self, file_id: int, function_info: FunctionInfo) -> FunctionInfo:
        fi = function_info
        cursor = self._connection.cursor()
        sql = f"INSERT INTO {self._table_name} " \
              f"(file_id, function_graph_json, function_name, first_addr, n_instructions, n_instr_data, " \
              f" n_instr_arithm, n_instr_logic, n_instr_string, n_instr_other) " \
              f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, (file_id, fi.function_graph_json, fi.function_name, fi.first_addr,
                             fi.n_instructions, fi.n_instr_data, fi.n_instr_arithm, fi.n_instr_logic,
                             fi.n_instr_string, fi.n_instr_other))
        self._connection.commit()
        fi.id = cursor.lastrowid
        return fi

    def find_functions(self, file_id: int) -> List[FunctionInfo]:
        cursor = self._connection.cursor()
        sql = f"SELECT * FROM {self._table_name} WHERE file_id = ?"
        cursor.execute(sql, (file_id,))
        result_rows = cursor.fetchall()
        function_infos: List[FunctionInfo] = []
        for result_row in result_rows:
            ff_info = FunctionStorage._map_row_to_function_info(result_row)
            function_infos.append(ff_info)
        return function_infos

    def find_function(self, file_id: int, function_name: str) -> FunctionInfo:
        cursor = self._connection.cursor()
        sql = f"SELECT * FROM {self._table_name} WHERE file_id = ? AND function_name = ?"
        cursor.execute(sql, (file_id, function_name))
        result_row = cursor.fetchone()
        if result_row:
            ff_info = FunctionStorage._map_row_to_function_info(result_row)
            return ff_info
        return None

    @staticmethod
    def _map_row_to_function_info(result_row):
        ff_info = FunctionInfo()
        ff_info.id = result_row['id']
        ff_info.file_id = result_row['file_id']
        ff_info.first_addr = result_row['first_addr']
        ff_info.function_graph_json = result_row['function_graph_json']
        ff_info.function_name = result_row['function_name']
        ff_info.n_instructions = result_row['n_instructions']
        ff_info.n_instr_data = result_row['n_instr_data']
        ff_info.n_instr_arithm = result_row['n_instr_arithm']
        ff_info.n_instr_logic = result_row['n_instr_logic']
        ff_info.n_instr_string = result_row['n_instr_string']
        ff_info.n_instr_other = result_row['n_instr_other']
        return ff_info
