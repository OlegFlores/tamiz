from typing import List
from angrutils import plot_func_graph
from .BinaryFramework import BinaryFramework
from .angr_extract_binary_functions import angr_extract_binary_functions
from .BinaryFunction import BinaryFunction
import os

def _get_dir_for_f_cfgs(file_path: str) -> str:
    dir_name = file_path.split('/')[-1]
    try:
        os.mkdir(f"./images/{dir_name}")
    except OSError as error:
        print(error)
    return dir_name


def extract_binary_functions(file_path: str, framework: BinaryFramework = BinaryFramework.ANGR, plot_cfg: bool = False) -> List[BinaryFunction]:
    if framework != BinaryFramework.ANGR:
        raise NotImplemented("Framework %s is not supported" % framework)
    dir_name = _get_dir_for_f_cfgs(file_path)

    t_functions, cfg, func_cfgs = angr_extract_binary_functions(file_path=file_path)
    if plot_cfg:
        for i in range(len(t_functions)):
            # if t_functions[i].first_address == 4202224:
            try:
                plot_func_graph(cfg.project, func_cfgs[i], f'./images/{dir_name}/{t_functions[i].function_name}_CFG',
                                format="png", asminst=True, ailinst=True, vexinst=False, structure=None,
                                color_depth=True)
            except:
                print(f'Could not plot CFG for function {t_functions[i].function_name}')
    return t_functions
