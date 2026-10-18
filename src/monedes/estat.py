SOLUCIO = " XXXC"
COSTOS = {"D": 1, "G": 2, "B": 2}
GIRA = {"C": "X", "X": "C"}
 
 
class Estat:
    # Atributo de clase: así funciona Estat.accions dentro de genera_fills
    accions = [(tipus, pos) for tipus in ("D", "G", "B") for pos in range(5)]
 
    def __init__(self, monedes: str, cost: int = 0, cami: list | None = None):
        self.monedes = monedes
        self.cost = cost                                # g(n): coste acumulado
        self.cami = cami if cami is not None else []    # acciones desde el inicio

    def __lt__(self, other):
        return False      # solo para desempatar en la PriorityQueue
 
    def es_meta(self) -> bool:
        return self.monedes == SOLUCIO
 
    def heuristica(self) -> int:
        """h(n) = p0 + v1 + v2 + v3 + v4 (enunciado).
 
        p0 = distancia del hueco a su posición final (la 0).
        vi = 1 si la posición i no coincide con la solución.
        Decisión de diseño: si en la posición i está el hueco, cuenta como
        incorrecta (vi = 1), porque ahí debería haber una moneda.
        """
        p0 = self.monedes.find(" ")
        v = sum(1 for i in range(1, 5) if self.monedes[i] != SOLUCIO[i])
        return p0 + v
 
    def f(self) -> int:
        return self.cost + self.heuristica()            # f(n) = g(n) + h(n)
 
    def __eq__(self, other):
        return isinstance(other, Estat) and self.monedes == other.monedes
 
    def __hash__(self):
        return hash(self.monedes)
 
    def __repr__(self):
        return f"Estat({self.monedes!r}, cost={self.cost})"
 
    def transicio(self, accio: tuple[str, int]) -> "Estat":
        tipus, pos = accio
        caselles = list(self.monedes)
        buit = self.monedes.find(" ")
 
        if tipus == "G":
            caselles[pos] = GIRA[caselles[pos]]
        elif tipus == "D":
            caselles[buit] = caselles[pos]   # primero la moneda va al hueco...
            caselles[pos] = " "              # ...y después se vacía su casilla
        elif tipus == "B":
            caselles[buit] = GIRA[caselles[pos]]
            caselles[pos] = " "
 
        return Estat("".join(caselles), self.cost + COSTOS[tipus], self.cami + [accio])
 
    def es_legal(self, accio) -> bool:
        tipus, pos = accio
        buit = self.monedes.find(" ")
        if pos == buit:
            return False
        if tipus == "G":
            return True
        if tipus == "D":
            return abs(pos - buit) == 1
        if tipus == "B":
            return abs(pos - buit) == 2
        return False

    def genera_fills(self) -> list["Estat"]:
        fills = []
        for accio in Estat.accions:
            if self.es_legal(accio):
                fills.append(self.transicio(accio))

        return fills

        