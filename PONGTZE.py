import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.locals import *
import math
import time

# Create main menu
def menu():
    sel=True
    mode=1
    while sel:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0,0,0,0)

        glColor3f(0.6,0.2,1)
        x = 300
        for i in range (100):
            y = 500
            for j in range (100):
                glPushMatrix()
                glTranslatef(x, y, 0.0)
                glScalef(7.2 / 30, 15 / 30, 0.1 / 30)
                title = "PONG GAME"
                for i in range(len(title)):
                    glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(title[i]))
                glPopMatrix()
                y += 0.01
            x += 0.01

        glColor3f(1,0.6,0.6)
        glLineWidth(3)
        glPushMatrix()
        glTranslatef(100, 400, 0.0)
        glScalef(3/ 30, 8 / 30, 0.1 / 30)
        title_1 = "PRESS TRIANGLE TO START"
        for i in range(len(title_1)):
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(title_1[i]))
        glPopMatrix()

        glColor3f(0, 0.8, 0.8)
        glLineWidth(3)
        glPushMatrix()
        glTranslatef(100, 300, 0.0)
        glScalef(3 / 30, 8 / 30, 0.1 / 30)
        title_1 = "INFOMATIONS"
        for i in range(len(title_1)):
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(title_1[i]))
        glPopMatrix()

        glColor3f(0.8,1,1)
        glLineWidth(3)
        glPushMatrix()
        glTranslatef(100, 250, 0.0)
        glScalef(3 / 30, 8 / 30, 0.1 / 30)
        title_1 = "LEFT PLAYER PRESS W FOR UP AND S FOR DOWN"
        for i in range(len(title_1)):
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(title_1[i]))
        glPopMatrix()

        glColor3f(1, 0.8, 0.9)
        glLineWidth(3)
        glPushMatrix()
        glTranslatef(100, 200, 0.0)
        glScalef(3 / 30, 8 / 30, 0.1 / 30)
        title_1 = "RIGHT PLAYER PRESS O FOR UP AND L FOR DOWN"
        for i in range(len(title_1)):
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(title_1[i]))
        glPopMatrix()

        glColor3f(0, 0.8, 0.8)
        glLineWidth(3)
        glPushMatrix()
        glTranslatef(100, 150, 0.0)
        glScalef(3 / 30, 8 / 30, 0.1 / 30)
        title_1 = "AFTER HITS, SPEED OF BALL INCREASES"
        for i in range(len(title_1)):
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(title_1[i]))
        glPopMatrix()

        glColor3f(0,0.8,0.8)
        glLineWidth(3)
        glPushMatrix()
        glTranslatef(100, 100, 0.0)
        glScalef(3 / 30, 8 / 30, 0.1 / 30)
        title_1 = "GAME OVER WHEN BALL HITS WALL"
        for i in range(len(title_1)):
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(title_1[i]))
        glPopMatrix()

        mouse_1 = pygame.mouse.get_pos()
        click_1 = pygame.mouse.get_pressed()

        if 745 > mouse_1[0] > 647 and 530 > mouse_1[1] > 212:
            glColor3f(0, 1, 0)
            if click_1[0]==1:
                sel=False

        else:
            glColor3f(1,1,1)
        glBegin(GL_TRIANGLES)
        glVertex3f(550, 300, 0)
        glVertex3f(750, 150, 0)
        glVertex3f(550, 10, 0)
        glEnd()
        pygame.display.flip()

    return mode

# this function draws a quad within a given size and a position
def draw_quad(width, height, x, y):
    # initializing the quad's coordinates
    quad_verts = [[x,y,0], [width + x, y, 0], [width + x,height + y,0], [x, height + y, 0]]
    # begining the opengl in intermidate mode for rendering
    glBegin(GL_QUADS)
    # for each coordinate, draw it
    for vert in quad_verts:
        glVertex3fv(vert)
    # rendering is done here
    glEnd()

# this function checks box collision detection, returns a boolean value( True/False) respectively.
def box_collision(x1,y1,width1,height1,x2,y2,width2,height2):
    if((x1 + width1 >= x2) and (x1 <= (x2 + width2)) and ((y1 + height1) >= y2) and (y1 <= (y2 + height2))):
        return True
    else:
        return False

