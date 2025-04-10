#include <GL/glut.h>
#include <vector>
#include <iostream>
using namespace std;

int step = 1;
int divisions = 10;
int begin_at = -2;
char extend = 't';
int extendlist[] = {10, 26};

//Define Points
vector<float> points = {
    14.2, 215,
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
    17.2, 408
};

//Functions
void plot_point(float x, float y);
vector<float> bestfit(const vector<float>& points);
void init();
void draw_scale();
void draw_text(float x, float y, const string& text);
void draw_text_label(float x, float y, const string& text);
void draw_labels();
void drawLineStrip(const vector<float>& points);
void display();
void mainLoop();


int main(int argc, char** argv) {

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(1000, 1000);
    glutInitWindowPosition(500, 100);
    glutCreateWindow("Group 10 Question B");

    init();
    glutDisplayFunc(display);
    mainLoop();

    return 0;
}

//plot a point given x and y coordinates
void plot_point(float x, float y) {
    glColor3f(0.0f, 0.0f, 1.0f); //blue colour 
    glBegin(GL_POINTS);
    glVertex2f(x, y);
    glEnd();
}

//returns a new list of points for the best fit line
vector<float> bestfit(const vector<float>& points){
    //Uses the least squares regression method
    // formula is gradient = (N Σ(xy) − Σx Σy) / (N Σ(x^2) − (Σx)^2)
    // y-intecept =  Σy − m Σx/  N
    float gradient;
    float y_intercept;
    float n = points.size() / 2;

    vector<float> newpoints;

    float sum_x = 0;
    float sum_y = 0;
    float sum_xy = 0;
    float sum_x_sq = 0;

    for (size_t i = 0; i < points.size(); i+=2){
        sum_x += points.at(i);
        sum_y += points.at(i+1);
        sum_xy += (points.at(i) * points.at(i+1));
        sum_x_sq += (points.at(i) * points.at(i));
    }

    gradient = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x_sq) - (sum_x * sum_x));
    y_intercept = (sum_y - (gradient * sum_x)) / n;

    //generate new points using the new equation of the line
    // x-coords: (x-10) / 2 to fit the scale
    // y-coords: y/100 
    for (size_t i = 0; i < points.size(); i+=2){
        float new_x = (points.at(i) - 10) / 2;
        float new_y = (((gradient * points.at(i)) + y_intercept)) / 100;
        newpoints.push_back(new_x);
        newpoints.push_back(new_y);
    }
    if (extend == 't'){
        for (size_t i = 0; i < sizeof(extendlist) / sizeof(extendlist[0]); i++){
            //extend the line
            int x1 = extendlist[i];
            float new_x1 = (x1 - 10) / 2;
            float new_y1 = (((gradient * x1) + y_intercept)) / 100;
            newpoints.push_back(new_x1);
            newpoints.push_back(new_y1);
        }
    }

        //extend the line
    //     int x1 = 10;
    //     float new_x1 = (x1 - 10) / 2;
    //     float new_y1 = (((gradient * x1) + y_intercept)) / 100;
    //     newpoints.push_back(new_x1);
    //     newpoints.push_back(new_y1);

    //     int x2 = 26;
    //     float new_x2 = (x2 - 10) / 2;
    //     float new_y2 = (((gradient * x2) + y_intercept)) / 100;
    //     newpoints.push_back(new_x2);
    //     newpoints.push_back(new_y2);
    // }


    return newpoints;
}

void init() {
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f); //background colour
    glColor3f(0.0f, 0.0f, 1.0f); // Point color
    glPointSize(6.0f); // Point size
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(begin_at, divisions, begin_at, divisions);
}

void draw_scale() {
    glColor3f(0.8f, 0.8f, 0.8f); // Light gray for the scale
    glBegin(GL_LINES);
    for (int i = 0; i < divisions; i += step) {
        glVertex2f(i, 0); // Start at 0 on y axis
        glVertex2f(i, divisions); // End at number of divisions on y axis
        glVertex2f(0, i); // Start at 0 on x axis
        glVertex2f(divisions, i); // End at divisions on x axis
    }
    glEnd();
}

void draw_text(float x, float y, const string& text) {
    glRasterPos2f(x, y);
    for (char c : text) {
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, c);
    }
}

//draw the label text in a different font
void draw_text_label(float x, float y, const string& text) {
    glRasterPos2f(x, y);
    for (char c : text) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c);
    }
}

//draw the numbers in scale and axis names 
void draw_labels() {
    glColor3f(0.0f, 0.0f, 0.0f); // Black color for labels

    // X-axis
    for (int i = 0; i < divisions; i += step) {
        draw_text(i, -0.5f, to_string(10 + (2 * i)));
    }

    // Y-axis labels (0 to 10, multiplied by 100)
    for (int i = 0; i < divisions; i += step) {
        draw_text(-0.7f, i, "$" + to_string(i * 100)); // Dollar sign and multiplied value
    }

    // Add axis names
    // x position / 2 so that it is always centered same for the y axis
    draw_text_label((divisions / 2) - 1, -1.0f, "Temperature °C"); // X-axis name
    draw_text_label(-1.5f, (divisions / 2), "Sales"); // Y-axis name
}

//draws a line given a set of points
void drawLineStrip(const vector<float>& points) {
    if (points.size() < 2) return; // Need at least two points

    glColor3f(1.0f, 0.6471f, 0.0f); //orange colour
    glLineWidth(5.0f);
    glEnableClientState(GL_VERTEX_ARRAY);
    glVertexPointer(2, GL_FLOAT, 0, points.data());
    glDrawArrays(GL_LINE_STRIP, 0, points.size() / 2); // Divide by 2 because each point has 2 coordinates
    glDisableClientState(GL_VERTEX_ARRAY);
    glLineWidth(1.0f);
  }

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    draw_scale();
    draw_labels();
    
    //points
    for (size_t i = 0; i < points.size(); i+=2){
        float x_coord = (points.at(i) - 10) / 2;
        float y_coord = points.at(i+1) / 100;
        plot_point(x_coord, y_coord);
    }
    
    //Best fit line
    vector<float> mypoints = bestfit(points);
    drawLineStrip(mypoints);

    glFlush();
}

void mainLoop() {
    glutMainLoop();
}
