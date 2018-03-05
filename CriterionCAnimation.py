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

input("Hello would you like to simulate yourself dying? ")
vNum=int(input("Please input an integer for the initial virus population "))
maxPop=int(input("Please the maximum virus population "))
clearProb=float(input("Please input the clearance chance as a decimal between 0-1 "))
maxBirth= float(input("Please input the maximum birth probability as a decimal between 0-1 "))
ticks=int(input("Number of days run "))
viruses=[]

#vNum=int(100)
#maxPop=int(1000)
#clearProb=float(0.5) #The lower the probability, the higher the clearance chance.
#maxBirth=float(0.1) #The lower, the lower the birth rate.
resistances={"Guttagonal":True}
mutProb=0.1
#ticks=int(150)
viruses=[]
prescription=["Guttagonal"]

# Create window and canvas to draw on
tk = Tk()
tk.wm_title("Virus Population Simulator") # Gives name to window
# Code below implements text into the Tkinter Window. It uses the Label function. 
text = Label(tk, text="Welcome to our Virus Simulator, made by Bernd Wong and Ocean Pak.")
text.pack(side=TOP) # Putting the text at the very top of the window.
text2 = Label(tk, text="Each particle displayed represents 10 particles in the real-life simulation. Please refer to the population count for that tick in the live-updating graph to the right.")
text2.pack(side=TOP)
text3 = Label(tk, text="Population Count:")
text3.pack(side=TOP)
listBox = Listbox(tk) # Create a listbox, as to contain all the population count into a scrollable list for the user.
listBox.pack(side=RIGHT, padx=50) # Providing paddings so that the box won't be aligned to the side of the window. 
canvas = Canvas(tk, width=375, height=575, bd=0, highlightthickness=0) # Style the tkinter window to specific measurements. 
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

plt.axis([0,10,0,1000]) # controls the visible axes on the graph
plt.xlabel('Ticks') # Labels x-axis
plt.ylabel('Virus Population Count') # Labels y-axis
plt.title('Virus Population Simulator') # Labels graph

"""
Initial virus population → How many viruses at the beginning of the program. (how many to be instances of the virus class)
Maximum virus population → Maximum amount. After which no more viruses should be produced.
Clearance Probability→ Chance for each single virus to be cleared.
Maximum birth probability → Chance for each single virus to reproduce
Ticks→ Time variable.
"""

class SimpleVirus(object):
    """
    The simple virus class defines the characteristics of a simple virus class.
    It takes into account the maximum birth and clear/death probabilities of the virus.
    """
    def __init__(self,maxBirth,clearProb):
        """
        Initialises the classes with parameters maximum birth probability, clearance probability
        Let the Variables be attached to the instance (self.=)
        """
        self.maxbirthProb=maxBirth
        self.maxclearProb=clearProb

    def getBirth(self):
        return self.maxbirthProb
    def getClear(self):
        return self.maxclearProb

    def doesClear(self):
        """
        This edited method generates a random probability.
        If the probability was >than the clearance probability, it clears. Otherwise it stays.
        """
        genChance=random.random()
        if genChance > self.maxclearProb:
            return True
        else:
            return False

class ResistantViruses(SimpleVirus):
    """
    The resistant virus class is a subclass of the simpleVirus class. This deals with resistance to drugs and
    mutation probabilities. It is a representation of a virus having drug resistance
    """
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        SimpleVirus.__init__(self,maxBirth,clearProb)
        self.maxbirthProb=maxBirthProb
        self.maxclearProb=clearProb
        self.resistances=resistances
        self.mutProb=mutProb

    def getResistances(self,drug): #This checks whether or not the virus is resistant to the drug
        return dict.get(self.resistances,drug)

    def Reproduce(self,popDensity,maxPop,activeDrugs):
        repProb=self.maxbirthProb *(1-popDensity)
        resinherit=1-self.mutProb
        inheritChance=random.random()
        bbDict={}
        bbList=[]
        for drug in activeDrugs:
            if self.getResistances(drug)==False:
                return ["No Child Exception"]

        for numDrug in range (0,len(activeDrugs)):
            if inheritChance>resinherit: #90%
                #90% keep chance, 10% get new. This means that they keep current resistances but drop everything else.
                bbDict[activeDrugs[numDrug]]=True

            elif inheritChance<resinherit:
                #90% don't get, 10% lose. This means that they drop current resistances but get everything else.
                bbDict[activeDrugs[numDrug]]=False

        numNew=math.floor(repProb*maxPop)
        if numNew!=0:
            for bbVirus in range (0,numNew):
                #Creating baby viruses with same variables as parents
                newVir=ResistantViruses(self.getBirth(),self.getClear(),bbDict,self.mutProb)
                bbList.append(newVir)
        return bbList

