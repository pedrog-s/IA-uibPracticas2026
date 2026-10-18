""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""
from iaLib import agent
from tictac.estat import Estat



class Agent(agent.Agent):
    def __init__(self, poda = False):
        super(Agent, self).__init__(long_memoria=1)
        self.__visitats = None
        self.__cami_exit = None
        self.__poda = poda
        self.jugador = None          # mi ficha (MAX); la pone actua


    def cerca(self, estat, alpha, beta, torn_max=True):
        if estat.es_meta():                          # hoja: valor real
            return estat.utilitat(self.jugador)

        puntuacions = []
        for fill in estat.genera_fills():            # cada jugada posible
            valor = self.cerca(fill, alpha, beta, not torn_max)   # recursión, cambia el turno
            puntuacions.append(valor)

        if torn_max:
            return max(puntuacions)                  # yo elijo lo mejor para mí
        else:
            return min(puntuacions)                  # el rival, lo peor para mí



    def actua(self, percepcio):
        self.jugador = percepcio["torn"]             # ¿quién soy yo?
        estat = Estat(percepcio["taulell"], percepcio["torn"])

        if estat.es_meta():                          # no queda nada por hacer
            return "E"

        millor_valor = float("-inf")
        millor_jugada = None
        for fill in estat.genera_fills():
            valor = self.cerca(fill, float("-inf"), float("inf"), torn_max=False)
            if valor > millor_valor:
                millor_valor = valor
                millor_jugada = fill.ultima_jugada   # ¡la coordenada que ha creado este hijo!
        return "P", millor_jugada
