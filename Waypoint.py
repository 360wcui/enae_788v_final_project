class Waypoint:
    def __init__(self,x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def __eq__(self, other):
        return abs(self.x - other.x) < 0.5 and abs(self.y - other.y) < 0.5 and abs(self.z - other.z) < 0.5

    def __lt__(self, other):
        if self.x == other.x:
            if self.y == other.y:
                return self.z < other.z
            else:
                return self.y < other.y
        else:
            return self.x < other.x

    def __gt__(self, other):
        if self.x == other.x:
            if self.y == other.y:
                return self.z > other.z
            else:
                return self.y > other.y
        else:
            return self.x > other.x

    def __str__(self):
        return ' x: ' + str(self.x) + ' y: ' + str(self.y) + ' z: ' + str(self.z)
