"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
Enrique Luna 0223929
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from datetime import date

ON = 255
OFF = 0
vals = [ON, OFF]
generations=200
firstFrame = True
inputName = "input.in"
outputName = "output.out" 

#Figures
block = np.array([[0,0,0,0],[0,255,255,0],[0,255,255,0],[0,0,0,0]]) #4x4
beehive = np.array([[0,0,0,0,0,0],[0,0,255,255,0,0],[0,255,0,0,255,0],[0,0,255,255,0,0],[0,0,0,0,0,0]]) #5x6
loaf = np.array([[0,0,0,0,0,0],[0,0,255,255,0,0],[0,255,0,0,255,0],[0,0,255,0,255,0],[0,0,0,255,0,0],[0,0,0,0,0,0]]) #6x6
boat = np.array([[0,0,0,0,0],[0,255,255,0,0],[0,255,0,255,0],[0,0,255,0,0],[0,0,0,0,0]]) #5x5
tub = np.array([[0,0,0,0,0],[0,0,255,0,0],[0,255,0,255,0],[0,0,255,0,0],[0,0,0,0,0]]) #5x5

blinker1 = np.array([[0,0,0],[0,255,0],[0,255,0],[0,255,0],[0,0,0]]) #5x3
blinker2 = np.array([[0,0,0,0,0],[0,255,255,255,0],[0,0,0,0,0]]) #3x5
toad1 = np.array([[0,0,0,0,0,0],[0,0,0,255,0,0],[0,255,0,0,255,0],[0,255,0,0,255,0],[0,0,255,0,0,0],[0,0,0,0,0,0]]) #6x6
toad2 = np.array([[0,0,0,0,0,0],[0,0,255,255,255,0],[0,255,255,255,0,0],[0,0,0,0,0,0]]) #4x6
beacon1 = np.array([[0,0,0,0,0,0],[0,255,255,0,0,0],[0,255,255,0,0,0],[0,0,0,255,255,0],[0,0,0,255,255,0],[0,0,0,0,0,0]]) #6x6
beacon2 = np.array([[0,0,0,0,0,0],[0,255,255,0,0,0],[0,255,0,0,0,0],[0,0,0,0,255,0],[0,0,0,255,255,0],[0,0,0,0,0,0]]) #6x6

glider1 = np.array([[0,0,0,0,0],[0,0,255,0,0],[0,0,0,255,0],[0,255,255,255,0],[0,0,0,0,0]]) #5x5
glider2 = np.array([[0,0,0,0,0],[0,255,0,255,0],[0,0,255,255,0],[0,0,255,0,0],[0,0,0,0,0]]) #5x5
glider3 = np.array([[0,0,0,0,0],[0,0,0,255,0],[0,255,0,255,0],[0,0,255,255,0],[0,0,0,0,0]]) #5x5
glider4 = np.array([[0,0,0,0,0],[0,255,0,0,0],[0,0,255,255,0],[0,255,255,0,0],[0,0,0,0,0]]) #5x5

spaceship1 = np.array([[0,0,0,0,0,0,0],[0,255,0,0,255,0,0],[0,0,0,0,0,255,0],[0,255,0,0,0,255,0],[0,0,255,255,255,255,0],[0,0,0,0,0,0,0]]) #6x7
spaceship2 = np.array([[0,0,0,0,0,0,0],[0,0,0,255,255,0,0],[0,255,255,0,255,255,0],[0,255,255,255,255,0,0],[0,0,255,255,0,0,0],[0,0,0,0,0,0,0]]) #6x7
spaceship3 = np.array([[0,0,0,0,0,0,0],[0,0,255,255,255,255,0],[0,255,0,0,0,255,0],[0,0,0,0,0,255,0],[0,255,0,0,255,0,0],[0,0,0,0,0,0,0]]) #6x7
spaceship4 = np.array([[0,0,0,0,0,0,0],[0,0,255,255,0,0,0],[0,255,255,255,255,0,0],[0,255,255,0,255,255,0],[0,0,0,255,255,0,0],[0,0,0,0,0,0,0]]) #6x7
###

