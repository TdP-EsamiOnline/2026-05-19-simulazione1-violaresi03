import networkx as nx
class Model:
    def __init__(self):
        # GRAFO
        self._idMapNames = {}  # perche i vertici sono Nomi degli artisti
        self._graph = nx.DiGraph() #Grado orientato
        #


   # self._graph.add_edge("A", "B")  # arco da A verso B
    #self._graph.add_edge("B", "C", weight=5)  # arco da B verso C con peso


    def getAllGenre(self):
        from database.DAO import DAO
        return DAO.getAllGenre()

    #GRAFO
    def buildGraph(self, genre):  #creo grafico, orientato
                                    #dato che la query è parametrica aggiungo anche qua i parametri
       self._idMapNames = {}
       self._graph = nx.DiGraph()
       from database.DAO import DAO

       self._names=DAO.getAllNodes(genre)  #chiamo temas perché nei nodi ci sono i nomi dei team
                                          #self._teams = res del DAO
       for n in self._names:
            self._idMapNames[n]=n   #Teams perchè sono i vertici
                                    #self._idMapTeams è un dizionario dove:
                                    #la chiave è t (il teamCode, es. "BOS")
                                    #il valore è t (stesso teamCode)
                                    #Serve dopo in getAllEdges per verificare se un team è nel grafo
       self._graph.add_nodes_from(self._names)


       #AGGIUNGIAMO ARCHI da a a b
       allEdges1= DAO.getAllEdges1(genre, idMapNames= self._idMapNames)
       for e in allEdges1: # e è l'arco

           self._graph.add_edge(e.a1, e.a2, weight=e.peso)    # arco da a1 verso a2 con peso
                                                             #vedi come hai chiamato i parametri della classe Arco
                                                             #funzione a cui do due nodi per creare l'arco
                                                             #t1 e t2 da arco
                                                             #t1 e t2 sono vicini

                           # con buildGraph si crea questa struttura
                           #Tre livelli di dizionari annidati:
                              #1 il dizionario esterno ha come chiave il nodo ("BOS"), valore → il dizionario dei vicini
                              #2 il dizionario intermedio ha come chiave il vicino ("NYA", "CLE"), valore→ il dizionario degli attributi dell'arco tra i due nodi es. {"weight": 1500000.0}
                              #3 il dizionario interno ha come chiave l'attributo ("weight"), valore → il valore numerico del peso, es. 1500000.0
                           #
                           # self._graph = {
                           #    "BOS": {     #NODO
                           #        "NYA": {"weight": 1500000.0},  #VICINO CON PESO DELL'ARCO
                           #        "CLE": {"weight": 2000000.0}   #VICINO CON PESO DELL'ARCO
                           #    },
                           #    "NYA": {     #NODO
                           #       "BOS": {"weight": 1500000.0},
                           #        ...
                           #    }
                           # }
       # AGGIUNGIAMO ARCHI da b a a
       allEdges2 = DAO.getAllEdges2(genre, idMapNames=self._idMapNames)
       for e in allEdges2:  # e è l'arco
           self._graph.add_edge(e.a2, e.a1, weight=e.peso)

       # AGGIUNGIAMO ARCHI da a a b e da b a a
       allEdges3 = DAO.getAllEdges3(genre, idMapNames=self._idMapNames)
       for e in allEdges3:  # e è l'arco
           self._graph.add_edge(e.a1, e.a2, weight=e.peso)
           self._graph.add_edge(e.a2, e.a1, weight=e.peso)

    def getGraphDetails(self):  #return numero nodi e archi
        return len(self._graph.nodes), len(self._graph.edges)
    #
    def getGraph(self):# per rendere self._graph accessibile dal controller
        return self._graph


    def getTop5Archi(self):
        return sorted(self._graph.edges(data= True), key=lambda x: x[2]["weight"], reverse= True)[:5]


    def getInfluenza(self, nodo):
        uscenti = sum(self._graph[nodo][v]["weight"]
                      for v in self._graph.successors(nodo))

        entranti = sum(self._graph[u][nodo]["weight"]
                       for u in self._graph.predecessors(nodo))

        return uscenti - entranti

    def getArtistaPiuInfluente(self):

        migliore = max(self._graph.nodes, key=self.getInfluenza)

        return migliore, self.getInfluenza(migliore)
