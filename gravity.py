# 0.8 - Moving over to pygame

import sys
import time
import pygame
import math
import numpy as np

sys.path.append('./modules')

import amath

from spacemath import *

TIME = 0.01
    
SCALE = 0.01
VIEW = "TOP"

G = 6.6743 * 10**-11
SOLAR_MASS = 10**8

STANDARD_MASS = 10**6

ENABLE_PLANETS = True
ENABLE_DWARFS = not True
ENABLE_ASTEROIDS = not True
ENABLE_MISC = not True

WIDTH = 1600
HEIGHT = 1000
TITLE = "Gravity Simulation"
BACKGROUND_COLOR = "#080f20"
CONTENTS_FOLDER = "contents"
ICON = "icon.png"
SUNFLARE = "sunflare.png"

config_file = True

if config_file == True:
    var1,var2,var3,var4="config","not","working","properly"
    file = open("settings.cfg")
    config_dict = {}
    replace_dict = {
        "\n"  : "",
        ":"   : "=",
        " = " : "=",
        }
    for line in file:
        if "=" in line or ":" in line:
            for r, w in replace_dict.items():
                line = line.replace(r,w)
            items = line.split('=', 1)
            if "#" in items[1]:
                config_dict[items[0]] = str(items[1])
                continue
            try:
                config_dict[items[0]] = eval(items[1])
            except NameError:
                config_dict[items[0]] = str(items[1])
            except SyntaxError:
                config_dict[items[0]] = str(items[1])
    globals().update(config_dict)
    print(var1,var2,var3,var4)
        
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKGROUND_COLOR)
pygame.display.set_caption(TITLE)
pygame.display.set_icon(pygame.image.load(f"{CONTENTS_FOLDER}\{ICON}"))
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
pygame.display.update()

start_solar_system = True

VIEW = VIEW.upper()
if VIEW == "TOP":
    h,v = 0,1
elif VIEW == "SIDE":
    h,v = 0,2
elif VIEW == "SIDE2":
    h,v = 1,2
else:
    h,v = 0,1

def line(color, pos1, pos2):
    pygame.draw.aaline(
        screen,
        color,
        (pos1[h]/SCALE+WIDTH/2, -pos1[v]/SCALE+HEIGHT/2),
        (pos2[h]/SCALE+WIDTH/2, -pos2[v]/SCALE+HEIGHT/2)
        )
    

class Body:
    def __init__(self, name = 'time', color = 'random', mass = 'default', position = (0,0,0), velocity = (0,0,0), immovable = False):
        self.current_time = time.time()
        time.sleep(0.01)
        
        if name == 'time':
            name = f"Object {self.current_time}"
        
        self.randomness = amath.mod(amath.trunc((amath.cos(amath.sin(self.current_time)*self.current_time))*self.current_time)**2,16**6)

        if mass == 'default':
            mass = m
        elif mass == 'random':
            mass = self.randomness*8

        if color == 'random':
            color = hex(self.randomness).replace('0x','')
            color = '#'+color.replace('0x','').zfill(6)
            
        if '§' in color:
            color = color.strip('§')
            secondary_color = color
        else:
            if '#' not in color:
                color = '#'+color
            color_hex = color.strip('#')
            RGB = []
            while color_hex:
                RGB.append(color_hex[:2])
                color_hex = color_hex[2:]
            
            secondary_color = '#'
            for n in range(3):
                color_value = int(RGB[n], 16)
                color_value -= 16
                if color_value <= 0:
                    color_value = 0
                secondary_color += hex(color_value).replace('0x','').zfill(2)

        self.name = name
        self.ID = str(self.name)+str(self.current_time)
        self.mass = mass
        self.color = color

        self.position = position
        self.init_vel = amath.hypot(velocity)
        self.velocity = velocity[0]*amath.sqrt(TIME), velocity[1]*amath.sqrt(TIME), velocity[2]*amath.sqrt(TIME)
        self.new_position = self.position

        self.immovable = immovable

        line(self.color, self.position, self.new_position)
        
        if self.name == "The Sun" and SCALE < 0.02:
            sunflare = pygame.image.load(f"{CONTENTS_FOLDER}\{SUNFLARE}")
            screen.blit(sunflare, ((WIDTH-sunflare.get_width())/2, (HEIGHT-sunflare.get_height())/2))
            

        self.FramesPerUpdate = 1/amath.sqrt(TIME)/20*amath.cbrt(SCALE)
        if self.FramesPerUpdate <= 0:
            self.FramesPerUpdate = 1

        c = 0
        if self.init_vel == 0:
            c = 0.04
        self.standardCounter = self.FramesPerUpdate/(amath.sqrt(self.init_vel)+c)
        
        self.counter = 0
        
        self.LastUpdatePosition = self.position

        print(f"\nCreated new body:"
              f"\n Name: {self.name}"
              f"\n Color: {self.color}"
              f"\n Mass: {self.mass}"
              f"\n Position: {self.position}"
              f"\n Coordinate magnitude: {amath.sqrt(self.position[0]**2+self.position[1]**2+self.position[2]**2)}"
              f"\n Velocity: {self.velocity}"
              f"\n Initial velocity: {self.init_vel}"
              f"\n Randomness key: {self.randomness}"
              f"\n Immovable: {self.immovable}"
              )


    def updateSelf(self):
        if self.immovable == True:
            self.position = (0, 0, 0)
            return
        
        elif amath.aabs(self.position[0]) > WIDTH or amath.aabs(self.position[1]) > HEIGHT:
            return
        
        if self.counter <= 0:
            line(self.color, self.LastUpdatePosition, self.position)
            self.LastUpdatePosition = self.position

            self.counter = self.standardCounter
            
        self.counter -= 1
        

