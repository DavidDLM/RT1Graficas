# Raytracing
# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso


import numpy as np
from intersect import Intersect
import matMath as mt

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Sphere(object):
    def __init__(this, center, radius, material):
        this.center = center
        this.radius = radius
        this.material = material

    def ray_intersect(this, origin, direction):
        L = mt.subtractVectors(this.center, origin)
        tca = mt.dotMatrix(L, direction)
        d = (mt.normL2(L) ** 2 - tca ** 2) ** 0.5

        if isinstance(d, complex):
            d = d.real

        if d > this.radius:
            return None

        thc = (this.radius ** 2 - d ** 2) ** 0.5

        if isinstance(thc, complex):
            thc = thc.real

        t0 = tca - thc
        t1 = tca + thc

        if isinstance(t0, complex):
            t0 = t0.real

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # P = O + t0 * D
        newt0 = [t0 * d for d in direction]
        P = mt.addVectors(origin, newt0)
        normal = mt.subtractVectors(P, this.center)
        normal = [n / mt.normL2(normal) for n in normal]

        u = 1 - ((np.arctan2(normal[2], normal[0]) / (2 * np.pi)) + 0.5)
        v = np.arccos(-1 * normal[1]) / np.pi

        uv = (u, v)
        return Intersect(distance=t0,
                         point=P,
                         normal=normal,
                         texcoords=uv,
                         sceneObj=this)
