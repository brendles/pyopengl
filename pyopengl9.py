import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random #necessary for random cube

#building vertices or nodes to create a cube
#need to define vertices and lines between
#also need to define faces as the area in between nodes/verts and lines

#define 8 vertices
vertices = (
    (1, -1, -1),  #location of nodes/vert is in units
    (1, 1, -1),   #tuples or list works here
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
    )

#define lines or edges, they are connectors to vertices
#each vert has 3 connections (12 total for this)
edges = (
    (0,1),  #tuple or dict works here. No idea why.
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7),
    )

surfaces = ( #this is each face of the cube, defined in each tuple. EG - 0,1,2,3 is one face
    (0,1,2,3), #each individual digit corresponds to vertex
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

colors = (  #using list here possibly modifies color unexpectedly
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1)
    )

##ground_vertices = (
##    (-10, -1.1, 20),
##    (10, -1.1, 20),
##    (-10, -1.1, -300),
##    (-10, -1.1, -300),
##    )
##
##def ground():
##    glBegin(GL_QUADS)
##    for vertex in ground_vertices:
##        glColor3fv((0,0.5,0.5))
##        glVertex3fv(vertex)
##
##    glEnd()


def set_vertices(max_distance, min_distance = -20, camera_x = 0, camera_y = 0): #modifies vertices for "infinite travel game", min distance is basically the end point of the camera

    camera_x = -1*int(camera_x)
    camera_y = -1*int(camera_y)


    x_value_change = random.randrange(camera_x-75,camera_x+75)
    y_value_change = random.randrange(camera_y-75,camera_y+75)
    z_value_change = random.randrange(-1*max_distance,min_distance)

    new_vertices = []

    for vert in vertices: #modifies individual vertex
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x) #applies changes
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert) #applies change for entire vertex

    return new_vertices #save changes to tuple



def Cube(vertices):
    glBegin(GL_QUADS) #again, begin any OpenGL related statement as glBegin, close with glEnd, etc.

    for surface in surfaces: #for all individual surface in the main tuple of surfaces
        x = 0 #depending on placement of x within code blocks, different coloring effects occur
        
        for vertex in surface: #fills entire space in all surface
            x+=1 #with x+=1 set here, gradient occurs on all faces
            glColor3fv(colors[x]) #color command
            glVertex3fv(vertices[vertex])
        
    glEnd()
    
    glBegin(GL_LINES) #specify a constant to notify opengl what type of graphic is generate
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex]) #draws and connects vertices
    glEnd() #and end it with this

# Remember, typically x is defined as left/right, y is up/down, and z is near/far

def main():
    pygame.init() #required for pygame
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) #specify double framebuffer constant through opengl


    max_distance = 100

    gluPerspective(45, (display[0]/display[1]), 0.1, max_distance) #field of view, aspect ratio, 'clipping plane' or object seethrough distance close and far
                                         #z-near^    ^z-far
    glTranslatef(0,0, -40) #x, y, z params for moving around object z starts zoomed out

    #object_passed = False #player starts out not touching or passing object, therefore object_passed = False

    x_move = 0 #used for allowing keypress hold down instead of 
    y_move = 0 #multiple keypress. better stored as var

    cur_x = 0
    cur_y = 0

    game_speed = 2 #modify to compensate for lag
    direction_speed = 2

    cube_dict = {} #container for all cube vertices and their keys

    for x in range(50):
        cube_dict[x] =set_vertices(max_distance) #creates 75 cubes dictionary for use in game
    
    #glRotatef(25, 2, 1, 0) #degrees as x, y, z

    while True: #game loop, while object is not passed
        for event in pygame.event.get(): #general event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: #if keypresses are inverted*, control seems to shift away from "cube control" to "player" or "screen" - depending on the modification of axes, the player's experience of what they control is defined
                if event.key == pygame.K_LEFT:
                    x_move = direction_speed
                if event.key == pygame.K_RIGHT:
                    x_move = -1*direction_speed
                    
                if event.key == pygame.K_UP:
                    y_move = -1*direction_speed
                if event.key == pygame.K_DOWN:
                    y_move = direction_speed


            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0
                    
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0

##            if event.type == pygame.MOUSEBUTTONDOWN: #mousewheel roll, forward is 4 backward is 5
##                if event.button == 4:
##                    glTranslatef(0,0,1.0) #z coordinate refers to zoom
##
##                if event.button == 5:
##                    glTranslatef(0,0, -1.0)
                
        #glRotatef(random.randrange(-5,5), random.randrange(-5,5), random.randrange(-5,5), random.randrange(-5,5)) #opengl active rotate command, params dictate dimensions, speed, etc

        x = glGetDoublev(GL_MODELVIEW_MATRIX) #obtains location in OpenGL
        #print(x) #prints those locations
        
        #foreword: this applies to FIRST vertex in vertices


        camera_x = x[3][0] #defines points of player size, if cube meets any of these params = game end
        camera_y = x[3][1]
        camera_z = x[3][2]


        cur_x += x_move
        cur_y += y_move



        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #cleanup, clears the frame with a fill 

        glTranslatef(x_move,y_move,game_speed) #throughout the while loop, iterates the cube through translate after clearing. Negative is outward (zfar), etc


        
        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])


        #infinite spawn after camerapass
        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
                new_max = int(-1*(camera_z-(max_distance*2)))

                cube_dict[each_cube] = set_vertices(new_max,int(camera_z-max_distance), cur_x, cur_y) #prevents cubes from spawning too close, starts them out past clipping plane

                
        
        pygame.display.flip() #pygame.display.update does not work here
        #pygame.time.wait(10)

main()
pygame.quit()
quit()