def calculateDistance(position1, position2): # Returns distance between two bodies
    
    dist_x = position2[0] - position1[0]
    dist_y = position2[1] - position1[1]
    dist_z = position2[2] - position1[2]
    
    distance = amath.sqrt(dist_x**2 + dist_y**2 + dist_z**2) # Distance between the two bodies
    
    return (dist_x, dist_y, dist_z, distance)

def calculateAcceleration(body1, body2): # Returns force between two bodies
    distance = calculateDistance(body1.position, body2.position)
    
    if distance[3]**2 == 0:
        return 0

    acceleration = G * body2.mass / distance[3]**3

    acceleration_x = acceleration * distance[0]
    acceleration_y = acceleration * distance[1]
    acceleration_z = acceleration * distance[2]
    
    return np.array([acceleration_x, acceleration_y, acceleration_z])


from solar_system import *

def add_solar_system():
    global ENABLE_PLANETS, ENABLE_DWARFS, ENABLE_ASTEROIDS, ENABLE_MISC

    TEST = not True

    SUN = Body(
            "The Sun",
            "#ffff00",
            SOLAR_MASS,
            (amath.mod(time.time(),1)/(10**10), 0, 0),
            immovable = True
            )

    universe.append(SUN)
    
    universe_data = []

    if ENABLE_PLANETS:
        universe_data.extend(PLANETS)
        
    if ENABLE_DWARFS:
        universe_data.extend(DWARFS)
        
    if ENABLE_ASTEROIDS:
        universe_data.extend(ASTEROIDS)
        
    if ENABLE_MISC:
        universe_data.extend(MISC)

    if TEST:
        universe_data.extend([
            GetParameters(
                "Test","§green",1,0.6,0.5,45,60,0
                )
            ])

    for n in range(len(universe_data)):
        body_data = universe_data[n]
        universe.append(
            Body(
                body_data[0],
                body_data[1],
                body_data[2],
                body_data[3],
                body_data[4]
                )
            )

setsolarsystem = False
def set_solar_system():
    global Event, setsolarsystem
    setsolarsystem = True
    Event = True

universe = []

if start_solar_system == True:
    set_solar_system()

Event = True

def Events():
    global Event
    if Event == True:
        print("Event")
        global setsolarsystem, universe
        if setsolarsystem == True:
            universe = []
            add_solar_system()
            setsolarsystem = False
            print("Set solar system")
            
        Event = False

Events()

time.sleep(0.5)

clicked = False

# Time at start of loop
loop_start = time.time()

simulation = True

