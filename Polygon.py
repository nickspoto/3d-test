import numpy as np
from math import *
import copy
class Polygon:
    def __init__(self, points, rotation=[0,0,0], position=[0,0,0,0], id=0):
        self.points = list(points)
        self.rotation = list(rotation) #default is no rotation
        self.position = list(position) #default is starting at the origin
        self.id = id
        self.onScreen = True

    def getId(self):
        return self.id
    
    def getPoints(self):
        return copy.deepcopy(self.points) #never physically change the points - this fucks things up
    
    def getPosition(self):
        return copy.deepcopy(self.position) #use this to have a normalized polygon and then translate it by this position vector
    
    def getTranslated(self):
        newPoints = self.getPoints()
        pos = self.getPosition()
        for i in range(len(newPoints)):
            pointList = np.array(newPoints[i])
            pointList += pos 
            newPoints[i] = pointList
        return newPoints
    
    def checkOffScreen(self): #checks if the entire polygon is off screen
        for point in self.getPoints():
            pointX = point[0] + self.getPosition()[0]
            if pointX < -30:
                return 'left'
            if pointX > 40:
                return 'right'
    
    def scaleMatrix3d(self, scalar):
        points = np.array(self.getPoints())
        for i in range(len(points)):
            pointArray = np.array(self.points[i])
            pointArray = pointArray / scalar
            self.points[i] = pointArray

    
    def rotateMatrix3d(self): #rotate a matrix x radians around x, y radians around y, z radians around z
        points = np.array(self.getPoints())
        x, y, z = self.rotation
        for i in range(len(points)):
            xRotation = np.array([[1,0,0,0],
                                [0,cos(x),-sin(x),0],
                                [0,sin(x),cos(x),0],
                                [0,0,0,1]])
            yRotation = np.array([[cos(y), 0, sin(y),0], 
                                [0, 1, 0,0], 
                                [-sin(y), 0, cos(y),0],
                                [0,0,0,1]])
            zRotation = np.array([[cos(z), -sin(z), 0,0], 
                                [sin(z), cos(z), 0,0], 
                                [0,0,1,0],
                                [0,0,0,1]])
            self.points[i] = points[i].__matmul__(xRotation.__matmul__(yRotation.__matmul__(zRotation))) 
    
    def getTotalZ(self):
        totalZ = 0
        for point in self.getPoints():
            z = point[2] + self.position[2]
            totalZ += z
        return totalZ

    def rotate(self, x=0, y=0, z=0):
        self.rotation[0] += x
        self.rotation[1] += y
        self.rotation[2] += z

    def translate(self, x=0, y=0, z=0):
        self.position[0] += x
        self.position[1] += y
        self.position[2] += z

    '''
    returns its points as x, y list pairs
    '''
    def project(self):
        points = list(np.array(self.getPoints()) + self.getPosition())
        for x in range(len(points)):
            points[x] = np.array(points[x][0:2])*100
        return points
    
