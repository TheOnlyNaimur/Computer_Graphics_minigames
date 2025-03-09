#task1

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_Width, W_Height = 2000, 700  # Window size
sky_brightness = 1 # Brightness of the sky
rain_drops = []
rain_angle = 0 

def createrain():
    global rain_drops
    drops = 500  # Increase number of drops for better coverage
    for i in range(drops):
        x = random.randint(-2000, 2000)  # Covers full width
        y = random.randint(-700, 700)  # Start above the screen
        rain_drops.append([x, y])



def drawrains():
    glColor3f(0, 0, 1)  # Blue color
    glBegin(GL_LINES)  
    for drop in rain_drops:
        drop_length = 30  # Increase drop length
        glVertex2f(drop[0], drop[1])  # Start point drop[0] is the x-coordinate of the rain drop. drop[1] is the y-coordinate of the rain drop.
        glVertex2f(drop[0] + rain_angle, drop[1] - drop_length) # End point
    glEnd()

def animateRain(value):
    global rain_drops
    for drop in rain_drops:
        drop[0] += rain_angle  
        drop[1] -= 30  # Move down
        
        if drop[1] < -700:  # If raindrop falls below ground
            drop[0] = random.randint(-2000, 2000)  # Reset 
            drop[1] = random.randint(700, 700)
    
    glutPostRedisplay() # Refresh the display
    glutTimerFunc(30, animateRain, 0)  #animateRain to run again after 30 milliseconds.
                                            



def specialKeys(key, x, y):
    global rain_angle
    if key == GLUT_KEY_LEFT:
        rain_angle = max(-10, rain_angle - 1)  # Bend left
    elif key == GLUT_KEY_RIGHT:
        rain_angle = min(10, rain_angle + 1)  # Bend right limit max angle
    glutPostRedisplay()


def drawShapes(): 
    glBegin(GL_QUADS)  # house
    glColor3f(255, 255, 255)  # Green color
    glVertex2f(-700, -190)
    glVertex2f(700, -190)
    glVertex2f(700, 190)
    glVertex2f(-700, 190)
    glEnd()

    glBegin(GL_TRIANGLES)  # shed
    glColor3f(1, 1, 0)  
    glVertex2f(-900, 150)
    glVertex2f(900, 150)
    glVertex2f(0, 400)
    glEnd()

    glBegin(GL_QUADS)  # Door
    glColor3f(1, 0, 1)  
    glVertex2f(-100, -190)
    glVertex2f(100, -190)
    glVertex2f(100, 50)
    glVertex2f(-100, 50)
    glEnd()

    glBegin(GL_QUADS)  # Door lock
    glColor3f(0, 0, 0)  
    glVertex2f(60, -90) 
    glVertex2f(80, -90)
    glVertex2f(80, -70)
    glVertex2f(60, -70)
    glEnd()

    glBegin(GL_QUADS)  #right window
    glColor3f(1, 0, 1)  
    glVertex2f(200, -50) 
    glVertex2f(400, -50) 
    glVertex2f(400, 50) 
    glVertex2f(200, 50) 
    glEnd()
    glBegin(GL_QUADS)  #left window 
    glColor3f(1, 0, 1)  
    glVertex2f(-400, -50) #bottomleft
    glVertex2f(-200, -50) #bottomright
    glVertex2f(-200, 50) #topright
    glVertex2f(-400, 50) #topleft
    glEnd()

    glBegin(GL_LINES)  #left window line
    glColor3f(0, 0, 0)  
    glVertex2f(-400, 0) 
    glVertex2f(-200, 0) 

    glEnd()

    glBegin(GL_LINES)  #left window line
    glColor3f(0, 0, 0)  
    glVertex2f(-300, 50) 
    glVertex2f(-300, -50) 

    glEnd()

    glBegin(GL_LINES)  #right window line
    glColor3f(0, 0, 0)  
    glVertex2f(200, 0) 
    glVertex2f(400, 0) 
 
    glEnd()   
    glBegin(GL_LINES)  #right window line
    glColor3f(0, 0, 0)  
    glVertex2f(300, 50) 
    glVertex2f(300, -50) 

    glEnd()


def drawbackgrounds():
    global sky_brightness  
    glBegin(GL_QUADS)  # sky
    glColor3f(sky_brightness,sky_brightness,sky_brightness)
    glVertex2f(-2000, 350) #bottomleft
    glVertex2f(2000, 350) #bottomright
    glVertex2f(2000, 700) #topright
    glVertex2f(-2000, 700) #topleft
    glEnd()

    glBegin(GL_QUADS)  #ground
    glColor3f(0.55, 0.47, 0.14)  # deep bronze color
    glVertex2f(-2000, -700) #bottomleft
    glVertex2f(2000, -700) #bottomright
    glVertex2f(2000, 351) #topright
    glVertex2f(-2000, 351) #topleft
    glEnd()

def keyboard_listener(key, x, y):
    global sky_brightness

    if key == b'w':  # Darken sky
        sky_brightness = max(0.0, sky_brightness - 0.09)  # wont go below 0
        print(f"Darkening Sky: {sky_brightness}")
    elif key == b's':  # Brighten sky
        sky_brightness = min(1.0, sky_brightness + 0.09)  # wont exceed 1
        print(f"Brightening Sky: {sky_brightness}")

    glutPostRedisplay()






def drawbackgroung_trees():
    space = 200  
    width = 200  
    height = 150   
    base = 200        

    for i in range(-2000 + (space // 2), 2000 + space, space): 
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 0.8, 0.0)  # Green color
        glVertex2f(i - width / 2, base)
        glVertex2f(i + width / 2, base)
        glVertex2f(i, base + height)
        glEnd()




def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
    glLoadIdentity()
    drawbackgrounds()
    drawbackgroung_trees()
    drawShapes()  
    drawrains() 
    glutSwapBuffers() #This function swaps the front and back buffers in double buffering
    gluLookAt(0,0,5,	0,0,0,	0,1,0) #camera view gluLookAt(eyeX, eyeY, eyeZ,  targetX, targetY, targetZ,  upX, upY, upZ)
 
    glMatrixMode(GL_MODELVIEW) #This tells OpenGL to switch to Model-View mode (used for transformations like moving objects, rotating, or scaling).

def init():
    glClearColor(0, 0, 0, 0) # Set the clear color to black
    glMatrixMode(GL_PROJECTION) #function tells OpenGL to operate on the projection matrix
    glLoadIdentity() #This function resets the current matrix to the identity matrix
    glOrtho(-1500, 1500, -700, 700, -1, 1)  # it just clips the window (left, right, bottom, top, near, far)
    glMatrixMode(GL_MODELVIEW) #

glutInit() #This function initializes the GLUT library
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0) #This function specifies the position of the window created by GLUT
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"shapes") #This function creates a top-level window
init()

glutDisplayFunc(display)  
glutKeyboardFunc(keyboard_listener)  
glutSpecialFunc(specialKeys)
glutTimerFunc(50, animateRain, 0)
createrain()
glutMainLoop()  