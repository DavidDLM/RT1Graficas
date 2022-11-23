# OBJ.py
# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso

class Obj(object):
    def __init__(this, filename):
        with open(filename, "r") as file:
            this.lines = file.read().splitlines()

        this.vertices = []
        this.texcoords = []
        this.normals = []
        this.faces = []

        for line in this.lines:
            try:
                prefix, value = line.split(' ', 1)
            except:
                continue

            if prefix == 'v':  # Vertices
                this.vertices.append(list(map(float, value.split(' '))))
            elif prefix == 'vt':
                this.texcoords.append(list(map(float, value.split(' '))))
            elif prefix == 'vn':
                this.normals.append(list(map(float, value.split(' '))))
            elif prefix == 'f':
                this.faces.append([list(map(int, vert.split('/')))
                                  for vert in value.split(' ')])