#Check if submatrix deserves to be checked if so checks it and compares each patter if possible
def patterCount(grid,N,M):
    patternCounter = [0,0,0,0,0,0,0,0,0,0]
    for i in range(N+2):
        for j in range(M+2):
            if grid[i][j]==vals[1] and ((i+4<N+2 and j+1<M+2 and sum(grid[i:i+4,j+1])>0) or (i+3<N+2 and j+1<M+2 and sum(grid[i:i+3,j+1])>0)):
                if i+4<=N+2 and j+4<=M+2 and (grid[i:i+4,j:j+4]==block).all():
                    patternCounter[0]+=1
                elif i+5<=N+2 and j+6<=M+2 and (grid[i:i+5,j:j+6]==beehive).all():
                    patternCounter[1]+=1
                elif i+6<=N+2 and j+6<=M+2 and (grid[i:i+6,j:j+6]==loaf).all():
                    patternCounter[2]+=1
                elif i+5<=N+2 and j+5<=M+2 and (grid[i:i+5,j:j+5]==boat).all():
                    patternCounter[3]+=1
                elif i+5<=N+2 and j+5<=M+2 and (grid[i:i+5,j:j+5]==tub).all():
                    patternCounter[4]+=1
                elif i+5<=N+2 and j+3<=M+2 and (grid[i:i+5,j:j+3]==blinker1).all():
                    patternCounter[5]+=1
                elif i+3<=N+2 and j+5<=M+2 and (grid[i:i+3,j:j+5]==blinker2).all():
                    patternCounter[5]+=1
                elif i+6<=N+2 and j+6<=M+2 and (grid[i:i+6,j:j+6]==toad1).all():
                    patternCounter[6]+=1
                elif i+4<=N+2 and j+6<=M+2 and (grid[i:i+4,j:j+6]==toad2).all():
                    patternCounter[6]+=1
                elif i+6<=N+2 and j+6<=M+2 and (grid[i:i+6,j:j+6]==beacon1).all():
                    patternCounter[7]+=1
                elif i+6<=N+2 and j+6<=M+2 and (grid[i:i+6,j:j+6]==beacon2).all():
                    patternCounter[7]+=1
                elif i+5<=N+2 and j+5<=M+2 and (grid[i:i+5,j:j+5]==glider1).all():
                    patternCounter[8]+=1
                elif i+5<=N+2 and j+5<=M+2 and (grid[i:i+5,j:j+5]==glider2).all():
                    patternCounter[8]+=1
                elif i+5<=N+2 and j+5<=M+2 and (grid[i:i+5,j:j+5]==glider3).all():
                    patternCounter[8]+=1
                elif i+5<=N+2 and j+5<=M+2 and (grid[i:i+5,j:j+5]==glider4).all():
                    patternCounter[8]+=1
                elif i+6<=N+2 and j+7<=M+2 and (grid[i:i+6,j:j+7]==spaceship1).all():
                    patternCounter[9]+=1
                elif i+6<=N+2 and j+7<=M+2 and (grid[i:i+6,j:j+7]==spaceship2).all():
                    patternCounter[9]+=1
                elif i+6<=N+2 and j+7<=M+2 and (grid[i:i+6,j:j+7]==spaceship3).all():
                    patternCounter[9]+=1
                elif i+6<=N+2 and j+7<=M+2 and (grid[i:i+6,j:j+7]==spaceship4).all():
                    patternCounter[9]+=1
    return patternCounter