# this class represents a paddle in a pong game
class paddle:
    # the paddle has a width and a height, and a position in the screen
    # this function initializes the paddle's properties(width, height, position)
    def __init__(self, player_one=True):
        self.width = 25
        self.height = 140
        self.posx = 20
        self.posy = 50
        if(player_one == False):
            self.posx = screen_width - self.width - self.posx


    # this function draws the paddle with his given current parameters(size and position)
    def draw_paddle(self):
        draw_quad(self.width, self.height, self.posx, self.posy)
        return
    # this function will move the paddle's position up
    def move_up(self):
        # checking boundaries first
        if(self.posy < (screen_height - self.height - 10)):
            self.posy += 7
    # this function will move the paddle's position down
    def move_down(self):
        if(self.posy > (10)):
            self.posy -= 7

    # this function returns the paddle's x coordinate
    def get_posx(self):
        return self.posx

    # this function returns the paddle's y coordinate
    def get_posy(self):
        return self.posy

# this function represents a ball in a pong's game
class ball:
    # the ball has a size, a position(x and y coordinates), and directions(which represents the speed(a.k.a speed vectors))
    def __init__(self):
        self.size = 25
        self.posx, self.posy = screen_width / 2, screen_height / 2
        self.dirx, self.diry = 3,3

    # this function draws the ball
    def draw_ball(self, i):
        # changes the color of the ball over time
        glColor3f(math.sin(i), 0.8, 0.6)
        # draws the ball
        draw_quad(self.size, self.size, self.posx, self.posy)
        # changes the drawing color back to stock white
        glColor3f(1.0,1.0,1.0)
    # this function detects the ball's collisions with either the paddle or the boundaries and updates the direction respectively.
    def ball_collision(self):
        global players
        # calculating the ball's collision with the boundaries
        calc = screen_height - self.posy - self.size
        if(calc >= (screen_height - self.size) or calc <= 10 ):
            self.diry *= -1

        # calculating the ball's collision with the paddle's(players)
        for player in players:
            # if there is a collision, negate the direction of the ball in the x direction
            if(box_collision(self.posx, self.posy, self.size, self.size, player.get_posx(), player.get_posy(), player.width, player.height) == True):
                self.dirx *= -1
                # make the ball move faster as well
                if(self.dirx < 0):
                    self.dirx -= 1
                    self.diry -= 1
                else:
                    self.dirx += 1
                    self.diry += 1
                print("ball speed is:", abs(self.dirx))
    # if the game is over, close the game
    def is_game_over(self):
        global game_over
        if((self.posx+ self.size) > (screen_width - self.size) or (self.posx <= 0)):
            game_over = True
            print("game over!")

    # this function updates the ball's position
    def move_ball(self):
        self.ball_collision()
        self.posx += self.dirx
        self.posy += self.diry

# the game loop draw function, everything graphically displayed is drawn here
def draw(i):
    global players
    for player in players:
        player.draw_paddle()
    ball_one.draw_ball(i)

# the game loop update function, everything logically is updated right here
def update():
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_s]:
        players[0].move_down()
    elif keystate[pygame.K_w]:
        players[0].move_up()
    if keystate[pygame.K_o]:
        players[1].move_up()
    elif keystate[pygame.K_l]:
        players[1].move_down()

    # update ball position
    ball_one.move_ball()
    ball_one.is_game_over()

# screen size globals
global screen_width
global screen_height
global players
global game_display
# initializing the screen size globals
screen_width = 800
screen_height = 600
players = [paddle(), paddle(player_one=False)]

# initializing the game over flag
game_over = False

# the main function of the game, runs everything in order
if __name__ == '__main__':
    global game_display
    glutInit(sys.argv)
    pygame.init()
    display = (screen_width, screen_height)
    game_display = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Bouncing Balls Game")
    glOrtho(0, screen_width, 0, screen_height, 0, 1)
    menu()

    # initializing the ball
    ball_one = ball()
    i = 0
    # while the game is running, take care of events
    while True:
        if game_over == True:
            quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # drawing the scene
        draw(i)
        # updating the scene
        update()
        # sleeping in order to keep the frame rate consistent
        time.sleep(0.015)
        # updating the screen(swapping buffers)
        pygame.display.flip()
        i += 0.01
