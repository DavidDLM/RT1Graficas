# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso

white = (1, 1, 1)
black = (0, 0, 0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    def __init__(this, diffuse=white):
        this.diffuse = diffuse
