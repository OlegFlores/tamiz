import argparse
import logging
from pathlib import Path
from typing import Tuple

from tamiz.cfg.algorithms.find_isomorphic_subgraphs_candidates import find_isomorphic_subgraphs_candidates
from tamiz.cfg.algorithms.is_found_subgraph_valid import is_found_subgraph_valid
from tamiz.KnowledgeBase import KnowledgeBase
import sys

FILE_NAME = str(Path(__file__).parent.parent / "samples/program_w_inline_strlen/program_w_inline")


logging.getLogger('angr').setLevel('ERROR')


# def main(file_path: str):
#     file_info = FileInfo()
#     file_info.load_from_fs(path=file_path)
#     print(file_info)
#     target_functions = extract_binary_functions(file_path=file_path, framework=BinaryFramework.ANGR)
#     for f in target_functions:
#         print(f.text_summary())
#         for addr, block in f.blocks.items():
#             if len(block.instructions) > 0:
#                 block_instrs = '\n'.join(map(lambda i: i.__repr__(), block.instructions))
#             else:
#                 block_instrs = 'no instructions'
#             print(block_instrs)


def load_library_file(kb: KnowledgeBase) -> Tuple[str, str]:
    lib_file_path = str(Path(__file__).parent.parent / "samples/lib_files/mystrcmp.o")
    file_info = kb.get_file_info(file_path=lib_file_path)
    return file_info.sha256, 'mystrcmp'


def load_exe_file(kb: KnowledgeBase) -> Tuple[str, str]:
    exe_file_path = str(Path(__file__).parent.parent / "samples/my_strcmp/program")
    file_info = kb.get_file_info(file_path=exe_file_path)
    return file_info.sha256, 'main'

def load_file(kb: KnowledgeBase, path: str) -> str:
    file_info = kb.get_file_info(file_path=path)
    return file_info.sha256


def search(kb: KnowledgeBase, exe_sha256: str, exe_func_name, lib_sha256, lib_func_name):
    function_main_in_executable = kb.get_function(file_sha256=exe_sha256, function_name=exe_func_name)
    function_strlen_in_library = kb.get_function(file_sha256=lib_sha256, function_name=lib_func_name)
    print(function_main_in_executable.text_summary())
    print(function_strlen_in_library.text_summary())
    blocks_candidates_graphs = find_isomorphic_subgraphs_candidates(superfunction=function_main_in_executable,
                                         subfunction=function_strlen_in_library)
    for graph_candidate in blocks_candidates_graphs:
        really_subgraph = is_found_subgraph_valid(superfunction=function_main_in_executable,
                                                  subfunction=function_strlen_in_library,
                                                  graph_candidate=graph_candidate)
        print(f'Graph verification result: {really_subgraph}')
    return

def main():
    print('\n\n')
    parser = argparse.ArgumentParser(description='Binary function identification tool.')
    parser.add_argument("-p", "--plot", action="store_true", help="Generate CFGs and basic blocks plots in ./images directory")
    parser.add_argument("-b", "--db", metavar="DB_PATH", help="Path to the database file", default="kbstorage.db")
    parser.add_argument("-a", "--add", metavar="FILE_PATH", help="Add a file to the database")
    parser.add_argument("-s", "--seek", nargs=4,
                        metavar=("TARGET_HASH", "TARGET_FUNCTION", "LIBRARY_HASH", "LIBRARY_FUNCTION"),
                        help="Search for isomorphisms")

    args = parser.parse_args()
    db_path = 'kbstorage.db'
    if args.db:
        db_path = args.db
        print(f'Using db: {db_path}')

    kb = KnowledgeBase(db_file_name=db_path, plot=args.plot).open()

    if args.add:
        print(f'Going to add a file *{args.add}* into the db')
        fi = kb.get_file_info(file_path=args.add)
        print(f'File was successfully loaded into the DB. Hash: `{fi.sha256}`')
        print(f'This is the list of function that was extracted:\n')
        funcs = kb.get_functions(file_info=fi)
        for func in funcs:
            print(f'-  `{func.function_name}@{hex(func.first_address)}` ({func.n_instructions} instrs)')
    elif args.seek:
        print(f'Going to search for isomorphisms')
        target_hash, target_function, library_hash, library_function = args.seek
        search(kb, target_hash, target_function, library_hash, library_function)
    else:
        parser.print_help()

    kb.close()


if __name__ == "__main__":  # pragma: no cover
    main()
