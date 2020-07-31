# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
from pylab import *
import random
import ps11_visualize
# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height, cleaned = {}):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleaned = {}
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        m = int(pos.getX())
        n = int(pos.getY())
        self.cleaned[(m, n)] = 'c'
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        flag = False
        if (m, n) in self.cleaned:
            flag = True
        return flag
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned)
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        return Position(x, y)
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        if (0 <= x <= self.width) and (0 <= y <= self.height):
            return True
        else:
            return False
            
class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.d = random.randint(0, 359)
        self.p = self.room.getRandomPosition()
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.p
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.p.x = position.x
        self.p.y = position.y
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        startpos = self.getRobotPosition()
        self.room.cleanTileAtPosition(startpos)
        for i in range(int(self.speed)):
            while True:
                temppos = startpos.getNewPosition(self.d, 1)
                if not self.room.isPositionInRoom(temppos):
                    self.d = random.randint(0, 359)
                else:break
            midway = startpos.getNewPosition(self.d, 1)
            self.setRobotPosition(midway)
            self.room.cleanTileAtPosition(midway)
        return self.room.cleaned
            
# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    res = []
    def givename(num_robots, robot_type, room, speed):
        robotls = []
        for i in range(num_robots):
            robotls.append(robot_type(room, speed))
        return robotls
        
    def Onemove(robotls):
        cleaned = {}
        for i in range(len(robotls)):
            x = robotls[i].updatePositionAndClean()
            cleaned.update(x)
        return cleaned

    rooms = []
    for i in range(num_trials):
        rooms.append(RectangularRoom(width, height))
    for i in range(num_trials):
##        anim = ps11_visualize.RobotVisualization(num_robots, width, height)
        covered = 0
        time = 0
        cleaned = {}
        room = rooms[i]
        tempcover = []
        robotls = givename(num_robots, robot_type, room, speed)
        while covered < min_coverage:
            cleaned.update(Onemove(robotls))
##            anim.update(room, robotls)
            time += 1
            covered = float(len(cleaned)) / room.getNumTiles()
            tempcover.append(covered * 100)
        res.append(tempcover)
##        anim.done()
    return res
            
                       
# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4
def helper(reslist):
    tot = 0
    for i in range(len(reslist)):
        tot += len(reslist[i])
    aver = tot / len(reslist)
    return aver
        

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    size5 = runSimulation(1, 1.0, 5, 5, 0.75, 30, Robot, False)
    size10 = runSimulation(1, 1.0, 10, 10, 0.75, 30, Robot, False)
    size15 = runSimulation(1, 1.0, 15, 15, 0.75, 30, Robot, False)
    size20 = runSimulation(1, 1.0, 20, 20, 0.75, 30, Robot, False)
    size25 = runSimulation(1, 1.0, 25, 25, 0.75, 30, Robot, False)
    aver5 = helper(size5)
    aver10 = helper(size10)
    aver15 = helper(size15)
    aver20 = helper(size20)
    aver25 = helper(size25)
    figure()
    plot([25,100,225,400,625], [aver5, aver10, aver15, aver20, aver25])
    title('A single robot cleans 75% of the room')
    xlabel('Room size')
    ylabel('Average time')
    show()
    

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    time =[]
    for i in range(1,11):
        templs = runSimulation(i, 1.0, 25, 25, 0.75, 30, Robot, False)
        aver = helper(templs)
        time.append(aver)
    figure()
    plot([1,2,3,4,5,6,7,8,9,10], time)
    title('1-10 robot(s) clean 75% of the room')
    xlabel('Robot number')
    ylabel('Average time')
    show()
    
def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    ratio1 = runSimulation(2, 1.0, 20, 20, 0.75, 30, Robot, False)
    ratio2 = runSimulation(2, 1.0, 25, 16, 0.75, 30, Robot, False)
    ratio3 = runSimulation(2, 1.0, 40, 10, 0.75, 30, Robot, False)
    ratio4 = runSimulation(2, 1.0, 50, 8, 0.75, 30, Robot, False)
    ratio5 = runSimulation(2, 1.0, 100, 4, 0.75, 30, Robot, False)
    aver1 = helper(ratio1)
    aver2 = helper(ratio2)
    aver3 = helper(ratio3)
    aver4 = helper(ratio4)
    aver5 = helper(ratio5)
    figure()
    plot([1,1.25,4,6.25,25], [aver1, aver2, aver3, aver4, aver5])
    axis([0, 30, 0, aver5 + 50])
    title('Two robots clean 75% of the room')
    xlabel('Ratio of room width to height')
    ylabel('Average time')
    show()

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    res1 = runSimulation(1, 1.0, 25, 25, 1, 30, Robot, False)
    res2 = runSimulation(2, 1.0, 25, 25, 1, 30, Robot, False)
    res3 = runSimulation(3, 1.0, 25, 25, 1, 30, Robot, False)
    res4 = runSimulation(4, 1.0, 25, 25, 1, 30, Robot, False)
    res5 = runSimulation(5, 1.0, 25, 25, 1, 30, Robot, False)
    mean1 = computeMeans(res1)
    mean2 = computeMeans(res2)
    mean3 = computeMeans(res3)
    mean4 = computeMeans(res4)
    mean5 = computeMeans(res5)
    figure()
    y1 = arange(1, len(mean1)+1)
    y2 = arange(1, len(mean2)+1)
    y3 = arange(1, len(mean3)+1)
    y4 = arange(1, len(mean4)+1)
    y5 = arange(1, len(mean5)+1)
    x1 = array(mean1)
    x2 = array(mean2)
    x3 = array(mean3)
    x4 = array(mean4)
    x5 = array(mean5)
    plot(x1, y1)
    plot(x2, y2)
    plot(x3, y3)
    plot(x4, y4)
    plot(x5, y5)
    title('Time to clean a 25*25 room with 1-5 robot(s)')
    xlabel('Cleaned percentage of the room')
    ylabel('Average time')
    show()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        startpos = self.getRobotPosition()
        self.room.cleanTileAtPosition(startpos)
        # the only change from ordinary robot
        self.d = random.randint(0, 359)
        for i in range(int(self.speed)):
            while True:
                temppos = startpos.getNewPosition(self.d, 1)
                if not self.room.isPositionInRoom(temppos):
                    self.d = random.randint(0, 359)
                else:break
            midway = startpos.getNewPosition(self.d, 1)
            self.setRobotPosition(midway)
            self.room.cleanTileAtPosition(midway)
        return self.room.cleaned


# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    res1 = runSimulation(1, 1.0, 20, 20, 1, 30, Robot, False)
    res2 = runSimulation(1, 1.0, 20, 20, 1, 30, RandomWalkRobot, False)
    mean1 = computeMeans(res1)
    mean2 = computeMeans(res2)
    figure()
    y1 = arange(1, len(mean1)+1)
    x1 = array(mean1)
    title('Ordinary Robot')
    xlabel('Cleaned percentage of the room')
    ylabel('Average time')
    plot(x1, y1)
    figure()
    y2 = arange(1, len(mean2)+1)
    x2 = array(mean2)
    title('Random walk Robot')
    xlabel('Cleaned percentage of the room')
    ylabel('Average time')
    plot(x2, y2)
    show()
    # Apparently, random walk robot has much lower effiency compared to ordinary robot.
