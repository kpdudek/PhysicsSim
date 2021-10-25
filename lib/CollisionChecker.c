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

double circle_circle(double pose_1 [2], double radius_1, double pose_2 [2], double radius_2){
    int result = 0;

    struct Point p1;
    struct Point p2;
    p1.x = pose_1[0];
    p1.y = pose_1[1];
    p2.x = pose_2[0];
    p2.y = pose_2[1];

    double dist = euclidian_dist(p1,p2);
    printf("Distance: %f\n",dist);
    printf("Radius sum: %f\n",radius_1+radius_2);
    if(radius_1+radius_2 >= dist){
        result = 1.0;
    }
    
    return result;
}

double circle_mesh(void){
    int result = 0;
    return result;
}

double sphere_collision_check_test(void){
    // struct Point t1;
    // struct Point t2;
    // t1.x = 2.0;
    // t1.y = 2.0;

    // t2.x = 3.0;
    // t2.y = 2.0;

    // double dist = 0.0;
    // dist = euclidian_dist(t1,t2);
    // printf("Dist: %f\n",dist);
    // return dist;

    double pose_1 [2] = {1,1};
    double pose_2 [2] = {5,1};
    double radius_1 = 1.5;
    double radius_2 = 1.5;
    double res = circle_circle(pose_1,radius_1,pose_2,radius_2);
    return res;
}