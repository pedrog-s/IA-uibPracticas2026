""" Solució a la decodificació d'una cadena de caràcters emprant algoritmes genètics.

Author: Miquel Miró Nicolau (UIB), 2026
"""

from iaLib import agent
from tqdm import tqdm

MIDA_POBLACIO = #TODO
GENERACIONS = #TODO
RATI_MUTACIO = #TODO

class Genetic(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        print(self._posicio_pintar)

    def actua(self, percepcio: dict) -> tuple[str, (int, int)]:
        #TODO
        pass