#include <stdlib.h>
#include <stdio.h>

// Written by Armin Rigo. Thank you Armin!

// Together with parse.py, converts a .tm2 file to a .c file (which will simulate much faster). Can be run with the command "python parse.py squaresaresmall.tm2 > tm.i && gcc -O2 tm.c"

#define LARGE_AMOUNT   (6L*1024*1024*1024)   // 6 GB


static long turning_machine(_Bool *p)
{
    long s = 0;

#include "tm.i"

 HALT:
    return s;

 ERROR:
    return -s;
}


int main(void)
{
    char *p = malloc(LARGE_AMOUNT);
    if (p == NULL) {
        fprintf(stderr, "cannot allocate memory\n");
        return 1;
    }

    long result = turning_machine((_Bool *)p);
    if (result < 0) {
        printf("Turing machine reached an error");
        result = -result;
    }
    else
        printf("Turing machine halted");
    printf(" after %ld steps\n", result);
    return 0;
}
