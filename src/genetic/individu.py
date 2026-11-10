import random 
from genetic import nlp
import json
from importlib.resources import files

ABECEDARI = "abcdefghijklmnopqrstuvwxyz"
with (files("genetic") / "bigrama.json").open("r", encoding="utf-8") as fitxer:
    BIGRAMES_REF = json.load(fitxer)

def distancia(bigrames, referencia):
    """
    Mide cuánto se diferencian dos "huellas" de bigramas.
    0 = idénticas, 2 = no tienen nada en común.  MENOR = MEJOR.
    """
    total = 0
    for bigrama in set(bigrames) | set(referencia):      # todos los bigramas de los dos, sin repetir
        frec_text = bigrames.get(bigrama, 0)             # si no está en mi texto → 0
        frec_ref  = referencia.get(bigrama, 0)           # si no está en el catalán → 0
        total += abs(frec_text - frec_ref)               # diferencia sin signo
    return total



class Individu:
    def __init__(self, clau = None):
        # El problema es que si hacemos abecedari = "abc..." sera un string, y necesitamos que sea un array
        if clau is None:
            abecedari = list(ABECEDARI)
            barajado = list(ABECEDARI)
            random.shuffle(barajado)
            self.clau = {}
            for i in range(26):
                self.clau[abecedari[i]] = barajado[i]
        else:
            self.clau = clau

        self.fitness = None

    def desxifra(self, text_encriptat):
        """Traduce el texto cifrado con SU clave. Devuelve un str."""
        text_desxifrat = []
        for paraula in text_encriptat:
            parcialDesxifrat = []
            for lletra in paraula:
                parcialDesxifrat.append(self.clau[lletra])            
            text_desxifrat.append("".join(parcialDesxifrat))   # ['e','l'] → "el"
        return " ".join(text_desxifrat)                        # ["el","meu",""] → "el meu "

    def calcular_fitness(self, text_encriptat):
        """Calcula SU nota: distancia entre los bigramas de su texto y los del catalán. MENOR = MEJOR."""
        text = self.desxifra(text_encriptat)                   # 1. clave → texto
        bigrames = nlp.calcular_bigrames_lletres(text)         # 2. texto → bigramas
        self.fitness = distancia(bigrames, BIGRAMES_REF)       # 3. bigramas → número (se guarda)
        return self.fitness
    
    def creuar(self, altre):
        """
        self = padre 1, altre = padre 2. Devuelve UN hijo (un Individu nuevo).
        El hijo siempre es una permutación válida: cada letra aparece una sola vez.
        """
        # 0. Claves como listas de valores en orden a..z  →  ['c','a','f',...]
        pare1 = list(self.clau.values())
        pare2 = list(altre.clau.values())

        # 1. Punto de corte al azar (nunca 0 ni 26: el hijo sería una copia)
        tall = random.randint(1, 25)

        # 2. Copiar el padre 1 hasta el corte
        fill = pare1[:tall]

        # 3. Seguir con el padre 2 desde el corte, saltando las letras que ya tiene el hijo
        for lletra in pare2[tall:]:
            if lletra not in fill:
                fill.append(lletra)

        # 4. Añadir al final las letras que faltan, en orden aleatorio
        falten = []
        for lletra in ABECEDARI:
            if lletra not in fill:
                falten.append(lletra)
        random.shuffle(falten)
        fill = fill + falten

        # 5. Volver a convertir la lista en diccionario a..z y crear el hijo
        nova_clau = {}
        for i in range(26):
            nova_clau[ABECEDARI[i]] = fill[i]
        return Individu(nova_clau)

    def mutar(self):
        """
        Mutación por intercambio: se eligen dos letras cifradas al azar
        y se intercambian sus traducciones. La clave sigue siendo una permutación válida.
        """
        # Elegir dos letras DISTINTAS del alfabeto al azar
        a, b = random.sample(ABECEDARI, 2)

        # Intercambiar sus valores
        self.clau[a], self.clau[b] = self.clau[b], self.clau[a]

        # La clave ha cambiado → la nota anterior ya no sirve
        self.fitness = None