// #define NOMINMAX
// #include <windows.h>
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

void main(void){
    return;
}

// def min_dist_point_to_line(P,A,B):
//     '''This function computes the shortest distance between a point and a line segment
//         params:
//             P (2x1 numpy.array): Point of interest
//             A (2x1 numpy.array): First vertex of line segment
//             B (2x1 numpy.array): Second vertex of line segment
//     '''
//     # Direction vector
//     M = B - A
//     # Running parameter at the orthogonal intersection
//     t0 = np.dot(M,P-A) / np.dot(M,M)
//     # Intersection point
//     C = A + t0 * M
//     # Compute distance based on where the point lies
//     if t0 <= 0: # left of the segment
//         dist = np.linalg.norm(P-A)
//     elif t0 >= 1: # right of the segment
//         dist = np.linalg.norm(P-B)
//     else: # Over the segment
//         dist = np.linalg.norm(P-C)
//     return dist,C

// def point_is_collision(point,body):
//     if body.config['type'] == 'circle':
//         dist = np.linalg.norm(body.pose-point)
//         if dist <= body.config['radius']:
//             return True
//         else:
//             return False

// def circle_collision_check(pose,radius,body):
//     if body.config['type']=='rect':
//         edges = []
//         edges.append([np.array([body.pose[0],body.pose[1]]),np.array([body.pose[0]+body.config['width'],body.pose[1]])])
//         edges.append([np.array([body.pose[0]+body.config['width'],body.pose[1]]),np.array([body.pose[0]+body.config['width'],body.pose[1]+body.config['height']])])
//         edges.append([np.array([body.pose[0]+body.config['width'],body.pose[1]+body.config['height']]),np.array([body.pose[0],body.pose[1]+body.config['height']])])
//         edges.append([np.array([body.pose[0],body.pose[1]+body.config['height']]),np.array([body.pose[0],body.pose[1]])])
//         for edge in edges:
//             min_dist,C = min_dist_point_to_line(pose,edge[0],edge[1])
//             if  min_dist <= radius:
//                 if edge[0][0] == edge[1][0]:
//                     reflect = np.array([-1,1])
//                 else:
//                     reflect = np.array([1,-1])
//                 return True,reflect
//     return False,np.array([1,1])
