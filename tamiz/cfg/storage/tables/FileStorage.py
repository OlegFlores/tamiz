from sqlite3 import Connection
from tamiz.cfg.storage.FileInfo import FileInfo
import os


class FileStorage:
    __slots__ = (
        "_connection",
        "_table_name"
    )

    def __init__(self, connection: Connection, table_name: str):
        self._connection = connection
        self._table_name = table_name

    def create_table(self):
        cursor = self._connection.cursor()
        fields = [
            "id INTEGER PRIMARY KEY",
            "name VARCHAR(256)",
            "sha256 VARCHAR(64)",
            "executable BOOLEAN",
        ]
        sql = (
            f"CREATE TABLE IF NOT EXISTS  {self._table_name} "
            f"({', '.join(fields)})"
        )
        # print(f'sql {sql}')
        cursor.execute(sql)
        self._connection.commit()


    def find_file(self, sha256: str) -> FileInfo | None:
        cursor = self._connection.cursor()
        sql = f"SELECT * FROM {self._table_name} WHERE sha256 = ?"
        cursor.execute(sql, (sha256,))
        result_row = cursor.fetchone()
        if result_row:
            file_info = FileStorage.map_row_to_file_info(result_row)
            return file_info
        return None

    @staticmethod
    def map_row_to_file_info(result_row):
        file_id = result_row['id']
        file_name = result_row['name']
        file_sha256 = result_row['sha256']
        file_executable = result_row['executable']
        file_info = FileInfo()
        file_info.id = file_id
        file_info.name = file_name
        file_info.sha256 = file_sha256
        file_info.executable = file_executable
        return file_info

    def save_file(self, file_info: FileInfo):
        sql = f"INSERT INTO {self._table_name} (name, sha256, executable) VALUES (?, ?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, (file_info.name, file_info.sha256, file_info.executable))
        self._connection.commit()
