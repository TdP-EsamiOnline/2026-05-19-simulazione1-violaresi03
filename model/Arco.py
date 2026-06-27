from dataclasses import dataclass
from model.Artist import Artist


@dataclass
class Arco:  #La classe Arco rappresenta un arco del grafo — collega due nodi con un peso.
             #Viene creato nel DAO dentro getAllEdges e
             # poi usato nel model per aggiungere l'arco al grafo: self._graph.add_edge(e.t1, e.t2, weight=e.peso)
    a1: str  # nel select della query getAllNodes del DAO definisco l'attributo string da dare ai nodi
    a2: str
    peso: int