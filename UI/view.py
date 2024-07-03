import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP WIFI Hotspots Manager"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP WIFI Hotspots Manager", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW 1
        self._ddProvider = ft.Dropdown(label="Provider")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                               on_click=self._controller.handleCreaGrafo)

        row1 = ft.Row([ft.Container(self._ddProvider, width=300),
                       ft.Container(self._btnCreaGrafo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)

        self._controller.fillDDProvider()

        # ROW 2
        self._txtInDistanza = ft.TextField(label="Distanza")
        self._btnAnalisiGrafo = ft.ElevatedButton(text="Analizza grafo",
                                                  on_click=self._controller.handleAnalizzaGrafo)

        row2 = ft.Row([ft.Container(self._txtInDistanza, width=300),
                       ft.Container(self._btnAnalisiGrafo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row2)

        # ROW 3
        self._txtInString = ft.TextField(label="Stringa")
        self._btnCalcolaPercorso = ft.ElevatedButton(text="Calcola Percorso",
                                                     on_click=self._controller.handleCalcolaPercorso)

        row3 = ft.Row([ft.Container(self._txtInString, width=300),
                       ft.Container(self._btnCalcolaPercorso, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row3)

        # ROW 4
        self._ddTarget = ft.Dropdown(label="Target")

        row4 = ft.Row([ft.Container(self._ddTarget, width=300),
                       ft.Container(None, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row4)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()
