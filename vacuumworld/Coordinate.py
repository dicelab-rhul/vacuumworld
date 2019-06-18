

class Coordinate(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def getX(self):  # i is o for getting x value and i is 1 for getting y value.
        return self.x
    
    def getY(self):  # i is o for getting x value and i is 1 for getting y value.
        return self.y
    
    def __add__(self,c):
        return Coordinate(self.x + c[0], self.y + c[1])

    def __sub__(self,c):
        return Coordinate(self.x - c[0], self.y - c[1])

    def __eq__(self,c): #compares two coords
        return len(self) == len(c) and self.x == c.x and self.y == c.y
    
    def __len__(self):
        return 2 # Always have two coorincates
    
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    def __unicode__(self):
        return self.__str__()
    
    def __repr__(self):
        return self.__str__()

    def t(self): #return a tuple representation.
        return (self.x,self.y)  