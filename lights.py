# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso
import numpy as np
import matMath as mt


# Colores default
white = (1, 1, 1)
black = (0, 0, 0)

# Luces default
DIRECTION_L = 0
POINT_L = 1
AMBIENT_L = 2


class DirectionalLight(object):
    def __init__(this, direction=(0, -1, 0), intensity=1, color=white):
        this.direction = [d / mt.normL2(direction) for d in direction]
        this.intensity = intensity
        this.color = color
        this.lightType = DIRECTION_L

    def getDiffuseColor(this, intersect, raytracer):
        light_dir = [d * -1 for d in this.direction]
        intensity = mt.dotMatrix(intersect.normal, light_dir) * this.intensity
        intensity = float(max(0, intensity))

        diffuseColor = ([intensity * this.color[0],
                         intensity * this.color[1],
                         intensity * this.color[2]])

        return diffuseColor

    def getSpecColor(this, intersect, raytracer):
        light_dir = [d * -1 for d in this.direction]
        reflect = reflectVector(intersect.normal, light_dir)
        view_dir = mt.subtractVectors(raytracer.camPosition, intersect.point)
        view_dir = [vd / mt.normL2(view_dir) for vd in view_dir]

        spec_intensity = this.intensity * \
            max(0, np.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * this.color[0],
                     spec_intensity * this.color[1],
                     spec_intensity * this.color[2]]

        return specColor

    def getShadowIntensity(this, intersect, raytracer):
        light_dir = [d * -1 for d in this.direction]
        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(
            intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class PointLight(object):
    def __init__(this, point, constant=1.0, linear=0.1, quad=0.05, color=white):
        this.point = point
        this.constant = constant
        this.linear = linear
        this.quad = quad
        this.color = color
        this.lightType = POINT_L

    def getDiffuseColor(this, intersect, raytracer):
        light_dir = mt.subtractVectors(this.point, intersect.point)
        light_dir = [ld / mt.normL2(light_dir) for ld in light_dir]

        attenuation = 1.0
        intensity = mt.dotMatrix(intersect.normal, light_dir) * attenuation
        intensity = float(max(0, intensity))

        diffuseColor = [intensity * this.color[0],
                        intensity * this.color[1],
                        intensity * this.color[2]]

        return diffuseColor

    def getSpecColor(this, intersect, raytracer):
        light_dir = mt.subtractVectors(this.point, intersect.point)
        light_dir = [ld / mt.normL2(light_dir) for ld in light_dir]

        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = np.subtract(raytracer.camPosition, intersect.point)
        view_dir = [vd / np.linalg.norm(view_dir) for vd in view_dir]

        attenuation = 1.0

        spec_intensity = attenuation * \
            max(0, mt.dotMatrix(view_dir, reflect)
                ) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * this.color[0],
                     spec_intensity * this.color[1],
                     spec_intensity * this.color[2]]

        return specColor

    def getShadowIntensity(this, intersect, raytracer):
        light_dir = mt.subtractVectors(this.point, intersect.point)
        light_distance = mt.normL2(light_dir)
        light_dir = [ld / light_distance for ld in light_dir]

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(
            intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            if shadow_intersect.distance < light_distance:
                shadow_intensity = 1

        return shadow_intensity


class AmbientLight(object):
    def __init__(this, intensity=0.1, color=white):
        this.intensity = intensity
        this.color = color
        this.lightType = AMBIENT_L

    def getDiffuseColor(this, intersect, raytracer):
        return [ic * this.intensity for ic in this.color]

    def getSpecColor(this, intersect, raytracer):
        return [0, 0, 0]

    def getShadowIntensity(this, intersect, raytracer):
        return 0


# Reflect
def reflectVector(normal, direction):
    reflect = 2 * mt.dotMatrix(normal, direction)
    reflect = mt.multVN(v=normal, n=reflect)
    reflect = mt.subtractVectors(reflect, direction)
    reflect = [rf / mt.normL2(reflect) for rf in reflect]
    return reflect


# Refract
def refractVector(normal, direction, ior):
    # Snell's Law
    cosi = max(-1, min(1, mt.dotMatrix(direction, normal)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        normal = [n * -1 for n in normal]

    eta = etai / etat
    k = 1 - (eta**2) * (1 - (cosi**2))

    if k < 0:  # Total Internal Reflection
        return None

    R = mt.multVectors([eta * d for d in direction],
                       [(eta * cosi - k ** 0.5) * n for n in normal])

    return R


def fresnel(normal, direction, ior):
    # Fresnel Equation
    cosi = max(-1, min(1, mt.dotMatrix(direction, normal)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi**2) ** 0.5)

    if sint >= 1:  # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint**2) ** 0.5
    cosi = abs(cosi)

    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))

    return (Rs**2 + Rp**2) / 2
