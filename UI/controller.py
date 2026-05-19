import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def read_DD(self):
        anni = self._model.getYears()
        options = []
        for a in anni:
            options.append(ft.dropdown.Option(a))
        return options

    def handleAnno(self, e):

        anno = self._view._ddAnno.value
        if anno is None or anno =="":
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text(f"Inserire un anno"))
            self._view.update_page()
            return

        try:
            anno = int(anno)
        except ValueError:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text(f"Errore conversione dell'intero"))
            self._view.update_page()
            return

        squadre = self._model.getSquadre(anno) # RECUPERO LE SQUADRE FILTRATE
        print(f"Squadre trovate: {squadre}")  # debug temporaneo

        # stampo le squadre che hanno giocato in quell'anno
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(squadre)} squadre che"
                                                       f" hanno giocato nell'anno {anno}", color="purple"))
        for s in squadre:
            self._view._txtOutSquadre.controls.append(ft.Text(s))  # è la sigla

        # AGGIORNO IL DROP DROWN "SQUADRE"
        self._view._ddSquadra.options = self.getSquadre(squadre)
        self._view._ddSquadra.value = None

        self._view.update_page()



    def getSquadre(self, squadre): # AGGIORNA IL MENU A TENDINA "SQUADRE"
        # CHIAMATA DENTRO IL METODO "handleAnno", altrimenti non si aggiorna il menu a tendina
        options = []
        for s in squadre:
            options.append(ft.dropdown.Option(s))
        return options




    def handleCreaGrafo(self, e):
        anno = int(self._view._ddAnno.value)
        self._model.buildGraph(anno)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))

        archi = self._model.getArchi()
        for a in archi:
            self._view._txt_result.controls.append(ft.Text(a))

        self._view.update_page()


    def handleDettagli(self, e):
        source = self._view._ddSquadra.value
        anno = int(self._view._ddAnno.value)
        if source is None or source=="":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un squadra"))
            self._view.update_page()
            return
        adiacenti = self._model.getAdiacenti(source, anno)
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {source} con il loro peso relativo", color="green"))
        for a in adiacenti:
            self._view._txt_result.controls.append(ft.Text(f"{a[0]} - {a[1]}", color="blue"))

        self._view.update_page()


    def handlePercorso(self, e):
        source = self._view._ddSquadra.value

        if source is None or source == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare una squadra"))
            self._view.update_page()
            return

        if self._model.getNumNodi() == 0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Creare prima il grafo"))
            self._view.update_page()
            return


        percorso, pesi, totale = self._model.getPercorso(source)

        self._view._txt_result.controls.append(ft.Text(f"Percorso ottimo da {source}:"
                                                       , color="purple"))
        for i, nodo in enumerate(percorso):
            self._view._txt_result.controls.append(ft.Text(nodo))
            if i < len(pesi):
                self._view._txt_result.controls.append(ft.Text(f"  peso arco: {pesi[i]}"))

        self._view._txt_result.controls.append(ft.Text(f"Peso totale: {totale}", color="blue"))
        self._view.update_page()