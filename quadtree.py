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
        self.capacity = 5
        self.max_level = 10
        self.level: int = pLevel
        self.nodes: list[Quadtree | None] = [None] * 4
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

    def get_index(self, circle):
        """Determine which quadrant a circle belongs to."""
        vertical_mid = self.bounds.x + self.bounds.w / 2
        horizontal_mid = self.bounds.y + self.bounds.h / 2

        # Circle's center position and radius
        cx, cy, radius = circle.position[0], circle.position[1], circle.radius

        # Determine the bounds of the circle
        left = cx - radius
        right = cx + radius
        top = cy - radius
        bottom = cy + radius

        # Check if circle is in top quadrants
        top_quadrant = bottom <= horizontal_mid
        # Check if circle is in bottom quadrants
        bottom_quadrant = top > horizontal_mid

        # Check if circle is in left quadrants
        if right <= vertical_mid:
            if top_quadrant:
                return 0  # Top-Left
            elif bottom_quadrant:
                return 2  # Bottom-Left
        # Check if circle is in right quadrants
        elif left > vertical_mid:
            if top_quadrant:
                return 1  # Top-Right
            elif bottom_quadrant:
                return 3  # Bottom-Right

        return -1

    def insert(self, point: Particle):
        if self.nodes[0] is not None:
            index = self.get_index(point)
            if index != -1:
                self.nodes[index].insert(point)
                return

        self.objects.append(point)
        if len(self.objects) >= self.capacity and self.level < self.max_level:
            if self.nodes[0] is None:
                self.split()

            for i, obj in enumerate(self.objects):
                index = self.get_index(obj)
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))

    def retrieve(self, r: [], p: Particle) -> list[Particle]:

        index = self.get_index(p)
        if index != -1 and self.nodes[0] is not None:
            self.nodes[index].retrieve(r, p)

        r.extend(self.objects)
        return r
