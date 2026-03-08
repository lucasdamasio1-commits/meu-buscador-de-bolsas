import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Buscador de Bolsas"),
    html.P("Dashboard conectado ao Supabase")
])

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)

