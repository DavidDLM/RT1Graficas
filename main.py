from gl import Raytracer, V3
import math
import conversions as conv
import struct
from intersect import *
from lights import *
from material import *
from sphere import *
from collections import namedtuple
import matMath as mt
from textures import *
from obj import *
from math import cos, sin, tan, pi


width = 1024
height = 768

# Materiales a usar
eyes = Material(diffuse=(0, 0, 0))
snow = Material(diffuse=(1, 1, 1))
button = Material(diffuse=(0, 0, 0))
carrot = Material(diffuse=(1, 0.64, 0))

rtc = Raytracer(width, height)

# Luces
rtc.lights.append(AmbientLight(intensity=0.3))
rtc.lights.append(DirectionalLight(direction=(0, 0, -1), intensity=0.3))
rtc.lights.append(DirectionalLight(direction=(0, 0, -5), intensity=0.3))

# Head
rtc.scene.append(Sphere(center=(0, 3, -10), radius=1, material=snow))
rtc.scene.append(Sphere(center=(0.2, 3, -9), radius=0.1, material=eyes))
rtc.scene.append(Sphere(center=(-0.2, 3, -9), radius=0.1, material=eyes))

# Smile
rtc.scene.append(Sphere(center=(-0.6, 2.7, -9), radius=0.1, material=eyes))
rtc.scene.append(Sphere(center=(0.6, 2.7, -9), radius=0.1, material=eyes))
rtc.scene.append(Sphere(center=(-0.3, 2.5, -9), radius=0.1, material=eyes))
rtc.scene.append(Sphere(center=(0.3, 2.5, -9), radius=0.1, material=eyes))

# Nose
rtc.scene.append(Sphere(center=(0, 2.7, -9), radius=0.1, material=carrot))


# Body
rtc.scene.append(Sphere(center=(0, 1, -10), radius=1.5, material=snow))
rtc.scene.append(Sphere(center=(0, -1, -10), radius=2, material=snow))
rtc.scene.append(Sphere(center=(0, -3, -10), radius=2.5, material=snow))

# Buttons
rtc.scene.append(Sphere(center=(0, 1.4, -8), radius=0.1, material=button))
rtc.scene.append(Sphere(center=(0, 1, -8), radius=0.1, material=button))
rtc.scene.append(Sphere(center=(0, 0, -7.5), radius=0.2, material=button))
rtc.scene.append(Sphere(center=(0, -1, -8), radius=0.3, material=button))
rtc.scene.append(Sphere(center=(0, -2, -7.5), radius=0.4, material=button))

rtc.glRender()
rtc.write("RT1.bmp")
