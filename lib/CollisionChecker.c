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

double norm(struct Point p){
    double result = 0.0;
    result = pow(pow(p.x,2)+pow(p.y,2),0.5);
    return result;
}

struct Point subtract(struct Point A, struct Point B){
    struct Point result;
    result.x = A.x - B.x;
    result.y = A.y - B.y;
    return result;
}

struct Point add(struct Point A, struct Point B){
    struct Point result;
    result.x = A.x + B.x;
    result.y = A.y + B.y;
    return result;
}

struct Point multiply(struct Point A, double n){
    struct Point result;
    result.x = A.x * n;
    result.y = A.y * n;
    return result;
}

double dot_product(struct Point B, struct Point A){
    double result = 0.0;
    result = (B.x*A.x) + (B.y*A.y);
    return result;
}

double edge_angle(struct Point V0, struct Point V1, struct Point V2){
    /*
    The edge angle is found using unit vectors. This function is passed a set of three vertices where V0
    is the shared point of the two vectors.
    Args:
        V0 (1x2 numpy array): Shared point of the two vectors
        V1 (1x2 numpy array): Vector 1 endpoint
        V2 (1x2 numpy array): Vector 2 endpoint
    */
    // This function finds the signed shortest distance between two vectors
    V1.x = V1.x - V0.x;
    V1.y = V1.y - V0.y;
    V2.x = V2.x - V0.x;
    V2.y = V2.y - V0.y;

    // Dot product of the vectors
    double cosine_theta = V1.x*V2.x + V1.y*V2.y;
    // Cross product of the vectors
    double sin_theta = V1.x*V2.y - V1.y*V2.x;
    // find the angle using the relationships sin(theta)== tan(theta) = sin(theta)/cos(theta)
    double edge_angle = atan2(sin_theta,cosine_theta);
    return edge_angle;
}

double min_dist_point_to_line(struct Point P, struct Point A, struct Point B){
    /* This function computes the shortest distance between a point and a line segment
        params:
            P (struct Point): Point of interest
            A (struct Point): First vertex of line segment
            B (struct Point): Second vertex of line segment
    */
    double dist = 0.0;
    // # Direction vector
    // M = B - A
    struct Point M = subtract(B,A);
    // # Running parameter at the orthogonal intersection
    // t0 = np.dot(M,P-A) / np.dot(M,M)
    double t0 = dot_product(M,subtract(P,A)) / dot_product(M,M);
    // # Intersection point
    // C = A + t0 * M
    struct Point C = add(A,multiply(M,t0));
    // Compute distance based on where the point lies
    // left of the segment
    if(t0 <= 0){
        dist = norm(subtract(P,A));
    }
    // right of the segment
    else if(t0 >= 1){
        dist = norm(subtract(P,B));
    }
    // Over the segment
    else{
        dist = norm(subtract(P,C));
    }
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
    if(radius_1+radius_2 >= dist){
        result = 1;
    }
    return result;
}

double circle_rect(double pose_1 [2], double radius_1, double pose_2 [2], double width, double height){
    double result = -999.0;

    struct Point p; p.x = pose_1[0]; p.y = pose_1[1];
    struct Point c1; c1.x = pose_2[0]; c1.y = pose_2[1];
    struct Point c2; c2.x = pose_2[0]+width; c2.y = pose_2[1];
    struct Point c3; c3.x = pose_2[0]+width; c3.y = pose_2[1]+height;
    struct Point c4; c4.x = pose_2[0]; c4.y = pose_2[1]+height;

    // Check each edges min dist from the circle origin and if its less than the radious the ball is in collision
    if(min_dist_point_to_line(p,c1,c2) <= radius_1){
        struct Point V0;
        V0.x = c1.x+50.0;
        V0.y = c1.y;
        return result = edge_angle(c1,V0,c2);
    }
    else if(min_dist_point_to_line(p,c2,c3) <= radius_1){
        struct Point V0;
        V0.x = c2.x+50.0;
        V0.y = c2.y;
        return result = edge_angle(c2,V0,c3);
    }
    else if(min_dist_point_to_line(p,c3,c4) <= radius_1){
        struct Point V0;
        V0.x = c3.x+50.0;
        V0.y = c3.y;
        return result = edge_angle(c3,V0,c4);
    }
    else if(min_dist_point_to_line(p,c4,c1) <= radius_1){
        struct Point V0;
        V0.x = c4.x+50.0;
        V0.y = c4.y;
        return result = edge_angle(c4,V0,c1);
    }
    return result;
}

int circle_mesh(double pose_1 [2], double radius_1, double x_vals [], double y_vals []){
    int result = 0;
    return result;
}

int point_in_rect(double point [2], double pose_1 [2], double w1, double h1){
    int result = 0;
    struct Point r1; r1.x = pose_1[0]; r1.y = pose_1[1];
    struct Point r2; r2.x = pose_1[0]+w1; r2.y = pose_1[1];
    struct Point r3; r3.x = pose_1[0]+w1; r3.y = pose_1[1]+h1;
    struct Point r4; r4.x = pose_1[0]; r4.y = pose_1[1]+h1;

    if(point[0] >= r1.x && point[0] <= r2.x && point[1] >= r1.y && point[1] <= r3.y){
        result = 1;
    }
    
    return result;
}

double rect_rect(double pose_1 [2], double w1, double h1, double pose_2 [2], double w2, double h2){
    double result = -999.0;
    struct Point r1; r1.x = pose_1[0]; r1.y = pose_1[1];
    struct Point r2; r2.x = pose_1[0]+w1; r2.y = pose_1[1];
    struct Point r3; r3.x = pose_1[0]+w1; r3.y = pose_1[1]+h1;
    struct Point r4; r4.x = pose_1[0]; r4.y = pose_1[1]+h1;

    struct Point r5; r5.x = pose_2[0]; r5.y = pose_2[1];
    struct Point r6; r6.x = pose_2[0]+w2; r6.y = pose_2[1];
    struct Point r7; r7.x = pose_2[0]+w2; r7.y = pose_2[1]+h2;
    struct Point r8; r8.x = pose_2[0]; r8.y = pose_2[1]+h2;

    if(r1.x >= r5.x && r1.x <= r6.x && r1.y >= r5.y && r1.y <= r7.y){
        result = 1.0;
    }
    else if(r2.x >= r5.x && r2.x <= r6.x && r2.y >= r5.y && r2.y <= r7.y){
        result = 1.0;
    }
    else if(r3.x >= r5.x && r3.x <= r6.x && r3.y >= r5.y && r3.y <= r7.y){
        result = 1.0;
    }
    else if(r4.x >= r5.x && r4.x <= r6.x && r4.y >= r5.y && r4.y <= r7.y){
        result = 1.0;
    }

    return result;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////
//  Tests
//////////////////////////////////////////////////////////////////////////////////////////////////////
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

double min_dist_point_to_line_test(double px, double py, double c1x, double c1y, double c2x, double c2y){
    struct Point p;
    p.x = px;
    p.y = py;
    struct Point c1;
    c1.x = c1x;
    c1.y = c1y;
    struct Point c2;
    c2.x = c2x;
    c2.y = c2y;

    double dist = min_dist_point_to_line(p,c1,c2);
    return dist;
}