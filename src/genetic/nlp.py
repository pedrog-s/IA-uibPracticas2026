import itertools
import re
from collections import Counter


def llevar_accents(text):
    """Substitueix les vocals accentuades i amb dièresi per la seva versió sense marca."""
    origen = "àèéíïòóúü"
    desti  = "aeeiioouu"
    taula_traduccio = str.maketrans(origen, desti)
    return text.translate(taula_traduccio)


def elimina_no_caracters(text):
    text = re.sub(r'[^a-zç ·]', '', text)
    text = re.sub(r'[ç·]', 'c', text)

    return text

def obtenir_freq_relatives(comptador) -> dict:
    """
    Calcula la freqüència relativa a partir d'un Counter.
    Retorna una llista de tuples: (bigrama, freq_absoluta, freq_relativa).
    """
    total_bigrames = sum(comptador.values())
    
    if total_bigrames == 0:
        return {}
        
    resultats = {}
    # Iterem sobre els elements ja ordenats de més a menys freqüents
    for element, compte in comptador.most_common():
        freq_relativa = round(compte / total_bigrames, 3)
        resultats[''.join(element)] = freq_relativa
        
    return resultats

def calcular_bigrames_lletres(text):
    """Calcula la freqüència de parelles de lletres consecutives."""
    text = text.lower()
    
    # Eliminem tot allò que no siguin lletres catalanes (espais, puntuació, números)
    nomen_lletres = elimina_no_caracters(text)
    
    # Creem els bigrames agrupant cada lletra amb la següent
    bigrames = itertools.pairwise(nomen_lletres)
    
    return obtenir_freq_relatives(Counter(bigrames))
