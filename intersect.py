# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso

# Colores default
white = (1, 1, 1)
black = (0, 0, 0)


class Intersect(object):
    def __init__(this, distance, point, normal, texcoords, sceneObj):
        this.distance = distance
        this.point = point
        this.normal = normal
        this.sceneObj = sceneObj
        this.texcoords = texcoords
