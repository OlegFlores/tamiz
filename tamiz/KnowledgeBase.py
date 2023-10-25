import sqlite3
from sqlite3 import Connection
from typing import List

from tamiz.cfg.storage.tables.FileStorage import FileStorage
from tamiz.cfg.storage.tables.FunctionStorage import FunctionStorage
from tamiz.cfg.storage.tables.BasicBlockStorage import BasicBlockStorage
from tamiz.cfg.storage.FileInfo import FileInfo
from tamiz.cfg.extract_binary_functions import extract_binary_functions
from tamiz.cfg.BinaryFramework import BinaryFramework
from tamiz.cfg.BinaryFunction import BinaryFunction
from tamiz.draw import draw_graph


class KnowledgeBase:
    __slots__ = (
        "_connection",
        "_db_file_name",
        "_file_storage",
        "_function_storage",
        "_basic_block_storage",
        "_plot",
    )

    def __init__(self, db_file_name: str, plot: bool = False):
        self._file_storage: FileStorage = None
        self._function_storage: FunctionStorage = None
        self._basic_block_storage: BasicBlockStorage = None
        self._connection: Connection = None
        self._db_file_name = db_file_name
        self._plot = plot

    def open(self) -> 'KnowledgeBase':
        self._connection = sqlite3.connect(self._db_file_name)
        self._connection.row_factory = sqlite3.Row
        self._file_storage = FileStorage(connection=self._connection, table_name='elf_files')
        self._function_storage = FunctionStorage(connection=self._connection,
                                                 table_name='functions',
                                                 files_table_name='elf_files')
        self._basic_block_storage = BasicBlockStorage(connection=self._connection,
                                                      table_name='basic_blocks',
                                                      functions_table_name='functions')
        self._file_storage.create_table()
        self._function_storage.create_table()
        self._basic_block_storage.create_table()
        return self

    def get_file_info(self, file_path) -> FileInfo:
        file_info = FileInfo()
        file_info.load_from_fs(path=file_path)
        db_file_info = self._file_storage.find_file(sha256=file_info.sha256)
        file_found = db_file_info is not None
        if file_found:
            print(
                f'File with sha256={file_info.sha256} was found in the DB. It is known by the name `{file_info.name}`. '
                f'Reusing it')
            return db_file_info
        else:
            # parse functions
            binary_functions = extract_binary_functions(file_path=file_path, framework=BinaryFramework.ANGR,
                                                        plot_cfg=self._plot)
            print('Saving FileInfo to sqlite...')
            self._file_storage.save_file(file_info=file_info)
            db_file_info = self._file_storage.find_file(sha256=file_info.sha256)
            file_id, _, _, _ = db_file_info.file_header
            for bf in binary_functions:
                stored_func = self._function_storage.save_function(file_id=file_id, function_info=bf.function_info)
                for b_addr, b_block in bf.blocks.items():
                    b_block_info = b_block.basic_block_info()
                    if self._plot:
                        self.plot_basic_block(b_block, b_block_info, bf, db_file_info)
                    self._basic_block_storage.save_basic_block(file_id=file_id, function_id=stored_func.id,
                                                               basic_block_info=b_block_info)
        return db_file_info

    def plot_basic_block(self, b_block, b_block_info, bf, db_file_info):
        try:
            draw_graph(b_block.local_edg,
                       str(f'./images/{db_file_info.name}/{bf.function_info.function_name}_{hex(b_block_info.address)}.png'))
        except:
            print(f'Could not plot BB {hex(b_block_info.address)} for function {bf.function_info.function_name}')

    def close(self):
        self._connection.close()

    def get_functions(self, file_info: FileInfo) -> List[BinaryFunction]:
        db_functions = self._function_storage.find_functions(file_id=file_info.file_header[0])
        db_func_bblocks = self._basic_block_storage.find_basic_blocks(file_id=file_info.file_header[0])
        binary_functions = [BinaryFunction.get_new_from_serialized(fi, db_func_bblocks.get(fi.id, []))
                            for fi in db_functions]
        return binary_functions

    def get_function(self, file_sha256: str, function_name: str) -> BinaryFunction:
        file = self._file_storage.find_file(sha256=file_sha256)
        if not file:
            raise ValueError(f'File {file_sha256} does not exist in the db')
        function_info = self._function_storage.find_function(file_id=file.id, function_name=function_name)
        if not function_info:
            raise ValueError(f'Function {function_name} does not exist in the db')
        db_func_blocks_dict = self._basic_block_storage.find_basic_blocks(file_id=file.id, function_id=function_info.id)
        blocks = db_func_blocks_dict[function_info.id]
        binary_function = BinaryFunction.get_new_from_serialized(function_info=function_info, blocks=blocks)
        return binary_function
