""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""

from iaLib import agent
from queue import PriorityQueue
from monedes.estat import Estat 

SOLUCIO = " XXXC"


class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__frontera = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def actua(self, percepcio):
        if self.__accions is None:
            estat_inicial = Estat(percepcio["Monedes"])
            if not self.cerca(estat_inicial):
                self.__accions = []          # sin solución: no se vuelve a buscar en cada turno

        if self.__accions:
            return self.__accions.pop(0)     # ("D", 3), ("G", 4)...
        return "R", None

    



    def cerca(self, estat_inicial: Estat)-> bool:
        self.__frontera = PriorityQueue()
        self.__tancats = set()

        prioritat = estat_inicial.f()

        self.__frontera.put((prioritat, estat_inicial))

        while  not self.__frontera.empty():
            _, estat_actual = self.__frontera.get()
            if estat_actual in self.__tancats:
                continue

            if estat_actual.es_meta():
                self.__accions = estat_actual.cami
                return True

            self.__tancats.add(estat_actual)

            for fill in estat_actual.genera_fills():
                if fill not in self.__tancats:
                    self.__frontera.put((fill.f(), fill))
        return False



    




