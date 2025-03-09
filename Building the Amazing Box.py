from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_width, W_height = 2000, 700

freeze = False
speed = 0.5
blink = False
directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
points = []




def createpoint(x, y):
  diagonalx, diagonaly = random.choice(directions)
  color = []  
    
  for i in range(3):  #for R G B
    randomvalue = random.uniform(0, 1)  #
    color.append(randomvalue)

  
  
  point={
      'x': x,
      'y': y,
      'diagonalx': diagonalx,
      'diagonaly': diagonaly,
      'color': color,
      'stored_color': color[:],
      
  }
  points.append(point)

 

def drawpoints():
    for i in points:
        glColor3f(*i['color'])
        glPointSize(8)
        glBegin(GL_POINTS)
        glVertex2f(i['x'], i['y'])
        glEnd()




def updatepoints():
    global points, freeze  
    if not freeze:  
        for i in points:
            i['x'] += i['diagonalx'] * speed
            i['y'] += i['diagonaly'] * speed
        bounceback()  
    else:
      return None

    glutPostRedisplay() 

def bounceback():
    global points, W_width, W_height 

    for i in points:
        if i['x'] <= -W_width // 2 or i['x'] >= W_width // 2:
            i['diagonalx'] *= -1
        if i['y'] <= -W_height // 2 or i['y'] >= W_height // 2:
            i['diagonaly'] *= -1

    glutPostRedisplay()  # Refresh the display

def keyboardListener(key, x, y):
    global freeze
    if key == b' ':
        freeze = not freeze

    glutPostRedisplay()


def specialKeys(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed += 1
    elif key == GLUT_KEY_DOWN:
        speed = max(1, speed - 1) 
    print(f"Speed: {speed}")  
    glutPostRedisplay()






def mouseListener(click, mousestate, x_coordinate, y_coordinate):
  
    if mousestate != GLUT_DOWN:
        return
        
    glutcoordinate_x = x_coordinate - W_width // 2
    glutcoordinate_y = W_height // 2 - y_coordinate

    


    if click == GLUT_RIGHT_BUTTON:
        createpoint(glutcoordinate_x, glutcoordinate_y)
    elif click == GLUT_LEFT_BUTTON:
        functionblinking()
        



def functionblinking():
    global points, blink
    if blink:
        for i in points:
            i['color'] = [0, 0, 0]
    else:
        for i in points:
            i['color'] = i['stored_color']
    blink = not blink
    glutPostRedisplay() 














def display():
    glClear(GL_COLOR_BUFFER_BIT)
    drawpoints()
    glutSwapBuffers()



def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W_width//2, W_width//2, -W_height//2, W_height//2, -1, 1)  # Set 2D coordinate system . it just clips the window (left, right, bottom, top, near, far)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitWindowSize(W_width, W_height)
glutInitWindowPosition(50, 50)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Building The Amazing Box")
init()
glutDisplayFunc(display)
glutIdleFunc(updatepoints)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeys)
glutMainLoop()
