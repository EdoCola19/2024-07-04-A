from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self.sightings = {}
        sights = DAO.get_all_sightings()
        for sight in sights:
            self.sightings[sight.id] = sight

    def build_graph(self, year, shape):
        nodes = DAO.get_nodes(shape, year)
        for node in nodes:
            self._graph.add_node(node)
        edges = DAO.get_edges(shape, year)
        for edge in edges:

            sighting1 = edge.Sighting1
            sighting2 = edge.Sighting2
            self._graph.add_edge(sighting1, sighting2)

    def cerca_cammino(self):
        best_score = 0
        best_path = []

        for nodo in self._graph.nodes:
            self._search([nodo], {nodo.datetime.month: 1}, nodo.duration, 100, nodo.datetime.month, set([nodo]), nodo,
                         best_path, best_score)

        # stampa risultati
        self._stampa_cammino(best_path)

    def _search(self, parziale, mesi_counter, last_duration, current_score, last_month, visited, current_node,
                best_path_ref, best_score_ref):
        # aggiorna best
        if current_score > best_score_ref:

            best_score_ref += current_score
            best_path_ref.extend(parziale)

        for succ in self._graph.successors(current_node):
            if succ in visited:
                continue
            if succ.duration <= last_duration:
                continue

            mese = succ.datetime.month
            if mesi_counter.get(mese, 0) >= 3:
                continue

            # calcolo punteggio
            punti = 100
            if mese == last_month:
                punti += 200

            # aggiorno stato
            parziale.append(succ)
            visited.add(succ)
            mesi_counter[mese] = mesi_counter.get(mese, 0) + 1

            self._search(parziale, mesi_counter, succ.duration, current_score + punti, mese, visited, succ,
                         best_path_ref, best_score_ref)

            # backtrack
            parziale.pop()
            visited.remove(succ)
            mesi_counter[mese] -= 1
            if mesi_counter[mese] == 0:
                del mesi_counter[mese]

    def _stampa_cammino(self, path):
        print(
            f"Punteggio totale: {len(path) * 100 + sum(200 for i in range(1, len(path)) if path[i].datetime.month == path[i - 1].datetime.month)}")
        for sight in path:
            print(f"Durata: {sight.duration}, Mese: {sight.datetime.month}")





