from particle import Particle


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x  # coordinates of top right corner
        self.y = y
        self.w = w  # dimensions
        self.h = h
        self.points = []


class Quadtree:
    def __init__(self, pLevel: int, pBounds: Rectangle):
        self.bounds: Rectangle = pBounds
        self.capacity = 3
        self.max_level = 10
        self.level: int = pLevel
        self.nodes: list[Quadtree | None] = [None, None, None, None]
        self.objects: list[Particle] = []

    def clear(self):
        self.objects.clear()
        for node in self.nodes:
            if node is not None:
                node.clear()
                node = None

    def split(self):
        sub_width = self.bounds.w
        sub_height = self.bounds.h
        x = self.bounds.x
        y = self.bounds.y

        level = self.level + 1

        self.nodes[0] = Quadtree(level, Rectangle(x, y, sub_width, sub_height))
        self.nodes[1] = Quadtree(level, Rectangle(x + sub_width, y, sub_width, sub_height))
        self.nodes[2] = Quadtree(level, Rectangle(x, y + sub_height, sub_width, sub_height))
        self.nodes[3] = Quadtree(level, Rectangle(x + sub_width, y + sub_height, sub_width, sub_height))

    def get_index(self, p: Particle) -> int:
        horizontal_mid = self.bounds.x + self.bounds.w / 2
        vertical_mid = self.bounds.y + self.bounds.h / 2

        x, y = p.position

        if x < horizontal_mid:
            if y < vertical_mid:
                return 0  # Top-left (NW)
            else:
                return 2  # Bottom-left (SW)
        else:
            if y < vertical_mid:
                return 1  # Top-right (NE)
            else:
                return 3  # Bottom-right (SE)

    def insert(self, point: Particle):
        if self.nodes[0] is not None:
            index = self.get_index(point)
            if index != -1:
                self.objects.append(point)
                return

        self.objects.append(point)

        if len(self.objects) > self.capacity and self.level < self.max_level:
            if self.nodes[0] is None:
                self.split()

            for obj in self.objects:
                index = self.get_index(obj)
                if index != -1:
                    self.nodes[index].insert(obj)

    def retrieve(self, p) -> list[Particle]:
        return_objects = []

        index = self.get_index(p)
        if index != -1 and not (self.nodes[0] is None):
            self.nodes[index].retrieve(p)

        return_objects.extend(self.objects)

        return return_objects
