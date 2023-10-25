#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

#pragma once

inline __attribute__((always_inline)) int func_inl_str_2(const char *arg1, const char *arg2) {
    int r = 1;
    if(arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(arg2) {
        printf("arg2\n");
        r += 1;
    }
    return r;
};


inline __attribute__((always_inline)) int func_inl_int_2(uintmax_t arg1, uintmax_t arg2) {
    int r = 1;
    if(arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(arg2) {
        printf("arg2\n");
        r += 1;
    }
    return r;
};

inline __attribute__((always_inline)) int func_inl_int_point_2(uintmax_t* arg1, uintmax_t* arg2) {
    int r = 1;
    if(*arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(*arg2) {
        printf("arg2\n");
        r += 1;
    }
    return r;
};


inline __attribute__((always_inline)) int func_inl_int_8(
        uintmax_t arg1, 
        uintmax_t arg2,
        uintmax_t arg3,
        uintmax_t arg4,
        uintmax_t arg5, 
        uintmax_t arg6,
        uintmax_t arg7,
        uintmax_t arg8
        ) {
    int r = 1;
    if(arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(arg2) {
        printf("arg2\n");
        r += 1;
    }
    if(arg3) {
        printf("arg3\n");
        r += 1;
    }
    if(arg4) {
        printf("arg4\n");
        r += 1;
    }
    if(arg5) {
        printf("arg5\n");
        r += 1;
    }
    if(arg6) {
        printf("arg6\n");
        r += 1;
    }
    if(arg7) {
        printf("arg7\n");
        r += 1;
    }
    if(arg8) {
        printf("arg8\n");
        r += 1;
    }
    return r;
};

inline __attribute__((always_inline)) int func_inl_int_9(
        uintmax_t arg1, 
        uintmax_t arg2,
        uintmax_t arg3,
        uintmax_t arg4,
        uintmax_t arg5, 
        uintmax_t arg6,
        uintmax_t arg7,
        uintmax_t arg8,
        uintmax_t arg9
        ) {
    int r = 1;
    if(arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(arg2) {
        printf("arg2\n");
        r += 1;
    }
    if(arg3) {
        printf("arg3\n");
        r += 1;
    }
    if(arg4) {
        printf("arg4\n");
        r += 1;
    }
    if(arg5) {
        printf("arg5\n");
        r += 1;
    }
    if(arg6) {
        printf("arg6\n");
        r += 1;
    }
    if(arg7) {
        printf("arg7\n");
        r += 1;
    }
    if(arg8) {
        printf("arg8\n");
        r += 1;
    }
    if(arg9) {
        printf("arg9\n");
        r += 1;
    }
    return r;
};

inline __attribute__((always_inline)) int func_inl_double_2(double arg1, double arg2) {
    int r = 1;
    if(arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(arg2) {
        printf("arg2\n");
        r += 1;
    }
    return r;
};

inline __attribute__((always_inline)) int func_inl_double_8(
        double arg1, 
        double arg2,
        double arg3,
        double arg4,
        double arg5, 
        double arg6,
        double arg7,
        double arg8
        ) {
    int r = 1;
    if(arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(arg2) {
        printf("arg2\n");
        r += 1;
    }
    if(arg3) {
        printf("arg3\n");
        r += 1;
    }
    if(arg4) {
        printf("arg4\n");
        r += 1;
    }
    if(arg5) {
        printf("arg5\n");
        r += 1;
    }
    if(arg6) {
        printf("arg6\n");
        r += 1;
    }
    if(arg7) {
        printf("arg7\n");
        r += 1;
    }
    if(arg8) {
        printf("arg8\n");
        r += 1;
    }
    return r;
};

inline __attribute__((always_inline)) int func_inl_double_9(
        double arg1, 
        double arg2,
        double arg3,
        double arg4,
        double arg5, 
        double arg6,
        double arg7,
        double arg8,
        double arg9
        ) {
    int r = 1;
    if(arg1) {
        printf("arg1\n");
        r += 1;
    }
    if(arg2) {
        printf("arg2\n");
        r += 1;
    }
    if(arg3) {
        printf("arg3\n");
        r += 1;
    }
    if(arg4) {
        printf("arg4\n");
        r += 1;
    }
    if(arg5) {
        printf("arg5\n");
        r += 1;
    }
    if(arg6) {
        printf("arg6\n");
        r += 1;
    }
    if(arg7) {
        printf("arg7\n");
        r += 1;
    }
    if(arg8) {
        printf("arg8\n");
        r += 1;
    }
    if(arg9) {
        printf("arg9\n");
        r += 1;
    }
    return r;
};

inline __attribute__((always_inline)) int func_inl_void(void) {
    uint8_t min = 1;
    uint8_t max = 101;
    srand(time(NULL));
    // Generate a random number in the range [min, max)
    return min + rand() % (max - min);
};
