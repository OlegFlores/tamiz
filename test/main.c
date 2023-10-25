#include "ifuncs.h"
#include <stdio.h>

int test_ins_func_str_imm() {
    return func_inl_str_2("a", "b");
}

int test_ins_func_str_2var() {
    const char p1[] = {'a'};
    const char p2[] = {'b'};
    return func_inl_str_2(p1, p2);
}

int test_ins_func_int_imm() {
    return func_inl_int_2(1, 2);
}

int test_ins_func_int_2var() {
    int p1 = 1;
    int p2 = 2;
    return func_inl_int_2(p1, p2);
}

int test_ins_func_int_2pointers() {
    uintmax_t p1 = 1;
    uintmax_t p2 = 2;
    return func_inl_int_point_2(&p1, &p2);
}


int test_ins_func_int_8var() {
    int p1 = 1;
    int p2 = 2;
    int p3 = 3;
    int p4 = 4;
    int p5 = 5;
    int p6 = 6;
    int p7 = 7;
    int p8 = 8;
    return func_inl_int_8(p1, p2, p3, p4, p5, p6, p7, p8);
}

int test_ins_func_int_9var() {
    int p1 = 1;
    int p2 = 2;
    int p3 = 3;
    int p4 = 4;
    int p5 = 5;
    int p6 = 6;
    int p7 = 7;
    int p8 = 8;
    int p9 = 9;
    return func_inl_int_9(p1, p2, p3, p4, p5, p6, p7, p8, p9);
}

int test_ins_func_double_imm() {
    return func_inl_double_2(1.1, 2.1);
}

int test_ins_func_double_2var() {
    double p1 = 1.1;
    double p2 = 2.1;
    return func_inl_double_2(p1, p2);
}

int test_ins_func_double_8var() {
    double p1 = 1.1;
    double p2 = 2.1;
    double p3 = 3.1;
    double p4 = 4.1;
    double p5 = 5.1;
    double p6 = 6.1;
    double p7 = 7.1;
    double p8 = 8.1;

    return func_inl_double_8(p1, p2, p3, p4, p5, p6, p7, p8);
}

int test_ins_func_double_9var() {
    double p1 = 1.1;
    double p2 = 2.1;
    double p3 = 3.1;
    double p4 = 4.1;
    double p5 = 5.1;
    double p6 = 6.1;
    double p7 = 7.1;
    double p8 = 8.1;
    double p9 = 9.1;

    return func_inl_double_9(p1, p2, p3, p4, p5, p6, p7, p8, p9);
}

int test_ins_func_void() {
    return func_inl_void();
}

int main(int argc, char *argv[]) {
    int r1 = test_ins_func_str_imm();
    int r2 = test_ins_func_str_2var();
    int r3 = test_ins_func_int_imm();
    int r4 = test_ins_func_int_2var();
    int r5 = test_ins_func_int_8var();
    int r6 = test_ins_func_int_9var();
    int r7 = test_ins_func_double_imm();
    int r8 = test_ins_func_double_2var();
    int r9 = test_ins_func_double_8var();
    int r10 = test_ins_func_double_9var();
    int r11 = test_ins_func_void();
    return r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11;
}
