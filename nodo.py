class Nodo:
    def __init__(self, estado, utilidad, minmax,  nodo_padre=None, profundidad = 0):
        self.estado = estado
        self.nodo_padre = nodo_padre
        self.hijos = []
        self.profundidad= profundidad
        self.utilidad = utilidad
        self.minmax = minmax