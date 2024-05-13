class Nodo:
    def __init__(self, estado, utilidad, minmax,  nodo_padre=None, profundidad = 0, rival=None):
        self.estado = estado
        self.nodo_padre = nodo_padre
        self.hijos = []
        self.profundidad= profundidad
        self.utilidad = utilidad
        self.minmax = minmax
        self.rival = rival

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def obtener_hijos(self):
        return self.hijos