class SimplePatient(object):
    """
    Patient class uses the virus classes data to either remove, keep or reproduce viruses.
    """
    def __init__ (self,name, maxPop, viruses,drugsList):
        self.name=name
        self.maxPop=maxPop
        self.viruses=viruses
        self.prescription=drugsList

    def getTotalPop(self):
        #getTotalPop is supposed to calculate the total virus population
        return len(self.viruses)

    def getPrescription(self):
        return self.prescription

    def addPrescription(self,newDrug):
        if newDrug in self.prescription:
            self.prescription=self.prescription
        else:
            self.prescription.append(newDrug)

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.
        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])
        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

    def update(self):
        for virus in range(0,len(self.viruses)):
            if self.viruses[virus].doesClear() == True:
                self.viruses.remove(viruses[virus])
                self.viruses.insert(virus,"remove") #To not mess up the positional count,
                # I replace the removed viruses with the name remove
        for i in range (0,self.viruses.count("remove")):
            #Then I remove all the "removes".
            self.viruses.remove("remove")

        for remainvirus in range(0,len(self.viruses)):
            """
            self.getTotalPop calls the function that gets the current amount of viruses after some of them have been cleared.
            Population Density of the Viruses as a Float
            """
            popDensity=(self.getTotalPop())/self.maxPop
            bbList=self.viruses[remainvirus].Reproduce(popDensity,self.maxPop,self.getPrescription())
            for virus in bbList:
                viruses.append(virus)
            for i in range (0,self.viruses.count("No Child Exception")):
                self.viruses.remove("No Child Exception")
        return "Maximum Virus Population Reached"

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

def StartoffBBY():
    """
    This is the function that takes in all the variables and starts the program. It uses the vNum or initial virus population to create the number of instances.
    """
    for virusNumber in range (0,vNum):
        newvirus=ResistantViruses(maxBirth,clearProb,resistances,mutProb)
        viruses.append(newvirus)

bob=SimplePatient("bob",maxPop,viruses,prescription)
def UpdateTotal():
    bob.update()
    return len(bob.viruses)

StartoffBBY()

try:
    for frame in range (0, ticks): # Updating the particles and graph in each frame. 
        populationVirus = UpdateTotal() # Obtaining the virus count from UpdateTotal() function.
        currentPopulation = int(math.floor(populationVirus/10.0)) # Since each particle represents 10 particles, we have to round down the current population count, and find the number of particles we need to generate. 
        if currentPopulation<prevPopulation: # This function is implemented to check whether the program should delete the number of particles from the previous frame. Otherwise, when the virus particles die out, the animation won't update accordingly. 
            difference = prevPopulation-currentPopulation # Find numerical difference in particle count.
            for j in range (0, difference):
                del ball_list[-1] # Deleting the actual ball object. Must be done before the for-loop below, that updates each object in ball_list. 
        if currentPopulation == 0: # If all the virus dies out, we need to delete ALL the particles. The previous if-statement will not do this.
            ball_list=[] # Clearing the list.
        for i in range (0, currentPopulation): # For the number of particles we need to generate, we run the loop that many times.
            particle = Ball(canvas) # Creates object Ball.
            ball_list.append(particle) # Adds created object into list of objects.
        frameList.append(int(frame)) # Save the current tick/frame to be used in the x-axis.
        populationList.append(populationVirus) # Saves the current virus particle popoulation to be used as the y-axis.
        for particle in ball_list: # Updating the position of the particles and graph individually in this for loop. This is the loop mentiond above. 
            particle.draw() # Finds position of object and updates according to the Draw Function.
            plt.plot(frameList, populationList, color='red') # Plots the updated line.
            tk.update() # Updates the position of the ball object.
            time.sleep(0.05) # Allow animation to appear.
        prevPopulation = currentPopulation # Update the previous population to act as a comparison for the next frame.
        listBox.insert(END, str(populationVirus)) # Putting the populationVirus value into the end of the Listbox. This is to display the population count.
except: # We use a try-except loop here because an error will appear upon closing the tab. Using this loop will give a more professional effect.
    pass
