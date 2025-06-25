from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
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


