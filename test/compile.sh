#!/usr/bin/env bash
set -e

WARN_FLAGS="-Wall"
FLTO_FLAGS=""
INLINE_FLAGS="" # FLTO_FLAGS="-flto"
CC_FLAGS="-g -O1"

# Step 1. Compile mystrcmp object file mystrcmp.o
echo '== Compiling the object file =='
rm -rf ./ifuncs.o
gcc $WARN_FLAGS $FLTO_FLAGS $CC_FLAGS -no-pie -c ifuncs.c
# nm ./ifuncs.o
# objdump -g ./ifuncs.o


# Step 3. Compile the program linking the library file to it
echo '== Compiling the program and linking the library =='
rm -f ./program
rm -f ./main.o

gcc $FLTO_FLAGS $INLINE_FLAGS $CC_FLAGS -no-pie -c main.c

gcc $INLINE_FLAGS $FLTO_FLAGS $CC_FLAGS -no-pie -o program ifuncs.o main.o

rm main.o
# rm ifuncs

# echo '================================================================================================================='
# echo 'This is the code of the program around test1 function\n'
# # objdump -d -M intel -j .text program | grep -A24 '<test1>:'
# gdb -batch -ex 'file ./program' -ex 'disassemble test1'

# echo '================================================================================================================='
# echo 'This is the code of the program around test2 function\n'
# gdb -batch -ex 'file ./program' -ex 'disassemble test2'

# echo '================================================================================================================='
# echo 'This is the code of the program around func1 function (that has inline attribute)\n'
# gdb -batch -ex 'file ./program' -ex 'disassemble func1'





