
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


catcher_x = 250 #horizontal position 500 width screen
catcher_width = 100

diamond_x = random.choice([10, 490])
diamond_y = 440

diamond_visible = True

score = 0
freeze = False
catcher_color = 'white'
catched = False
diamond_color = [random.random(), random.random(), random.random()]

speed_increase_interval = 2000  # Increase speed every 2000 milliseconds
current_time = 0
elapsed_time=0
current_speed = 3
speed_increase = 0.1  # Amount to increase speed
pause= False

def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()



def drawLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):  # zone 0, 3, 4, and 7
        if dx >= 0:
            if dy >= 0:
                drawLine_0(x0, y0, x1, y1, 0)
            else:
                drawLine_0(x0, -y0, x1, -y1, 7)

        else:
            if dy >= 0:
                drawLine_0(-x0, y0, -x1, y1, 3)
            else:
                drawLine_0(-x0, -y0, -x1, -y1, 4)

    else:  # zone 1, 2, 5, and 6
        if dx >= 0:
            if dy >= 0:
                drawLine_0(y0, x0, y1, x1, 1)
            else:
                drawLine_0(y0, -x0, y1, -x1, 6)

        else:
            if dy >= 0:
                drawLine_0(-y0, x0, -y1, x1, 2)
            else:
                drawLine_0(-y0, -x0, -y1, -x1, 5)


def drawLine_0(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    delE = 2 * dy
    delNE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x0
    y = y0
    while x < x1:
        draw8way(x, y, zone)

        if d < 0:
            d += delE
            x += 1

        else:
            draw8way(x, y, zone)
            d += delNE
            x += 1
            y += 1


def draw8way(x, y, zone):
    if zone == 0:
        draw_points(x, y)  # glpoints

    if zone == 1:
        draw_points(y, x)

    if zone == 2:
        draw_points(-y, x)
    if zone == 3:
        draw_points(-x, y)
    if zone == 4:
        draw_points(-x, -y)
    if zone == 5:
        draw_points(-y, -x)
    if zone == 6:
        draw_points(y, -x)
    if zone == 7:
        draw_points(x, -y)


def drawCatcher():
    global catcher_x, catcher_width, catcher_color
    if catcher_color=='white':
        glColor3f(1, 1, 1)
    else:
        glColor3f(1, 0, 0)

    drawLine(catcher_x, 0, catcher_x + catcher_width, 0)
    drawLine(catcher_x + catcher_width, 0, catcher_x + catcher_width + 25, 20)
    drawLine(catcher_x - 25, 20, catcher_x + catcher_width + 25, 20)
    drawLine(catcher_x - 25, 20, catcher_x, 0)



def animation(value):
    global diamond_x, diamond_y, diamond_visible, score, freeze, catcher_color, catched, diamond_color
    global current_time, current_speed, elapsed_time, pause

    if not pause:  # Only update if the game is not paused
        if diamond_visible:
            diamond_y -= current_speed

            if catcher_x - 25 <= diamond_x <= catcher_x + catcher_width + 25 and diamond_y <= 20:
                diamond_visible = False
                catched = True
                score += 1
                print('Score:', score)
                diamond_y = 440
                diamond_x = random.randint(10, 490)
                diamond_visible = True

            if diamond_y < 20:
                catcher_color = 'red'
                print('Game Over!!! Score:', score)
                freeze = True
                glutPostRedisplay()
                return

        drawCatcher()

        elapsed_time = glutGet(GLUT_ELAPSED_TIME)
        if elapsed_time - current_time > speed_increase_interval:
            current_speed += speed_increase
            current_time = elapsed_time

        # Change color of the diamond if caught
        if catched:
            diamond_color = [random.random(), random.random(), random.random()]
            catched = False

        glColor3f(*diamond_color)


    glutPostRedisplay()
    glutTimerFunc(16, animation, 0)

def mouseListener(button, state, x, y):
    global freeze, pause, diamond_x, diamond_y, diamond_visible, score, catcher_color, catched, diamond_color
    global current_time, current_speed, elapsed_time
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_X = x
        c_y = y
        #print(c_X, c_y)

        ###restart button
        if 0 <= c_X <= 50 and 0 <= c_y <= 50:

            print('Starting over!!!')
            diamond_x = random.choice([10, 490])
            diamond_y = 440
            diamond_visible = True
            score = 0
            freeze = False
            catcher_color = 'white'
            catched = False
            diamond_color = [random.random(), random.random(), random.random()]
            current_time = 0
            current_speed = 3
            elapsed_time = 0

            glutTimerFunc(30, animation, 0)
        ###pause button
        if 200 <= c_X <= 300 and 0 <= c_y <= 50:
            pause = not pause
            if pause:
                print('Game Paused!')
            else:
                print('Game Resumed!')
        ### cross button
        if 400 <= c_X <= 500 and 0 <= c_y <= 50:
            print('Goodbye! Score:', score)
            glutLeaveMainLoop()
        glutPostRedisplay()

def specialKeyListener(key, x, y):
    global catcher_x

    if not pause and not  freeze: ###false means catcher can move

        if key == GLUT_KEY_RIGHT:
            catcher_x += 10
        elif key == GLUT_KEY_LEFT:
            catcher_x -= 10
    else: ###true means gameover so catcher will stopp moving
        glColor3f(1, 0, 0)
        return
    # Ensure the catcher does not go beyond window boundaries
    if catcher_x-25 < 0:
        catcher_x = 25
    elif catcher_x + catcher_width+25 > 500:
        catcher_x = 500 - catcher_width - 25

    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 500, 0.0, 500)  # Use gluOrtho2D for 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # Arrow key
    glColor3f(0, 128, 128)
    drawLine(10, 470, 30, 470)
    drawLine(10, 470, 20, 480)
    drawLine(10, 470, 20, 460)  ###window ta (0,0) (500,500)###

    # pause resume PART

    if  not pause: ###pause button
        glColor3f(255, 191, 0)
        drawLine(240, 460, 240, 480)
        drawLine(250, 460, 250, 480)

    else:          ###play button
        glColor3f(255, 191, 0)
        drawLine(240, 460, 240, 480)
        drawLine(240, 480, 250, 470)
        drawLine(240, 460, 250, 470)


    # cross
    glColor3f(1, 0, 0)
    drawLine(440, 460, 460, 480)
    drawLine(440, 480, 460, 460)


    # Diamond draw
    glColor3f(1, 0, 0)
    if diamond_visible:
        if freeze:  # Game over, diamond turns black
            glColor3f(0, 0, 0)
        else:
            glColor3f(*diamond_color)

        drawLine(diamond_x, diamond_y, diamond_x + 10, diamond_y + 10)
        drawLine(diamond_x - 10, diamond_y + 10, diamond_x, diamond_y)
        drawLine(diamond_x - 10, diamond_y + 10, diamond_x, diamond_y + 20)
        drawLine(diamond_x, diamond_y + 20, diamond_x + 10, diamond_y + 10)

    drawCatcher()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutDisplayFunc(showScreen)
glutTimerFunc(0, animation, 0)
glutMainLoop()
