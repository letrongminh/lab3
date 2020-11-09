from math import cos, sin, pi


from struct import pack


class Bitmap():
    def __init__(s, width, height):
        s._bfType = 19778  # Bitmap signature
        s._bfReserved1 = 0
        s._bfReserved2 = 0
        s._bcPlanes = 1
        s._bcSize = 12
        s._bcBitCount = 24
        s._bfOffBits = 26
        s._bcWidth = width
        s._bcHeight = height
        s._bfSize = 26 + s._bcWidth * 3 * s._bcHeight
        s.clear()

    def clear(s):
        s._graphics = [(0, 0, 0)] * s._bcWidth * s._bcHeight

    def setPixel(s, x, y, color):
        if isinstance(color, tuple):
            if x < 0 or y < 0 or x > s._bcWidth - 1 or y > s._bcHeight - 1:
                raise ValueError('Coords out of range')
            if len(color) != 3:
                raise ValueError('Color must be a tuple of 3 elems')
            s._graphics[y * s._bcWidth + x] = (color[2], color[1], color[0])
        else:
            raise ValueError('Color must be a tuple of 3 elems')

    def write(s, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                         s._bfType,
                         s._bfSize,
                         s._bfReserved1,
                         s._bfReserved2,
                         s._bfOffBits))  # Writing BITMAPFILEHEADER
            f.write(pack('<LHHHH',
                         s._bcSize,
                         s._bcWidth,
                         s._bcHeight,
                         s._bcPlanes,
                         s._bcBitCount))  # Writing BITMAPINFO
            for px in s._graphics:
                f.write(pack('<BBB', *px))
            for i in range((4 - ((s._bcWidth * 3) % 4)) % 4):
                f.write(pack('B', 0))

t = 0
all_pixels = []
pixel = []
while t <= 4 * pi:
    x = round(13*(cos(t) - cos(6.5*t)/6.5), 2)
    y = round(13*(sin(t) - sin(6.5*t)/6.5), 2)
    pixel.append(x)
    pixel.append(y)
    all_pixels.append(tuple(pixel))
    pixel.clear()
    t += 0.01


def main():

    side = 600
    b = Bitmap(side, side)
    for i in range(0, side):
        for j in range(0, side):
            b.setPixel(i, j, (255, 255, 255))


    offset2 = 0
    for y_locate in range(side):
        offset1 = 0
        for x_locate in range(side):
            if (offset1, offset2) in all_pixels:
                b.setPixel(x_locate, y_locate, (0, 0, 0))
            else:
                b.setPixel(x_locate, y_locate, (255, 255, 255))
            offset1 = round(offset1 + 0.01, 2)
        offset2 = round(offset2 + 0.01, 2)

    b.write('file.bmp')


if __name__ == '__main__':
    main()
