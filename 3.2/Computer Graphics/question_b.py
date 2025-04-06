from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

import ctypes
# GLUT_BITMAP_TIMES_ROMAN_24 = ctypes.c_void_p(5)
# GLUT_BITMAP_HELVETICA_18 = ctypes.c_void_p(6)

step = 1
divisions = 10
begin_at = -2
extend = True

#Define Points
points = [14.2, 215,
    16.4, 325,
    11.9, 185,
    15.2, 332,
    18.5, 406,
    22.1, 522,
    19.4, 412,
    25.1, 614,
    23.4, 544,
    18.1, 421,
    22.6, 445,
    17.2, 408]

#Functions
#plot a point given x and y coordinates
def plot_point(x, y): 
    glColor3f(0.0, 0.0, 1.0) #blue colour 
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

#returns a new list of points for the best fit line
def bestfit(points):
    #Uses the least squares regression method
    #formula is gradient = (N Σ(xy) − Σx Σy) / (N Σ(x^2) − (Σx)^2)
    #y-intecept =  Σy − m Σx/  N

    n = len(points) / 2

    newpoints = []

    sum_x = sum_y =  sum_xy = sum_x_sq = 0

    for i in range(0, len(points), 2):
        sum_x += points[i]
        sum_y += points[i+1]
        sum_xy += (points[i] * points[i+1])
        sum_x_sq += (points[i] * points[i])

    gradient = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x_sq) - (sum_x * sum_x))
    y_intercept = (sum_y - (gradient * sum_x)) / n

    #generate new points using the new equation of the line
    #x-coords: (x-10) / 2 to fit the scale
    # y-coords: y/100 
    for i in range(0, len(points), 2):
        new_x = (points[i] - 10) / 2
        new_y = (((gradient * points[i]) + y_intercept)) / 100
        newpoints.append(new_x)
        newpoints.append(new_y)

    if extend:
        #extend the line
        x1 = 10
        new_x1 = (x1 - 10) / 2
        new_y1 = (((gradient * x1) + y_intercept)) / 100
        newpoints.append(new_x1)
        newpoints.append(new_y1)

        x2 = 26
        new_x2 = (x2 - 10) / 2
        new_y2 = (((gradient * x2) + y_intercept)) / 100
        newpoints.append(new_x2)
        newpoints.append(new_y2)

    return newpoints

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0) #background colour
    glColor3f(0.0, 0.0, 1.0) #Point color
    glPointSize(6.0) #Point size
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(begin_at, divisions, begin_at, divisions)

def draw_scale():
    glColor3f(0.8, 0.8, 0.8) # Light gray for the scale
    glBegin(GL_LINES)
    for i in range(0, divisions, step):
        glVertex2f(i, 0) # Start at 0 on y axis
        glVertex2f(i, divisions) #End at number of divisions on y axis
        glVertex2f(0, i) #Start at 0 on x axis
        glVertex2f(divisions, i)#End at divisions on x axis
    glEnd()

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

#draw the label text in a different font
def draw_text_label(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

#draw the numbers in scale and axis names 
def draw_labels():
    glColor3f(0.0, 0.0, 0.0) # Black color for labels

    #X-axis
    for i in range(0, 11, step):
        draw_text(i, -0.5, str(10 + (2 * i)))

    #Y-axis labels (0 to 10, multiplied by 100)
    for i in range(0, 11, step):
        draw_text(-0.7, i, str(f"${(i * 100)}")) #// Dollar sign and multiplied value

    #Add axis names
    draw_text_label(4, -1.0, str("Temperature °C")) #X-axis name
    draw_text_label(-1.5, 5, str("Sales")) # Y-axis name

#draws a line given a set of points
from OpenGL.GL import *

def drawLineStrip(points):
    if len(points) < 2:  # Need at least two points
        return

    glColor3f(1.0, 0.6471, 0.0)  # Orange color
    glLineWidth(5.0)
    glEnableClientState(GL_VERTEX_ARRAY)
    
    # Convert the points list to a ctypes array
    points_array = (GLfloat * len(points))(*points)
    glVertexPointer(2, GL_FLOAT, 0, points_array)
    
    glDrawArrays(GL_LINE_STRIP, 0, len(points) // 2)  # Divide by 2 because each point has 2 coordinates
    
    glDisableClientState(GL_VERTEX_ARRAY)
    glLineWidth(1.0)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_scale()
    draw_labels()
    
    #points
    for i in range (0, len(points), 2):
        x_coord = (points[i] - 10) / 2
        y_coord = points[i+1] / 100
        plot_point(x_coord, y_coord)

    #Best fit line
    mypoints = bestfit(points)
    drawLineStrip(mypoints)

    glFlush()

def mainLoop():
    glutMainLoop()



def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(1000, 1000)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("Group 10 Question B")

    init()
    glutDisplayFunc(display)
    mainLoop()

main()