while simulation:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation = False
        if clicked == False and event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                down = pygame.mouse.get_pos()
                down = down[0]-WIDTH/2, -(down[1]-HEIGHT/2)
        elif clicked == True and event.type == pygame.MOUSEBUTTONUP:
            clicked = False
            mouse_presses = pygame.mouse.get_pressed()
            if not mouse_presses[0]:
                up = pygame.mouse.get_pos()
                up = up[0]-WIDTH/2, -(up[1]-HEIGHT/2)

                relative = np.array(up)-np.array(down)
                velocity = relative*SCALE/4
                print(down)
                universe.append(
                    Body(
                        "time",
                        "random",
                        STANDARD_MASS,
                        (down[0]*SCALE, down[1]*SCALE, 0),
                        (velocity[0], velocity[1], 0)
                        )
                    )
    
    for body in universe:
        body.acceleration = np.array([0.0, 0.0, 0.0])

        for other_body in universe:
            if other_body.mass > 10 and body.ID != other_body.ID:

                body.acceleration += calculateAcceleration(body, other_body)

        body.velocity = (body.velocity[0] + body.acceleration[0]*TIME, body.velocity[1] + body.acceleration[1]*TIME, body.velocity[2] + body.acceleration[2]*TIME)
        body.new_position = (body.position[0] + body.velocity[0], body.position[1] + body.velocity[1], body.position[2] + body.velocity[2])

    for body in universe:
        body.position = body.new_position
        body.updateSelf()
        
    pygame.display.update()

pygame.quit()

## Retired code:
        
        
##            if amath.dist3(self.LastUpdatePosition, self.position) > SCALE:#*amath.log(1/SCALE, 10):
                
##                self.LastUpdatePosition = self.position
##                
##            self.counter = self.FramesPerUpdate/(1000*amath.hypot(self.velocity))
##            print(amath.hypot(self.velocity))
##            
            
##        
##            line(self.color, self.LastUpdatePosition, self.new_position)
##            self.LastUpdatePosition = self.position
##            self.counter = self.FramesPerUpdate
##        self.counter -= 1

##        global addNew
##        if addNew == True:
##            velocity = newBodyVelocity(down_x, down_y, up_x, up_y)
##            newBody((down_x, down_y, 0), velocity, standard_mass)
##            print("new body added at", down_x, down_y)
##            addNew = False

##        global toggle_trails, trails
##        if toggle_trails == True:
##            trails = not trails
##            if trails == True:
##                for body in universe:
##                    body.Body_turtle.pendown()
##                print("Trails enabled")
##            else:
##                for body in universe:
##                    body.Body_turtle.penup()
##                print("Trails disabled")
##            
##            toggle_trails = False

        #if amath.sqrt(body.position[0]**2+body.position[1]**2+body.position[2]**2) > 2000*turtle_SCALE:
        #    universe.remove(body)
        #    print(f"terminated {body.ID} (outside of perimeter)")
        #    continue
    
##    for body in universe:
##        #print(f"{universe[4].position[0]-universe[3].position[0]}\n{universe[4].position[1]-universe[3].position[1]}")
##        if (amath.aabs(body.position[0]) > 2000*turtle_SCALE or amath.aabs(body.position[1]) > 2000*turtle_SCALE):
##            universe.remove(body)
##            print(f"terminated {body.ID} (outside of perimeter)")
##            continue
##        
##        frame.append(dummy(body.ID, body.mass, body.position))
        
## Heading
##        if self.velocity[0] == 0:
##            self.Body_turtle.hideturtle()
##        else:
##            self.Body_turtle.showturtle()
##            angle = degrees(atan(self.velocity[1]/self.velocity[0]))
##            
##            if self.velocity[0] < 0:
##                angle += 180
##            
##            self.Body_turtle.setheading(angle)
        
        #Body("1", "blue", 0.5, 1*m,(1*r,0),(0,1*v)),
        #Body("1", "green", 0.5, 1*m,(-1*r,0),(0,-1*v)),
        #Body("1", "orange", 0.5, 1*m,(1*r,-0.5*r),(0,1*v)),
        #Body("1", "purple", 0.5, 1*m,(-1*r,2*r),(2*v,-3*v)),
        #Body("1", "brown", 0.5, 1*m,(-1.5,-5),(0,-0.04))
