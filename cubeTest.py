import numpy as np
from Polygon import Polygon
from math import *
import pygame


WIDTH, HEIGHT = 900, 600 #window width is 900 - let's make that 1/4 of the total fov, so it starts moving back at 
#-450 and 1350
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def project(face): #used for making the polygon for each face
    return face[0:4, 0:2]

def draw(polygon):
    points = polygon.getTranslated() #just get the points + position matrix - scale and rotation is all axial
    points = np.array(points)*100
    for i in range(len(points)-1):
        pygame.draw.line(WIN, "black", points[i][0:2], points[i+1][0:2], 3)
    pygame.draw.line(WIN, "black", points[-1][0:2], points[0][0:2], 3)

def rotateMatrix3d(x, y, z, point): #rotate a matrix x radians around x, y radians around y, z radians around z
    point = np.array(point)
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
    return point.__matmul__(xRotation.__matmul__(yRotation.__matmul__(zRotation))) 

def main():
    poly1 = Polygon([[1,-1,-1,1], [1,1,-1,1], [-1,1,-1,1], [-1,-1,-1,1]], id=1)
    poly2 = Polygon([[1,-1,1,1], [1,1,1,1], [-1,1,1,1], [-1,-1,1,1]], id=2)
    poly3 = Polygon([[1,-1,-1,1], [1,1,-1,1], [1,1,1,1], [1,-1,1,1]], id=3)
    poly4 = Polygon([[1,1,-1,1], [-1,1,-1,1], [-1,1,1,1], [1,1,1,1]], id=4)
    poly5 = Polygon([[-1,1,-1,1], [-1,-1,-1,1], [-1,-1,1,1], [-1,1,1,1]], id=5)
    poly6 = Polygon([[-1,-1,-1,1], [1,-1,-1,1], [1,-1,1,1], [-1,-1,1,1]], id=6)
    polys = [poly1,poly2,poly3,poly4,poly5,poly6]
    for poly in polys:
        poly.translate(3,3,3) #moves them all to the positive plane
        poly.rotate(-1,1,1)
        poly.rotateMatrix3d()
    colors = ["blue", "red", "green", "orange", "purple", "yellow"]
    clock = pygame.time.Clock()
    run = True
    scalar = 1
    while run:
        x = y = z = move = 0
        scale = 1
        clock.tick(60)
        WIN.fill("white")
        zLevels = []
        for h in range(len(polys)):
            zLevels.append([polys[h].getTotalZ(),h]) #want to get total z level
        zLevels.sort()
        for zLevel in zLevels:
            order = zLevel[1]
            color = colors[order]
            poly = polys[order]
            pygame.draw.polygon(WIN, color, poly.project())
            draw(poly)#drawing too small
        pygame.display.update()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if keys[pygame.K_LEFT]:
            y = pi/50
        elif keys[pygame.K_RIGHT]:
            y = -pi/50
        if keys[pygame.K_UP]:
            x = -pi/50
        elif keys[pygame.K_DOWN]:
            x = pi/50
        if keys[pygame.K_w]:
            z = -pi/50
        elif keys[pygame.K_s]:
            z = pi/50
        
        if keys[pygame.K_c]:#c should move the object to the left because it's like looking to the right
            move = -.08
            y += pi/600
            for poly in polys:
                allOff = True
                for point in poly.getTranslated():
                    if point[0] > 0:
                        allOff = False #every point on the polygon is offscreen
                if poly.getPosition()[0] < 5:#on the left half of the screen
                    poly.scaleMatrix3d(1-sin((5-poly.getPosition()[0])*pi/10)/100)#make larger as it goes left
                else:
                    poly.scaleMatrix3d(1+sin((poly.getPosition()[0]-5)*pi/10)/100)
            if allOff:
                y -= pi/600*1.42
                    #rotate this point this amount to offset, this is wrong a bit
                        
        elif keys[pygame.K_z]:
            move = .08
            y -= pi/600 #perspective
            for poly in polys:
                allOff = True
                for point in poly.getTranslated():
                    if point[0] < 10:
                        allOff = False #every point on the polygon is offscreen
                if poly.getPosition()[0] < 5:#on the left half of the screen
                    poly.scaleMatrix3d(1+(sin((5-poly.getPosition()[0])*pi/10))**2/100)#make larger as it goes right
                else:
                    poly.scaleMatrix3d(1-sin(((poly.getPosition()[0]-5)*pi/10))**2/100)
            if allOff:
                y += pi/600*1.42

        if keys[pygame.K_1] and scalar > 0.01:
            scale = 1-pi/80
            scalar -= pi/70
        elif keys[pygame.K_2]:
            scale = 1 + pi/80
            scalar += pi/70
        #scale it a bit based on position on-screen - take distance from 5 as the basis
        for poly in polys:
            if poly.checkOffScreen() == 'left':
                poly.translate(40)
            elif poly.checkOffScreen() == 'right':
                poly.translate(-40)
            poly.rotation = [x,y,z]
            poly.translate(move, 0, 0)
            poly.rotateMatrix3d()
            poly.scaleMatrix3d(scale)

if __name__ == "__main__":
    main()