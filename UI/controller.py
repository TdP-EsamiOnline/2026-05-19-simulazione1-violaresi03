import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre=None


    # DDROPDOWN
    def _choiceDDGenre(self, e):  #_choiceDDGenre invece viene chiamata ogni volta
                                  # che l'utente seleziona un genere dal dropdown — il suo unico scopo è salvare la scelta dell'utente in self._choiceGenre.
        self._choiceGenre = e.control.value
        # _choiceDDGenre salva il genere scelto dall'utente in self._choiceGenre e
        # lo passa a fillDDsGenre(self._choiceGenre)
        # fillDDsGenre riceve quell'anno come parametro genre
        # e lo usa per filtrare i genre dal database
        print(f"Hai selezionato come genere {self._choiceGenre}")  # appare sul terminale del main
        # quando selezioni un valore del dropdown

    def fillDDGenre(self):
        generi = self._model.getAllGenre()
        print(f"Genere trovati: {generi}")  # aggiungi questo
        generioptions = list(map(lambda x: ft.dropdown.Option(x), generi))
        self._view._ddGenre.options = generioptions  # leggi da view

        self._view.update_page()

#GRAFO
    def handleCreaGrafo(self, e):
        print("Crea Grafo cliccato")
        genre = self._choiceGenre  # il grafo si crea a partire dalla selezione di un anno da parte dell'utente
        if genre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona un genere!", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(genre)  # costruisce il grafo con i team dell'anno scelto
        self._graph = self._model.getGraph()
        nNodi, nArchi = self._model.getGraphDetails()  # prende numero nodi e archi dal model
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nNodi}, Archi: {nArchi}"))

        #PUNTO C
        top5= self._model.getTop5Archi()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi", color="red"))
        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]}->{arco[1]}: {arco[2]["weight"]} ")) #vedi l'output come lo vuole
          #artista più influente
        artista, infl = self._model.getArtistaPiuInfluente()
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {artista} ({infl})"))
        self._view.update_page()



    def handleCammino(self,e):
        pass