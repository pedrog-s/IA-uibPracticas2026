""" Modul que implement un xifratge de substitució monoalfabètica aleatòria.

Desenvolupat per: Miquel Miró Nicolau (UIB), 2026.
"""
import random
import string
from importlib.resources import files

from iaLib import joc

from genetic import nlp


class Genetic(joc.JocNoGrafic):

    with (files("genetic") / "blai.txt").open('r', encoding='utf-8') as file:
        __text = file.read()

    def __init__(
            self,
            agents,
    ):
        clau = list(string.ascii_lowercase)
        random.shuffle(clau)
        
        self.__clau = clau


        paraules = self.__text.split(" ")

        left = random.randint(0, len(paraules))
        right = random.randint(left, len(paraules))
        
        paraules = paraules[left:right]
        paraules = [self.__encripta(nlp.elimina_no_caracters(nlp.llevar_accents(nlp.llevar_accents(p.lower())))) for p in paraules]

        self.__sub_text = paraules
        
        self.__solucio = None

        super().__init__(agents)


    def _aplica(self, accio, params=None, agent_actual=None):
        if self.__solucio is None:
            diffs = self.__verifica(accio)
            self.__solucio = {
                "diffs": diffs,
                "resultat": accio
            }


    def _draw(self):
        if self.__solucio:
            text = ["".join(paraula) for paraula in self.__sub_text]
            text = " ".join(text)

            print(f"El text original era: \n {text} \n La proposta de solució es: \n {self.__solucio['resultat']} \n \tHi ha {self.__solucio['diffs']} errors.")
            self.set_game_status(True)
        

    def __encripta(self, text):
        if isinstance(text, str) and " " in text:
            text = text.split(" ")

        if isinstance(text, str) and " " not in text:
            text_enc = [self.__clau[ord(lletra) - ord("a")] for lletra in text]
        else:
            text_enc = [[self.__clau[ord(lletra) - ord("a")] for lletra in paraula] for paraula in text]

        return text_enc
    
    def percepcio(self) -> dict:
        return {"text": self.__sub_text}

    def __verifica(self, cadena):
        cadena_enc = self.__encripta(cadena)
        diffs = sum(a != b for a, b in zip(self.__sub_text, cadena_enc)) + abs(len(self.__sub_text) - len(cadena_enc))

        return diffs
        
    
