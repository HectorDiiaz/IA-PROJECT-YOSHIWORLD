import copy

class Nodo:
    def __init__(self, estado, utilidad, minmax, tablero, estadoContrincante, nodo_padre=None, profundidad = 0):
        self.estado = estado
        self.nodo_padre = nodo_padre
        self.hijos = []
        self.profundidad= profundidad
        self.utilidad = utilidad
        self.minmax = minmax
        self.tablero = copy.deepcopy(tablero) 
        self.estadoContrincante = estadoContrincante

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def obtener_hijos(self):
        return self.hijos
    
    #Funcion que agrega el nuevo estado a su tablero
    def agregarPosicionTablero(self):
        if(self.minmax == "MAX"):
            self.tablero[self.estado[0]][self.estado[1]] = 2
        else:
            self.tablero[self.estado[0]][self.estado[1]] = 1