import copy
from tictac import victoria

class Estat:
    def __init__(self, taulell, torn, ultima_jugada=None): 
        self.taulell = taulell
        self.torn = torn 
        self.ultima_jugada = ultima_jugada

    def transicio(self, accio)-> "Estat":
        _, coordenada = accio
        x, y = coordenada
        nou_taulell = copy.deepcopy(self.taulell)
        nou_taulell[x][y] = self.torn

        
        if (self.torn == "0"):
            nouTorn = "X"
        else: 
            nouTorn = "0"

        return Estat(nou_taulell, nouTorn, coordenada)


    def genera_fills(self):
        fills = []
        for x in range(len(self.taulell)):
            for y in range(len(self.taulell[0])):
                if self.taulell[x][y] == " ":
                    fill = self.transicio(("P",(x,y)))
                    fills.append(fill)
        return fills


    def guanyador(self):
        if self.ultima_jugada is None:
            return None
        x, y = self.ultima_jugada
        if victoria.victoria(self.taulell, self.ultima_jugada):
            return self.taulell[x][y]
        return None


    def es_meta(self):
        if self.guanyador() is not None:     # alguien ha ganado
            return True
        if len(self.genera_fills()) == 0:    # no quedan jugadas: empate
            return True
        return False

    def utilitat(self, jugador_max):
        g = self.guanyador()
        if g == jugador_max:    # ha ganado MAX
            return 1
        if g is None:           # nadie ha ganado: empate
            return 0
        return -1               # ha ganado el otro (MIN)