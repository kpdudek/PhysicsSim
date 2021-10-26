#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

int LIB_VERSION = 1;

struct Point {
    double x;
    double y;
};

int get_library_version(void){
    return LIB_VERSION;
}

double pixels_to_meters(double pixels){
    return 0.01 * pixels;
}

double meters_to_pixels(double meters){
    return meters / 0.01;
}

double euclidian_dist(struct Point p1, struct Point p2){
    double dist = 0.0;
    dist = pow(pow(p1.x-p2.x,2)+pow(p1.y-p2.y,2),0.5);
    return dist;
}

int circle_circle(double pose_1 [2], double radius_1, double pose_2 [2], double radius_2){
    int result = 0;

    struct Point p1;
    struct Point p2;
    p1.x = pose_1[0];
    p1.y = pose_1[1];
    p2.x = pose_2[0];
    p2.y = pose_2[1];

    double dist = euclidian_dist(p1,p2);
    // printf("Distance: %f\n",dist);
    // printf("Radius sum: %f\n",radius_1+radius_2);
    if(radius_1+radius_2 >= dist){
        result = 1;
    }
    // printf("Result: %d\n",result);
    return result;
}

int circle_rect(double pose_1 [2], double radius_1, double pose_2 [2], double width, double height){
    int result = 0;

    struct Point p1;
    struct Point p2;
    p1.x = pose_1[0];
    p1.y = pose_1[1];
    p2.x = pose_2[0];
    p2.y = pose_2[1];

    return result;
}

int circle_mesh(double pose_1 [2], double radius_1, double x_vals [], double y_vals []){
    int result = 0;
    return result;
}

int circle_circle_test(void){
    double pose_1 [2] = {1,1};
    double pose_2 [2] = {5,1};
    double radius_1 = 1.5;
    double radius_2 = 1.5;
    int res = circle_circle(pose_1,radius_1,pose_2,radius_2);
    return res;
}

int circle_rect_test(void){
    int res = 0;
    return res;
}

int circle_mesh_test(void){
    int res = 0;
    return res;
}