#Writes the results in an output file
def writeOutputFile(iteration,patternCounter):
    total = sum(patternCounter)
    one = False
    if total==0: 
        one=True
        total=1
    outputFile = open(outputName,"a")
    outputFile.write("Iteration: "+str(iteration)+"\n")
    outputFile.write("Block:     "+str(patternCounter[0])+"    Percent: "+str(patternCounter[0]/total*100)+"\n")
    outputFile.write("Beehive:   "+str(patternCounter[1])+"    Percent: "+str(patternCounter[1]/total*100)+"\n")
    outputFile.write("Loaf:      "+str(patternCounter[2])+"    Percent: "+str(patternCounter[2]/total*100)+"\n")
    outputFile.write("Boat:      "+str(patternCounter[3])+"    Percent: "+str(patternCounter[3]/total*100)+"\n")
    outputFile.write("Tub:       "+str(patternCounter[4])+"    Percent: "+str(patternCounter[4]/total*100)+"\n")
    outputFile.write("Blinker:   "+str(patternCounter[5])+"    Percent: "+str(patternCounter[5]/total*100)+"\n")
    outputFile.write("Toad:      "+str(patternCounter[6])+"    Percent: "+str(patternCounter[6]/total*100)+"\n")
    outputFile.write("Beacon:    "+str(patternCounter[7])+"    Percent: "+str(patternCounter[7]/total*100)+"\n")
    outputFile.write("Glider:    "+str(patternCounter[8])+"    Percent: "+str(patternCounter[8]/total*100)+"\n")
    outputFile.write("Spaceship: "+str(patternCounter[9])+"    Percent: "+str(patternCounter[9]/total*100)+"\n")
    outputFile.write("Total:     "+str(0 if one else total)+"\n")
    outputFile.write("\n")
    outputFile.close()

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N, M):
    global firstFrame
    if firstFrame:
        firstFrame=False
        return

    counter = patterCount(grid, N,M) #Call the function to count patterns
    writeOutputFile(frameNum+1,counter) #Write results of iteration in output file

    if frameNum+1==generations:
        return

    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # TODO: Implement the rules of Conway's Game of Life
    for i in range(N+2):
        for j in range(M+2):
            neighbours = 0 
            for k in range(-1,2):
                for l in range(-1,2):
                    if i+k>=0 and i+k<N+2 and j+l>=0 and j+l<M+2:
                        if grid[i+k][j+l]==vals[0]:
                            neighbours+=1
            if grid[i][j]==vals[0]:
                if (neighbours-1)<2 or (neighbours-1)>3:
                    newGrid[i][j] = vals[1]
            elif neighbours==3:
                newGrid[i][j] = vals[0]
    
    # update data
    img.set_data(newGrid[1:N+1,1:M+1])
    grid[:] = newGrid[:]
    print(frameNum+2) #Print frame number
    return img,

#Read an input file and assigns variables
def readInputFile():
    file = open(inputName, "r")
    width, height = map(int,file.readline().split()[:2])
    gens = int(file.readline().split()[0])
    
    grid = np.zeros((width+2)*(height+2)).reshape(width+2, height+2)
    for line in file:
        i,j = map(int,line.split()[:2])
        grid[i+1][j+1]=vals[0]
    file.close()
    return width,height,gens,grid

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments

    #Allows to run program as follow: python conway.py inputName outputName
    if len(sys.argv) == 3:
        global inputName
        global outputName
        inputName = sys.argv[1]
        outputName = sys.argv[2] 
    # set grid size
    #N = 100

    # set animation update interval
    updateInterval = 100

    # declare grid
    #grid = np.array([])
    
    #Call input function and start writing output file
    global generations
    N,M,generations,grid = readInputFile()
    outputFile = open(outputName,"w")
    outputFile.write("Simulation at "+str(date.today())+"\n")
    outputFile.write("Universe size "+str(N)+" x "+str(M)+"\n")
    outputFile.write("\n")
    outputFile.close()
    
    # populate grid with random on/off - more off than on
    #grid = randomGrid(N)
    # Uncomment lines to see the "glider" demo
    #grid = np.zeros(N*N).reshape(N, N)
    #addGlider(1, 1, grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid[1:N+1,1:M+1], interpolation='nearest')
    print(1) #First frame
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, M),
                                  frames = generations,
                                  interval=updateInterval,
                                  save_count=100,
                                  repeat=False)

    plt.show()

# call main
if __name__ == '__main__':
    main()