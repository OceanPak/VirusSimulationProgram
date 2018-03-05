# Importing neccessary modules. 

import tkinter # To use Tkinter Window and its properties. 
from tkinter import *
import random # To generate random speeds/slopes for the ball to travel in when
              # it hits the wall. 
import time # To pause the program to let animation to appear.

import matplotlib
matplotlib.use("TkAgg") # Needed to use Matplotlib in the GUI Python Shell.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # We only need to import the Canvas.
from matplotlib import style # For styling the graph.
import matplotlib.pyplot as plt # To perform the actual plotting.
import math

# Define ball properties and functions
class Ball:
    def __init__(self, canvas):
        # Drawing Board
        self.canvas = canvas
        # Creating the particle ball.
        # First 2 (0,10) is left upper corner, last 2 (10,20) is right lower corner.
        # Fill and outline is red so that the ball is colored red.
        self.id = canvas.create_oval(0,10,10,20, fill='red', outline='red') 
        self.canvas.move(self.id, 300, 200) #move ball to starting frame position
        self.yspeed = -1 # Default speed for ball for y-axis. 
        self.xspeed = random.randrange(-3, -1) # slope of the line that the ball
                                               # follows. Basically is the speed

    def draw(self):
        self.canvas.move(self.id, self.xspeed, self.yspeed) #move ball to position
        pos = self.canvas.coords(self.id) #obtain coordinates of ball to update

        # Invisible boundaries that the ball cannot cross. In this case,
        # the outline of the human body.
        
        if pos[1] <= 173: #upper ceiling
            self.yspeed = random.randrange(1,3) #slope/speed of ball
            
        # Arms
        if pos[0] <= 100 and 400 >= pos[1] >= 180: #left wall
            self.xspeed = random.randrange(1,3) #slope/speed of ball
        if pos[2] >= 300 and 400 >= pos[3] >= 180: #right wall
            self.xspeed = random.randrange(-3,-1) #slope/speed of ball

        # Legs
        if pos[0] <= 124 and 550 >= pos[1] >= 396: #left wall
            self.xspeed = random.randrange(1,3) #slope/speed of ball
        if pos[2] >= 275 and 550 >= pos[3] >= 396: #right wall
            self.xspeed = random.randrange(-3,-1) #slope/speed of ball

        # Horizontal Hands
        if 125 >= pos[2] >= 100 and pos[3] >= 398: #lower floor
            self.yspeed = random.randrange(-3,-1) #slope/speed of ball
        if 275 >= pos[2] >= 300 and pos[3] >= 398: #lower floor
            self.yspeed = random.randrange(1,3) #slope/speed of ball

        # Lower Floor
        if pos[3] >= 550: #lower floor
            self.yspeed = random.randrange(-3,-1) #slope/speed of ball

# Create window and canvas to draw on
tk = Tk()
tk.wm_title("Virus Population Simulator") # Gives name to window
# Code below implements text into the Tkinter Window. It uses the Label function. 
text = Label(tk, text="Welcome to our Virus Simulator, made by Bernd Wong and Ocean Pak.")
text.pack(side=TOP)
canvas = Canvas(tk, width=375, height=575, bd=0, highlightthickness=0)
canvas.pack(side=LEFT) # Style the window to the left of the graph
style.use("ggplot") # To make the graph have the nice appeaance. 

f = plt.figure(figsize=(9, 8)) # Plotting the figure size on the canvas.
plt.ion() # Turn on interactive mode for the graph. Allows display on Tkinter Window.
a = f.add_subplot(111) #1 by 1 graph, chart number 1

canv = FigureCanvasTkAgg(f, master=tk) # Create new canvas to draw graph on
                                       # since graph cannot be on same canvas
                                       # as the human body. We use 'f' as the
                                       # figure/graph we want to use, and use
                                       # tk as the master to display on
                                       # Tkinter window.
canv.get_tk_widget().pack(side=LEFT, padx=50) # Essential function to place
                                              # the widget properties in tkinter
                                              # onto the graph. We place the
                                              # alignment for the graph to the
                                              # left, because it will be right
                                              # next to the human body canvas.
                                              # padx is the invisible padding
                                              # so as to artistically seperate
                                              # the two canvas.
canv._tkcanvas.pack(side=LEFT) # Same as code above. Still essential. 

# The set of code below is to draw the head and body for the human.
# First 2 coordinates are for the left upper corner,
# last 2 coordinates are for the right lower corner.
head = canvas.create_oval(125, 10, 275, 160, width=5)
top = canvas.create_line(125, 175, 275, 175, width=5)
# For leftshoulder below, we are using start=90, extent=90 as to rotate the shoulder
# 90 degrees left. This is to make the arc look like a shoulder.
# style=tkinter.ARC is used so that only the arc line will appear, making the
# line look like a shoulder.
leftshoulder = canvas.create_arc(100, 175, 150, 225, start=90, extent=90, width=5, style=tkinter.ARC)
rightshoulder = canvas.create_arc(250, 175, 300, 225, width=5, style=tkinter.ARC)
left = canvas.create_line(100, 200, 100, 400, width=5)
right = canvas.create_line(300, 225, 300, 400, width=5)
lefthand = canvas.create_line(100, 398, 125, 398, width=5)
righthand = canvas.create_line(275, 398, 300, 398, width=5)
leftleg = canvas.create_line(124, 396, 124, 550, width=5)
rightleg = canvas.create_line(275, 396, 275, 550, width=5)
bottom = canvas.create_line(124, 550, 275, 550, width=5)

ball_list = [] # store a list of Particle objects
frameList = [] # counts the number of frames/ticks that have passed.
               # this will be the x axis.
populationList = [] # stores the total viral population for that tick/frame.
                    # this will be the y axis. 
frame = 0 # initializing the frame count.
prevPopulation = 0 # storing the previous population number

plt.axis([0,100,0,100]) # controls the visible axes on the graph
plt.xlabel('Ticks') # Labels x-axis
plt.ylabel('Virus Population Count') # Labels y-axis
plt.title('Virus Population Simulator') # Labels graph

try:
    # Animation loop
    while True:
        if frame%10==0:
            particle = Ball(canvas) #creates object Ball
            ball_list.append(particle) #add created object into list of objects
        frame = frame+1 #only for testing purposes only
        frameList.append(int(frame)) #save the current tick/frame
                                     #to be used in x-axis.
        populationList.append(len(ball_list)) #save the current virus particle
                                              #population to be used as the
                                              #y-axis. 

        # animate each ball in the list of balls
        for particle in ball_list: #updating each object in the list
            particle.draw() #find position of object
            plt.plot(frameList, populationList, color='red') #plots updating line
            tk.update() #update position of object
            time.sleep(0.05) #allow animation to appear
except: #for the error that appears upon closing the tab
    pass
