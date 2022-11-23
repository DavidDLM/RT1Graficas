# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso
import struct
import matMath as mt
import numpy as np


class Texture(object):
    def __init__(this, filename):

        with open(filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(18)
            this.width = struct.unpack('=l', image.read(4))[0]
            this.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            this.framebuffer = []

            for y in range(this.height):
                frameRow = []

                for x in range(this.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    frameRow.append([r, g, b])

                this.framebuffer.append(frameRow)

    def getColor(this, u, v):
        if 0 <= u < 1 and 0 <= v < 1:
            return this.framebuffer[int(v * this.height)][int(u * this.width)]
        else:
            return None

    def getEnvColor(this, direction):
        direction = [d / mt.normL2(direction) for d in direction]

        x = int(
            (np.arctan2(direction[2], direction[0]) / (2 * np.pi) + 0.5) * this.width)
        y = int(np.arccos(-direction[1]) / np.pi * this.height)

        return this.framebuffer[y][x]
