#include "ifuncs.h"
#include <stdint.h>

int func_inl_str_2(const char *, const char *);

int func_inl_int_2(uintmax_t, uintmax_t);

int func_inl_int_point_2(uintmax_t*, uintmax_t*);

int func_inl_int_8(
        uintmax_t arg1, 
        uintmax_t arg2,
        uintmax_t arg3,
        uintmax_t arg4,
        uintmax_t arg5, 
        uintmax_t arg6,
        uintmax_t arg7,
        uintmax_t arg8
        );

int func_inl_int_9(
        uintmax_t arg1, 
        uintmax_t arg2,
        uintmax_t arg3,
        uintmax_t arg4,
        uintmax_t arg5, 
        uintmax_t arg6,
        uintmax_t arg7,
        uintmax_t arg8,
        uintmax_t arg9
        );

int func_inl_double_2(double, double);

int func_inl_double_8(
        double arg1, 
        double arg2,
        double arg3,
        double arg4,
        double arg5, 
        double arg6,
        double arg7,
        double arg8
        );


int func_inl_double_9(
        double arg1, 
        double arg2,
        double arg3,
        double arg4,
        double arg5, 
        double arg6,
        double arg7,
        double arg8,
        double arg9
        );

int func_inl_void(void);