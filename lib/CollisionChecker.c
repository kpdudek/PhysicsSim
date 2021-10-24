#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

double pixels_to_meters(double pixels){
    return 0.01 * pixels;
}

double meters_to_pixels(double meters){
    return meters / 0.01;
}
