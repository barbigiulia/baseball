import copy

import networkx as nx
from flet_core import CupertinoListTile

from database.DAO import DAO
import sys
sys.setrecursionlimit(10000)


class Model:
    def __init__(self):
        self._grafo = nx.Graph()



    def getYears(self):
        return DAO.getAllYears()

    def getSquadre(self, anno):
        return DAO.getSquadre(anno)


    def buildGraph(self, anno):
        self._grafo.clear() # resetta il grafo prima di costruirlo
        squadre = self.getSquadre(anno) # sigle delle squadre --> nodi
        self._grafo.add_nodes_from(squadre)
        print(f"Nodi aggiunti (prima degli archi): {len(self._grafo.nodes)}")

        archiAggiunti = set( )
        salari = {}
        for s in squadre:
            salari[s] = DAO.getSalarioSquadra(s, anno)  # il salario di ciascun squadra
            print(f"Squadra: {s}, Salario: {salari[s]}")
        for u in squadre:
            for v in squadre:
                if u != v and frozenset({u,v}) not in archiAggiunti:
                    peso = salari[u]+salari[v]
                    self._grafo.add_edge(u, v, weight=peso)
                    archiAggiunti.add(frozenset({u,v}))  # fa si che (A,B) = (B,A)

        print(f"Archi aggiunti totali: {len(self._grafo.edges)}")


    def getAdiacenti(self, source, anno):
        vicini = self._grafo.neighbors(source)
        results = []
        for vicino in vicini:
            peso = self._grafo[source][vicino]["weight"]
            nomeVicino = DAO.getNomeSquadre(vicino, anno)
            results.append((peso, nomeVicino))
        results.sort(key=lambda x: x[0], reverse=True)
        return results

# ==================STATISTICHE ========================================

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getArchi(self):
        return self._grafo.edges


    def getArchiConPeso(self):
        return self._grafo.edges(data=True)  # COSI MI RESTITUISCE GLI ARCHI CON IL PESO!!


    # ==========RICORSIONE====================
    def getPercorso(self, source):
        self._bestPercorso=[source]
        self._bestPesi =[]
        self._bestTotale = 0

        visitati = set()
        visitati.add(source)

        self._ricorsione(source, visitati, [source], [], 0)
        return self._bestPercorso, self._bestPesi, self._bestTotale

    def _ricorsione(self, nodoCorrente, visitati, percorsoCorrente, pesiCorrenti, totaleCorrente):
        print(f"Nodo: {nodoCorrente}, Totale: {totaleCorrente}, Profondità: {len(percorsoCorrente)}")
        # aggiorno la soluzione migliore se il totale corrente è maggiore
        if totaleCorrente >self._bestTotale:
            self._bestPercorso = copy.deepcopy(percorsoCorrente)
            self._bestPesi = copy.deepcopy(pesiCorrenti)
            self._bestTotale = totaleCorrente

        if len(pesiCorrenti)>0:  # salvo l'ultimo peso usato
            ultimoPeso= pesiCorrenti[-1]
        else:
            ultimoPeso = float("inf")

        vicini_con_peso = []
        for vicino in self._grafo.neighbors(nodoCorrente):
            pesoArco = self._grafo[nodoCorrente][vicino]["weight"]
            if vicino not in visitati and pesoArco < ultimoPeso:
                vicini_con_peso.append((pesoArco, vicino))

        vicini_con_peso.sort(key=lambda x: x[0], reverse=True)

        for pesoArco, vicino in vicini_con_peso:
            visitati.add(vicino)
            percorsoCorrente.append(vicino)
            pesiCorrenti.append(pesoArco)

            self._ricorsione(vicino, visitati, percorsoCorrente,
                             pesiCorrenti, totaleCorrente+pesoArco)

            visitati.remove(vicino)
            percorsoCorrente.pop()
            pesiCorrenti.pop()