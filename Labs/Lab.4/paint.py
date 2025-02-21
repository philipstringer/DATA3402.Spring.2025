#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        if 0 <= row < len(self.data) and 0 <= col < len(self.data[0]):
            self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' ' for _ in range(self.width)] for _ in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            

    def line(self, x1, y1, x2, y2, char='*'):
        x1, y1 = max(0, min(x1, self.width - 1)), max(0, min(y1, self.height - 1))
        x2, y2 = max(0, min(x2, self.width - 1)), max(0, min(y2, self.height - 1))

        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.set_pixel(y1, x1, char)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))
        
class shape:

    def area(self):
        raise NotImplementedError("Subclasses must implement this method")

    def circumfrence(self):
        raise NotImplementedError("Subclasses must implement this method")

    def perimeter(self):
        raise NotImplementedError("Subclasses must implement this method")

    def display(self):
        raise NotImplementedError("Subclasses must implement this method")

    def parameters(self):
        raise NotImplementedError("Subclasses must implement this method")

    def inside_object(self):
        raise NotImplementedError("Subclasses must implement this method")

    def overlap(self):
        raise NotImplementedError("Subclasses must implement this method")

class rectangle(shape):
    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y
        
    def __repr__(self):
        return f"rectangle({repr(self._rectangle__x)}, {repr(self._rectangle__y)}, {repr(self._rectangle__width)}, {repr(self._rectangle__length)})"


    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def display(self):
        print(f"Rectangle: length={self.__length}, width={self.__width}, corner=({self.__x}, {self.__y})")

    def parameters(self):
        points = []
        for i in range(16):
            if i < 4:
                x = self.__x + (i / 4) * self.__length
                y = self.__y
            elif i < 8:
                x = self.__x + self.__length
                y = self.__y + ((i - 4) / 4) * self.__width
            elif i < 12:
                x = self.__x + (12 - i) / 4 * self.__length
                y = self.__y + self.__width
            else:
                x = self.__x
                y = self.__y + (16 - i) / 4 * self.__width
            points.append((x, y))
        return points

    def inside_object(self, x, y):
        return self.__x <= x <= (self.__x + self.__length) and self.__y <= y <= (self.__y + self.__width)

    def overlap(self, other):
        if isinstance(other, rectangle):
            return not (self.__x + self.__length < other.__x or
                       other.__x + other.__length < self.__x or
                       self.__y + self.__width < other.__y or
                       other.__y + other.__width < self.__y)
        elif isinstance(other, circle):
            distance_x = abs(other._circle__x - (self.__x + self.__length / 2))
            distance_y = abs(other._circle__y - (self.__y + self.__width / 2))
            if distance_x > (self.__length / 2 + other._circle__radius):
                return False
            if distance_y > (self.__width / 2 + other._circle__radius):
                return False
            return True
        elif isinstance(other, triangle):
            return (self.inside_object(other._triangle__x, other._triangle__y) or
        self.inside_object(other._triangle__x + other._triangle__a, other._triangle__y) or
        self.inside_object(other._triangle__x + other._triangle__a / 2, other._triangle__y + other._triangle__b))
        return False


class circle(shape):
    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y
        
    def __repr__(self):
        return f"circle({repr(self._circle__x)}, {repr(self._circle__y)}, {repr(self._circle__radius)})"

    def area(self):
        return 3.14 * self.__radius ** 2

    def circumfrence(self):
        return 2 * 3.14 * self.__radius

    def display(self):
        print(f"Circle: Radius={self.__radius}, center = (x={self.__x}, y={self.__y}).")

    def parameters(self):
        points = []
        for i in range(16):
            angle = (i / 16) * (2 * 3.14)
            x = round(self.__x + self.__radius * (3.14 ** 0.5) * (angle),2)
            y = round(self.__y + self.__radius * (3.14 ** 0.5) * (angle),2)
            points.append((x, y))
        return points

    def inside_object(self, x, y):
        return ((x-self.__x) ** 2 + (y- self.__y) ** 2) <= (self.__radius ** 2)

    def overlap(self, other):
        if isinstance(other, circle):
            return (self.__x - other.__x) ** 2 + (self.__y - other.__y) ** 2 <= (self.__radius + other.__radius) ** 2
        if isinstance(other, rectangle):
            return other.overlap(self)
        if isinstance(other, triangle):
            return other.overlap(self)

class triangle(shape):
    def __init__(self, side1, side2, side3, x, y):
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3
        self.__x = x
        self.__y = y
        
    def __repr__(self):
        return f"triangle({repr(self._triangle__x)}, {repr(self._triangle__y)}, {repr(self._triangle__side1)},{repr(self._triangle__side2)}, {repr(self._triangle__side3)})"

    def area(self):
        s = (self.__side1 + self.__side2 + self.__side3) / 2
        return (s * (s - self.__side1) * (s - self.__side2) * (s - self.__side3))

    def perimeter(self):
        return self.__side1 + self.__side2 + self.__side3

    def display(self):
        print(f"Triangle: Side1 = {self.__side1}, side2 = {self.__side2}, side3 = {self.__side3}, corner = (x = {self.__x}, y = {self.__y})")

    def parameters(self):
        points = []
        for i in range(16):
            if i < 5:
                x = round(self.__x + (i / 4) * self.__side1,2)
                y = self.__y
            elif i < 10:
                x = round((self.__x + self.__side1) - (i - 4) / 5 * (self.__side1 / 2),2)
                y = round(self.__y + ((i - 4) / 5) * self.__side2,2)

            else:
                x = round(self.__x + ((10 - i) / 5) * (self.__side1 / 2),2)
                y = round(self.__y + (5 / 5) * self.__side2,2)
            points.append((x, y))
        return points

    def inside_object(self, x, y):
        def area(self):
            s = (self.__side1 + self.__side2 + self.__side3) / 2
            return (s * (s - self.__side1) * (s - self.__side2) * (s - self.__side3)) ** 0.5
        A = area(self.__x, self.__y, self.__x + self.__side1, self.__y, self.__x + self.__side1 / 2, self.__y + self.__side2)
        A1 = area(x, y, self.__x, self.__y, self.__x + self.__side1, self.__y)
        A2 = area(x, y, self.__x + self.__side1, self.__y, self.__x + self.__side1 / 2, self.__y + self.__side2)
        A3 = area(x, y, self.__x + self.__side1 / 2, self.__y + self.__side2, self.__x, self.__y)
        return A == A1 + A2 + A3

    def overlap(self, other):
        if isinstance(other, triangle):
            return (self.inside_object(other._triangle__x, other._triangle__y) or
                    self.inside_object(other._triangle__x + other._triangle__a, other._triangle__y) or
                    self.inside_object(other._triangle__x + other._triangle__a / 2, other._triangle__y + other._triangle__b))
        if isinstance(other, circle):
            return other.overlap(self)
        if isinstance(other, rectangle):
            return other.overlap(self)
        
class compoundShape(shape):
    class CompoundShape(shape):
        def __init__(self, shapes):
            self.shapes = shapes

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)


# In[3]:




