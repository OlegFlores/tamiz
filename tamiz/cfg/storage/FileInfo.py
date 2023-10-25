from hashlib import file_digest
import os
from typing import Tuple
import elftools.elf.elffile as elffile


def _calc_sha256(path: str):
    with open(path, 'rb', buffering=0) as f:
        return file_digest(f, 'sha256').hexdigest()


def _is_executable(path):
    it_is_library = False
    it_is_executable = True
    # Open the ELF file using elftools
    with open(path, 'rb') as file:
        elf = elffile.ELFFile(file)
        # Check if the file type is executable
        if elf.header.e_type == 'ET_EXEC':
            return it_is_executable
        # Check if the file type is dynamic library
        elif elf.header.e_type == 'ET_DYN':
            if elf.header.e_entry == 0:
                return it_is_library
            else:
                return it_is_executable
        elif elf.header.e_type == 'ET_REL':
            return it_is_library
        else:
            # File is not an ELF executable or library
            raise Exception(f'The file is not an ELF executable or library. Actual type: {elf.header.e_type}')


class FileInfo:
    __slots__ = (
        "id",
        "name",
        "sha256",
        "executable",
        "functions",
        "_file_header"
    )

    def __init__(self, ):
        self.id = None
        self.executable = None
        self.name = None
        self.sha256 = None
        self.functions = None

    def load_from_fs(self, path: str) -> 'FileInfo':
        file_name = os.path.basename(path)
        self.name = file_name
        self.sha256 = _calc_sha256(path)
        self.executable = _is_executable(path)
        return self

    @property
    def file_header(self) -> Tuple[int, str, str, bool]:
        """
        Returns main file properties.

        Returns:
            *Tuple[int, str, str, bool]* A tuple containing the file_id in the DB (int), file name \
             (as a string), SHA-256 hash (string) and executable flag.
        """
        return self.id, self.name, self.sha256, self.executable

    def __repr__(self):
        return f"{self.name}, executable: {self.executable}. SHA256: {self.sha256}"
