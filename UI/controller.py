import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        # questo metodo mi deve prima prendere tutte le informazioni che mi servono
        provider = self._view._ddProvider.value  # dato che è una stringa posso accedere direttamente al value
        if provider is None:
            print("Seleziona un provider")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Seleziona un provider."))
            self._view.update_page()
            return  # perché non ha senso continuare

        soglia = self._view._txtInDistanza.value
        if soglia == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Distanza non inserita."))
            self._view.update_page()
            return

        try:
            sogliaFloat = float(soglia)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione, soglia inserita non numerica"))
            self._view.update_page()
            return

        # se provider non è None vuol dire che è una stringa valida, e se soglia è effettivamente un float, faccio:
        self._model.buildGraph(provider, sogliaFloat)

        nNodes, nEdges = self._model.getGraphDetails()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato. Il grafo ha {nNodes} nodi "
                                                       f"e {nEdges} archi."))

        self.fillDDTarget()

        self._view.update_page()

    def handleAnalizzaGrafo(self, e):
        # questo metodo prima si assicura che il grafo sia stato creato

        nNodes, nEdges = self._model.getGraphDetails()
        if nNodes == 0 and nEdges == 0:  # così mi assicuro di non avere un grafo con dei nodi ma non degli archi
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione, grafo vuoto."))
            self._view.update_page()
            return

        # passato questo if vuol dire che il grafo è pieno e posso chiamare il metodo del modello

        lista = self._model.getNodesMostVicini()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Nodi con più vicini:"))
        for l in lista:
            self._view._txt_result.controls.append(ft.Text(f"{l[0]} -- {l[1]}"))

        self._view.update_page()

    def handleCalcolaPercorso(self, e):
        target = self._choiceLocation
        substring = self._view._txtInString.value

        # il target sono sicura di averlo selezionato perché lo leggo da self._choiceLocation,
        # faccio il controllo sulla substring

        if substring == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Attenzione, stringa non inserita."))
            self._view.update_page()
            return

        path, source = self._model.getCammino(target, substring)
        # questo path potrebbe non esistere, quindi se non esiste ho un errore nel model, quindi lo gestisco

        if path == []:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Non ho trovato un cammino fra {source} e {target}"))
            self._view.update_page()
            return

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Ho trovato un cammino fra {source} e {target}:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))

        self._view.update_page()

    def fillDDProvider(self):
        providers = self._model.getAllProviders()
        providers.sort()  # sono stringhe quindi automaticamente ce le ho ordinate in ordine alfabetico

        """
        # Modo 1:
        for p in providers:
            self._view._ddProvider.options.append(ft.dropdown.Option(p))
            # dato che sono stringhe passo direttamente p, ma se nel dd avessi un oggetto mi conviene passarlo
            # con la forma estesa, quindi data = l'oggetto, text = il toString dell'oggetto e poi
            # un metodo on_click che si va a leggere l'oggetto
        self._view.update_page()
        """

        # Modo 2:
        providersDD = map(lambda x: ft.dropdown.Option(x), providers)
        # self._view._ddProvider.options = list(providersDD)
        # questo metodo crea problemi nel momento in cui questa providerDD non esiste più,
        # ovvero quando esco dalla funzione, quindi per evitare questo problema faccio extend
        self._view._ddProvider.options.extend(providersDD)

        self._view.update_page()

    def fillDDTarget(self):
        locations = self._model.getAllLocations()
        locationsDD = map(lambda x: ft.dropdown.Option(data=x, text=x.Location,
                                                       on_click=self.readChoiceLocation), locations)
        # questo è il modo in cui costruisco un dd quando voglio recuperare l'oggetto quando seleziono i campi
        self._view._ddTarget.options.extend(locationsDD)

    def readChoiceLocation(self, e):
        # l'evento ha un campo control che ha un campo data che contiene l'oggetto
        if e.control.data is None:  # quando non viene selezionato
            self._choiceLocation = None
        else:
            self._choiceLocation = e.control.data


