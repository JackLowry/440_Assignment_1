from math import sqrt
import heapq

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return other.x - self.x + other.y - self.y > 0

    def __str__(self):
        return f"({self.x}, {self.y})"

    def dist(self, o):
        return sqrt((self.x-o.x)**2 + (self.y-o.y)**2)

class FastFringe():
    def __init__(self):
        self.queue = []

    def insert(self, point, f_val):
        heapq.heappush(self.queue, (f_val, point))
    
    def remove(self, point):
        for i in range(len(self.queue)):
            if self.queue[i][1] == point:
                return self.queue.pop(i)
        raise ValueError("Cannot find item to remove from fringe")

    def is_empty(self):
        return len(self.queue) == 0

    def pop(self):
        val = heapq.heappop(self.queue)
        return (val[1], val[0])

    def __contains__(self, o):
        for v in self.queue:
            if o == v[1]:
                return True
        return False
class Fringe():
    
    def __init__(self):
        self.queue = []

    def insert(self, point, f_val):
        for i in range(len(self.queue)):
            if self.queue[i][1] > f_val:
                self.queue.insert(i, (point, f_val))
                return
        self.queue.append((point, f_val))
    
    def remove(self, point):
        for i in range(len(self.queue)):
            if self.queue[i][0] == point:
                return self.queue.pop(i)
        raise ValueError("Cannot find item to remove from fringe")

    def is_empty(self):
        return len(self.queue) == 0

    def pop(self):
        return self.queue.pop(0)

    def __contains__(self, o):
        for v in self.queue:
            if o == v[0]:
                return True
        return False