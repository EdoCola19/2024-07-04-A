import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        self._model.build_graph(year, shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model._graph.number_of_nodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model._graph.number_of_edges()}"))
        import networkx as nx
        componenti = list(nx.connected_components(self._model._graph))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di componenti connesse: {len(componenti)}"))
        if len(componenti) > 0:
            componente_max = max(componenti, key=len)
            self._view.txt_result1.controls.append(ft.Text(f"Componente più grande: {len(componente_max)} nodi"))
            self._view.txt_result1.controls.append(ft.Text(f"Dettagli (Città - Data):"))

            lista = sorted(componente_max, key=lambda s: s.datetime)

            for s in lista:
                self._view.txt_result1.controls.append(
                    ft.Text(f"{s.city} - {s.datetime.strftime('%Y-%m-%d')}")
                )


        self._view._page.update()

    def handle_path(self, e):
        pass

    def fillDD(self):
        years = DAO.get_years()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year["year"]))
        self._view._page.update()
    def fillDDshape(self):
        shapes = DAO.get_shapes()
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape["shape"]))
        self._view._page.update()


