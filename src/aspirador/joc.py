from iaLib import agent, joc
import random

class Aspirador(joc.JocNoGrafic):

    def __init__(self, agents: list[agent.Agent] | None = None):
        if agents is None:
            agents = []
        super(Aspirador, self).__init__(agents=agents)

        #DOS HABITACIONES: 1 y 2
        #False = sucia, True = limpia
        self.habitacions = {0: random.choice([True,False]), 1: random.choice([True,False])}

        #El aspirador empieza en una de las dos habitaciones
        self.posHabitacio = random.choice([0,1])


    def _draw(self):
        print(f"Posició de l'aspirador: {self.posHabitacio + 1}")
        print(f"Estado de la habitacion 1: {'neta' if self.habitacions[0] else 'bruta'}")
        print(f"Estado de la habitacion 2: {'neta' if self.habitacions[1] else 'bruta'}")
        print("-" * 30)   
        


    def percepcio(self):
        return {"Loc" : self.posHabitacio, "Net": self.habitacions[self.posHabitacio]}
        


    def _aplica(self, accio, params=None, agent_actual=None):
        print(f"Acció: {accio}")
        # accio de netejar la habitacio
        if accio == 'A':
            self.habitacions[self.posHabitacio] = True

        # accio de canviar d'habitacio a la dreta
        elif accio == 'D':
            if self.posHabitacio == 0:
                self.posHabitacio = 1
            else:
                raise ValueError(f"Acción no válida: {accio}")

        # accio de canviar d'habitacio a la esquerra
        elif accio == 'E':
            if self.posHabitacio == 1:
                self.posHabitacio = 0
            else:
                raise ValueError(f"Acción no válida: {accio}")

        elif accio == 'S':
            pass

        else:
            raise ValueError(f"Acción no válida: {accio}")

        #Comprovar si ambdues habitacions estan netes (fi del joc).
        if self.habitacions[0] and self.habitacions[1]:
            self._draw()                         # muestra el estado final
            print("Les dues habitacions estan netes. Fi del joc!")
            raise SystemExit                     # sale del bucle y termina el programa