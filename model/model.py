import copy
import random

import networkx as nx

from database.DAO import DAO

from geopy.distance import distance


class Model:
    def __init__(self):
        self._providers = DAO.getAllProviders()
        self._graph = nx.Graph()

    def getCammino(self, target, substring):
        # possibili source:
        sources = self.getNodesMostVicini()  # lista da cui devo prenderne uno
        source = sources[random.randint(0, len(sources))-1][0]
        # -1 perché randint ha estremi inclusi, [0] perché altrimenti source è una tupla

        if not nx.has_path(self._graph, source, target):
            print(f"{source} e {target} non sono connessi.")
            return [], source  # faccio la return di un cammino vuoto

        # altrimenti mi calcolo il cammino, in questo modo gestisco
        # il fatto che il cammino potrebbe non esserci

        self._bestPath = []
        self._bestLen = 0
        parziale = [source]

        self._ricorsione(parziale, target, substring)

        return self._bestPath, source  # faccio la return di source solo per poterlo stampare nel controller

    def _ricorsione(self, parziale, target, substring):

        if parziale[-1] == target:
            # devo uscure, ma prima controlo che sia una soluzione ottima
            if len(parziale) > self._bestLen:  # se sì me la salvo
                self._bestLen = len(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        # se non entro nel'if vuol dire che posso aggiungenre
        for v in self._graph.neighbors(parziale[-1]):  # v è una Location
            if v not in parziale and substring not in v.Location:
                # se entro qui vuol dire che è un nodo che posso aggiungere
                parziale.append(v)
                self._ricorsione(parziale, target, substring)
                parziale.pop()

    def buildGraph(self, provider, soglia):
        self._nodes = DAO.getLocationsOfProviderV2(provider)
        self._graph.add_nodes_from(self._nodes)

        # Add edges

        # MODO 1: faccio una query che mi restituisce gli archi
        allEdges = DAO.getAllEdges(provider)  # ho una lista di tuple che sono coppie di nodi che sono oggetti
        for edge in allEdges:  # di tipo Location, non sono stringhe, quindi faccio l'unpack di questo oggetto
            l1 = edge[0]  # di tipo location e tirare fuori le stringhe che avevo messo nei nodi
            l2 = edge[1]
            dist = distance((l1.latitude, l1.longitude), (l2.latitude, l2.longitude)).km
            if dist < soglia:
                self._graph.add_edge(l1, l2, weight=dist)

        print(f"Modo 1: N nodes: {len(self._graph.nodes)} - N edges: {len(self._graph.edges)}")

        self._graph.clear_edges()

        # MODO 2: modifico il metodo del DAO che legge i nodi, e ci aggiungo le coordinate di ogni location,
        # dopo, doppio ciclo sui nodi e mi calcolo le distanze in python
        for u in self._nodes:
            for v in self._nodes:
                if u != v:  # u e v sono location
                    dist = distance((u.latitude, u.longitude),(v.latitude, v.longitude)).km
                    if dist < soglia:
                        self._graph.add_edge(u, v, weight=dist)

        print(f"Modo 2: N nodes: {len(self._graph.nodes)} - N edges: {len(self._graph.edges)}")

        # MODO 3: doppio ciclo sui nodi e per ogni "possibile" arco faccio una query,
        # metodo da evitare per l'elevato numero di query, ma ha senso su grafi piccolini
        # quando le query per trovare gli archi sono complicate

    def getNodesMostVicini(self):
        listTuples = []

        for v in self._nodes:
            listTuples.append((v, len(list(self._graph.neighbors(v)))))

        listTuples.sort(key=lambda x: x[1], reverse=True)  # ordino per numerosità

        result1 = list(filter(lambda x: x[1] == listTuples[0][1] , listTuples))
        # prendo tutti gli elementi di questa lista che hanno come numero di vicini uguale al
        # primo elemento della lista che per definizione è quello con più vicini
        # filter come map vuole prima un metodo e poi un iterable, il metodo è il metodo che
        # mi permette di filtrare i valori della lista

        # Alternativa a filter:
        result2 = [x for x in listTuples if x[1] == listTuples[0][1]]
        # ovvero prendo tutti gli elementi di listTuples tale per cui l'elemento in posizione 2 della tupla
        # che è il nuemro di vicini è esattamente uguale al numero di vicini del primo elemento della lista

        print(len(result2))
        return result2

    def getAllProviders(self):  # metodo che mi permette di accedere ai provider
        return self._providers  # sarà una lista di stringhe

    def getAllLocations(self):
        return self._graph.nodes

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
