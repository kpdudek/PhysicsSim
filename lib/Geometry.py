#!/usr/bin/env python3

import numpy as np
from math import cos, sin, atan2
import time

def pixels_to_meters(pixels):
    return 0.01 * float(pixels)

def meters_to_pixels(meters):
    return float(meters) / 0.01

def min_dist_point_to_line(P,A,B):
    '''This function computes the shortest distance between a point and a line segment
        params:
            P (2x1 numpy.array): Point of interest
            A (2x1 numpy.array): First vertex of line segment
            B (2x1 numpy.array): Second vertex of line segment
    '''
    # Direction vector
    M = B - A
    # Running parameter at the orthogonal intersection
    t0 = np.dot(M,P-A) / np.dot(M,M)
    # Intersection point
    C = A + t0 * M
    # Compute distance based on where the point lies
    if t0 <= 0: # left of the segment
        dist = np.linalg.norm(P-A)
    elif t0 >= 1: # right of the segment
        dist = np.linalg.norm(P-B)
    else: # Over the segment
        dist = np.linalg.norm(P-C)
    return dist,C

def point_is_collision(point,body):
    if body.config['type'] == 'circle':
        dist = np.linalg.norm(body.pose-point)
        if dist <= body.config['radius']:
            return True
        else:
            return False

def circle_collision_check(pose,radius,body):
    if body.config['type']=='rect':
        edges = []
        edges.append([np.array([body.pose[0],body.pose[1]]),np.array([body.pose[0]+body.config['width'],body.pose[1]])])
        edges.append([np.array([body.pose[0]+body.config['width'],body.pose[1]]),np.array([body.pose[0]+body.config['width'],body.pose[1]+body.config['height']])])
        edges.append([np.array([body.pose[0]+body.config['width'],body.pose[1]+body.config['height']]),np.array([body.pose[0],body.pose[1]+body.config['height']])])
        edges.append([np.array([body.pose[0],body.pose[1]+body.config['height']]),np.array([body.pose[0],body.pose[1]])])
        for edge in edges:
            min_dist,C = min_dist_point_to_line(pose,edge[0],edge[1])
            if  min_dist <= radius:
                if edge[0][0] == edge[1][0]:
                    reflect = np.array([-1,1])
                else:
                    reflect = np.array([1,-1])
                return True,reflect

    return False,np.array([1,1])

def rotate_2d(vertices,angle):
    rot_mat = np.array([[cos(angle),-sin(angle)],[sin(angle),cos(angle)]])
    r,c = vertices.shape
    for idx in range(0,c):
        res = np.matmul(rot_mat,vertices[:,idx].reshape(2,1))
        vertices[0,idx] = res[0]
        vertices[1,idx] = res[1]
    return vertices

def edge_angle(V0,V1,V2):
    '''
    The edge angle is found using unit vectors. This function is passed a set of three vertices where V0 is the shared point of the two vectors.
    Args:
        V0 (1x2 numpy array): Shared point of the two vectors
        V1 (1x2 numpy array): Vector 1 endpoint
        V2 (1x2 numpy array): Vector 2 endpoint
    '''
    # This function finds the signed shortest distance between two vectors
    V1[0] = V1[0] - V0[0]
    V1[1] = V1[1] - V0[1]
    V2[0] = V2[0] - V0[0]
    V2[1] = V2[1] - V0[1]

    # Dot product of the vectors
    cosine_theta = V1[0]*V2[0] + V1[1]*V2[1]
    # Cross product of the vectors
    sin_theta = V1[0]*V2[1] - V1[1]*V2[0]
    # find the angle using the relationships sin(theta)== tan(theta) = sin(theta)/cos(theta)
    edge_angle = atan2(sin_theta,cosine_theta)
    return edge_angle

class Circle():
    def __init__(self,pose,radius):
        self.pose = pose
        self.radius = radius

class Rectangle():
    def __init__(self,pose,width,height):
        self.pose = pose
        self.width = width
        self.height = height

class Mesh():
    def __init__(self,vertices):
        self.vertices = vertices

    def compute_center_of_mass(self):
        pass