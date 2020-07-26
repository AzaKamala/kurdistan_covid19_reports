from spyre import server

class SimpleApp(server.App):
    title = "Kurdistan Covid19 Reports"
    inputs = []

    tabs = ['Erbil', 'Sulaymani', 'Halabja', 'Duhok']

    outputs = []

app = SimpleApp()
app.launch()