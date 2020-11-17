from math import cos, sin, pi

from struct import pack


class Bitmap:
    def __init__(self, width, height):
        self.type = 19778  # Bitmap signature
        self.reserved1 = 0
        self.reserved2 = 0
        self.planes = 1
        self.c_size = 12
        self.bit_count = 24
        self.off_bits = 26
        self.Width = width
        self.Height = height
        self.f_size = 26 + self.Width * 3 * self.Height
        self.clear()

    def clear(self):
        self.graphics = [(0, 0, 0)] * self.Width * self.Height

    def set_pixel(self, x, y, color):
        if isinstance(color, tuple):
            if x < 0 or y < 0 or x > self.Width - 1 or y > self.Height - 1:
                raise ValueError('Coords out of range')
            if len(color) != 3:
                raise ValueError('Color must be a tuple of 3 elements')
            self.graphics[y * self.Width + x] = (color[2], color[1], color[0])
        else:
            raise ValueError('Color must be a tuple of 3 elements')

    def write(self, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                         self.type,
                         self.f_size,
                         self.reserved1,
                         self.reserved2,
                         self.off_bits))  # Writing BITMAP FILE HEADER
            f.write(pack('<LHHHH',
                         self.c_size,
                         self.Width,
                         self.Height,
                         self.planes,
                         self.bit_count))  # Writing BITMAP INFO
            for px in self.graphics:
                f.write(pack('<BBB', *px))
            for i in range((4 - ((self.Width * 3) % 4)) % 4):
                f.write(pack('B', 0))


t = 0
all_pixels = []
pixel = []
step = 0.04
while t <= 4 * pi:
    x = round(13 * (cos(t) - cos(6.5 * t) / 6.5), 2)
    y = round(13 * (sin(t) - sin(6.5 * t) / 6.5), 2)
    pixel.append(x)
    pixel.append(y)
    all_pixels.append(tuple(pixel))
    pixel.clear()
    t += 0.001


def main():
    side = 800
    b = Bitmap(side, side)
    for i in range(0, side):
        for j in range(0, side):
            b.set_pixel(i, j, (255, 255, 255))

    offset2 = -15.5
    for y_locate in range(side):
        offset1 = -15.5
        for x_locate in range(side):
            if (offset1, offset2) in all_pixels:
                b.set_pixel(x_locate, y_locate, (0, 0, 0))
            else:
                b.set_pixel(x_locate, y_locate, (255, 255, 255))
            offset1 = round(offset1 + step, 3)
        offset2 = round(offset2 + step, 3)

    b.write('2nd_result.bmp')


if __name__ == '__main__':
    main()
