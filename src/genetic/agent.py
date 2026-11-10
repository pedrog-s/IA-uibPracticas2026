""" Solució a la decodificació d'una cadena de caràcters emprant algoritmes genètics.

Author: Miquel Miró Nicolau (UIB), 2026
"""
import random 
from iaLib import agent
from tqdm import tqdm
from genetic.individu import Individu
MIDA_POBLACIO = 100
GENERACIONS = 3000
RATI_MUTACIO = 0.6
ELIT = 2                # los N mejores pasan tal cual a la siguiente generación
PACIENCIA = 3000          # generaciones seguidas sin mejorar antes de parar

def crear_poblacio(MIDA_POBLACIO):
    poblacioCompleta = []
    for i in range(MIDA_POBLACIO):
        poblacioCompleta.append(Individu())
        
    return poblacioCompleta



def pes_ruleta(ind):
    """Trozo de ruleta de un individuo (mayor = mejor). La distancia va de 0 a 2."""
    return 2 - ind.fitness
    

def ruleta(poblacio):
   
    #Selección por ruleta: elige UN individuo de la población.
    #Cada uno ocupa un trozo proporcional a su fitness para la ruleta (2 - distancia),
    #así que los de menor distancia (mejores) salen más a menudo.
   # Requiere que cada individuo ya tenga calculado su .fitness.
    
    # 1. Total de fitness de la población (2 - d: mayor = mejor)
    total = 0
    for ind in poblacio:
        total += 2 - ind.fitness

    # 2. Número al azar entre 0 y el total ("girar la ruleta")
    numero = random.uniform(0, total)

    # 3. Ir restando el trozo de cada uno; donde quede por debajo de 0, ese es el elegido
    for ind in poblacio:
        numero -= 2 - ind.fitness
        if numero < 0:
            return ind

    # 4. Por seguridad (redondeos con decimales): si no ha salido nadie, el último
    return poblacio[-1]



class Genetic(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        print(self._posicio_pintar)

    def actua(self, percepcio: dict):
        text_xifrat = percepcio["text"]

        # ---------- 1. Población inicial ----------
        poblacio = crear_poblacio(MIDA_POBLACIO)
        for ind in poblacio:
            ind.calcular_fitness(text_xifrat)

        millor = min(poblacio, key=lambda ind: ind.fitness)   # menor distancia = mejor
        sense_millora = 0

        # ---------- 2. Bucle de generaciones ----------
        for generacio in tqdm(range(GENERACIONS)):

            # Elitismo: ordenar de mejor a peor y conservar los ELIT mejores
            poblacio.sort(key=lambda ind: ind.fitness)
            nova_poblacio = poblacio[:ELIT]

            # Rellenar la nueva población con hijos
            while len(nova_poblacio) < MIDA_POBLACIO:
                pare1 = ruleta(poblacio)                 # SELECCIÓN
                pare2 = ruleta(poblacio)

                fill = pare1.creuar(pare2)               # CRUCE

                if random.random() < RATI_MUTACIO:       # MUTACIÓN
                    fill.mutar()

                fill.calcular_fitness(text_xifrat)       # EVALUACIÓN
                nova_poblacio.append(fill)

            poblacio = nova_poblacio                     # REEMPLAZO

            # Criterio de parada: ¿ha mejorado el mejor?
            millor_gen = min(poblacio, key=lambda ind: ind.fitness)
            if millor_gen.fitness < millor.fitness:
                millor = millor_gen
                sense_millora = 0
            else:
                sense_millora += 1
                if sense_millora >= PACIENCIA:
                    break

        # ---------- 3. Respuesta ----------
        print(f"\033[94mMillor distància: {millor.fitness:.3f}  (generació {generacio})\033[0m")
        return millor.desxifra(text_xifrat)