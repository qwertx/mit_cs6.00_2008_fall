# 6.00 Problem Set 9
#
# Name:
# Collaborators:
# Time:

from string import *

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return float(self.side**2)
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return float(3.14159*(self.radius**2))
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = float(base)
        self.height = float(height)
    def area(self):
        return float(self.base * self.height / 2.0)
    def __str__(self):
        return 'Triangle with base ' + str(self.base) + ' and height ' + str(self.height)
    def __eq__(self, other):
        return type(other) == Triangle and self.base == other.base and self.height == other.height

#
# Problem 1: Create the Triangle class
#
## TO DO: Implement the `Triangle` class, which also extends `Shape`.

#
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

class ShapeSet:
    def __init__(self):
        """
        Initialize any needed variables
        """
        self.shape = []
        self.place = None
    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be
        identical
        sh: shape to be added
        """
        if type(sh) != Triangle and type(sh) != Square and type(sh) != Circle:
            raise TypeError('not a supported shape') 
        for i in range(len(self.shape)):
            if self.shape[i] == sh:
                raise ValueError('same shape')
        self.shape.append(sh)  
    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        self.place = 0
        return self
    def next(self):
        if self.place >= len(self.shape):
            raise StopIteration
        self.place += 1
        return self.shape[self.place - 1].__str__()
    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        for i in range(len(self.shape)):
            print self.shape[i]
        return ''

#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    largest = []
    indx = 0
    for i in range(len(shapes.shape)):
        if shapes.shape[i].area() > shapes.shape[indx].area():
            indx = i
    largest.append(shapes.shape[indx])
    for j in range(len(shapes.shape)):
        if shapes.shape[j].area() == shapes.shape[indx].area() and indx != j:
            largest.append(shapes.shape[j])
    return largest

##ss = ShapeSet()
##ss.addShape(Triangle(3,8))
##ss.addShape(Circle(1))
##ss.addShape(Triangle(4,6))
##largest = findLargest(ss)
##for e in largest: print e

#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    ss = ShapeSet()
    shapefile = open(filename)
    for line in shapefile:
        eachline = line.strip()
        temp = eachline.split(',')
        print temp
        if temp[0] == 'triangle':
            ss.addShape(Triangle(float(temp[-2]),float(temp[-1])))
        elif temp[0] == 'square':
            ss.addShape(Square(float(temp[-1])))
        elif temp[0] == 'circle':
            ss.addShape(Circle(float(temp[-1])))
    return ss
            
