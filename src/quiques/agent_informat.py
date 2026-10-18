""" Fitxer que conté l'agent informat.

S'ha d'implementar el mètode:
    actua()
"""

from quiques.agent import Barca
from quiques.estat import Estat
#Importamos una cola con prioridad de la libreria de python
from queue import PriorityQueue

class BarcaGreedy(Barca):
    def __init__(self):
        super(BarcaGreedy, self).__init__()
        self.__tancats = None
        self.__frontera = None
        self.__cami_exit = None


    def heuristica(self, estat: Estat) -> int:
        return estat.llops_esq + estat.quica_esq

    
    def cerca(self, estat_inicial: Estat):
        self.__frontera = PriorityQueue()
        self.__tancats = set()
        h = self.heuristica(estat_inicial)
        contador = 0
        self.__frontera.put((h,contador, estat_inicial))
        contador += 1

        while not self.__frontera.empty():
            #la h , tampoco el contador aqui no la vamos a usar, se pone _ para que se entienda mejor
            _, _,  estat_actual = self.__frontera.get()

            if estat_actual.es_meta():
                self.__cami_exit = estat_actual.cami
                return True

            if estat_actual.es_segur() and estat_actual not in self.__tancats:
                for fill in estat_actual.genera_fill():
                    h = self.heuristica(fill)
                    self.__frontera.put((h, contador, fill))
                    contador +=1
                
                self.__tancats.add(estat_actual)
        return False
  
    def actua(self, percepcio: dict) -> tuple[str, (int, int)]:
        if self.__cami_exit is None:
            estat_inicial = Estat(
            local_barca = percepcio["Lloc"],
            llops_esq = percepcio["Llop Esq"],
            polls_esq = percepcio["Poll Esq"]
            )
            self.cerca(estat_inicial)

        if self.__cami_exit:
            quiques, llops = self.__cami_exit.pop(0)
            return "M", (quiques, llops)
        else:
            return "A", None 