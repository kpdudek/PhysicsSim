#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

struct Point {
    double x;
    double y;
};

struct Point return_struct(void){
    struct Point result;
    result.x = 1.0;
    result.y = 1.0;
    return result;
}

int mult(int a, int b){
    return a*b;
}

void array_test(double np_array [], int cols){
    printf("Vertex 1: [%f,%f]",np_array[0],np_array[cols]);
}