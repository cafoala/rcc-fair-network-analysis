import dash
import dash_cytoscape as cyto
import networkx as nx
from dash import Input, Output, State, dcc, html

# Global NetworkX graph and state
G = nx.Graph()
previous_word = None

app = dash.Dash(__name__)
app.title = "Word Network"

app.layout = html.Div(
    [
        html.H1("Word Network Builder", style={"textAlign": "center"}),
        html.Div(
            [
                dcc.Input(
                    id="word-input",
                    type="text",
                    placeholder="Enter a word...",
                    debounce=False,
                    style={"marginRight": "8px", "padding": "6px", "fontSize": "16px"},
                ),
                html.Button(
                    "Submit",
                    id="submit-btn",
                    n_clicks=0,
                    style={"padding": "6px 14px", "fontSize": "16px"},
                ),
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        cyto.Cytoscape(
            id="cytoscape-graph",
            layout={"name": "cose"},
            style={"width": "100%", "height": "600px", "border": "1px solid #ccc"},
            elements=[],
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "label": "data(label)",
                        "background-color": "#4A90D9",
                        "color": "#fff",
                        "text-valign": "center",
                        "text-halign": "center",
                        "font-size": "14px",
                        "width": "50px",
                        "height": "50px",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "width": 2,
                        "line-color": "#aaa",
                        "curve-style": "bezier",
                    },
                },
            ],
        ),
    ],
    style={"maxWidth": "900px", "margin": "0 auto", "fontFamily": "sans-serif"},
)


def graph_to_elements(graph):
    """Convert a NetworkX graph to Cytoscape elements."""
    elements = []
    for node in graph.nodes():
        elements.append({"data": {"id": node, "label": node}})
    for source, target in graph.edges():
        elements.append({"data": {"source": source, "target": target}})
    return elements


@app.callback(
    Output("cytoscape-graph", "elements"),
    Output("word-input", "value"),
    Input("submit-btn", "n_clicks"),
    State("word-input", "value"),
    prevent_initial_call=True,
)
def add_word(n_clicks, word):
    global G, previous_word

    if not word or not word.strip():
        return dash.no_update, dash.no_update

    word = word.strip()

    if word not in G:
        G.add_node(word)

    if previous_word is not None and previous_word != word:
        G.add_edge(previous_word, word)

    previous_word = word

    return graph_to_elements(G), ""


if __name__ == "__main__":
    app.run(debug=True)
