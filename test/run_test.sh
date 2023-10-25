#!/usr/bin/env bash
PROGRAM_SHA=`sha256sum ./program  | awk '{print $1}'`
IFUNCS_SHA=`sha256sum ./ifuncs.o  | awk '{print $1}'`
DB_NAME='tamiz.db'
PLOT_FLAG=''  # PLOT_FLAG='--plot'
rm -rf $DB_NAME

source ../venv/bin/activate; python --version
export PYTHONPATH=../

python -m tamiz --add ./program --db $DB_NAME $PLOT_FLAG
python -m tamiz --add ./ifuncs.o --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 2 str immediates"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_str_imm $IFUNCS_SHA func_inl_str_2 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 2 str local vars"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_str_2var $IFUNCS_SHA func_inl_str_2 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 2 int immediates"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_int_imm $IFUNCS_SHA func_inl_int_2 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 2 int local vars"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_int_2var $IFUNCS_SHA func_inl_int_2 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 8 int local vars"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_int_8var $IFUNCS_SHA func_inl_int_8 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 9 int local vars"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_int_9var $IFUNCS_SHA func_inl_int_9 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 2 int by address"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_int_2pointers $IFUNCS_SHA func_inl_int_point_2 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 2 double immediates"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_double_imm $IFUNCS_SHA func_inl_double_2 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 2 double local vars"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_double_2var $IFUNCS_SHA func_inl_double_2 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 8 double local vars"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_double_8var $IFUNCS_SHA func_inl_double_8 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: 9 double local vars"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_double_9var $IFUNCS_SHA func_inl_double_9 --db $DB_NAME $PLOT_FLAG
printf "\n\n## Test case: no parameters"
python -m tamiz --seek $PROGRAM_SHA test_ins_func_void $IFUNCS_SHA func_inl_void --db $DB_NAME $PLOT_FLAG
