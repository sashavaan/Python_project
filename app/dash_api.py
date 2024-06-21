from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
import plotly
import psutil
from .monitor import update_df, df, CPU_COUNT, conections

UPDATE_INTERVAL = 75

dash_app = Dash(__name__, requests_pathname_prefix="/dashboard/", title="project", external_stylesheets=[dbc.themes. SKETCHY])


header = dbc.Row(
    dbc.Col(
        [
            html.Div(style={"height": 30}),
            html.H1("Project", className="text-center"),
        ]
    ),
    className="mb-4",
)



tabs_styles = {
    'height': '55px'
}

tab_style = {
    'padding': '11px',
    'fontWeight': 'bold',
    'borderBottom': '2px solid #d6d6d6',
    'borderTop': '2px solid #d6d6d6',
    'font-size': '20px',
}

tab_selected_style_cpu = {
    'backgroundColor': '#f6b6b6',
    'color': 'black',
    'padding': '15px',
    'borderBottom': '2px solid #f39b9b',
    'borderTop': '2px solid #f39b9b',
    'font-size': '15px'
}
tab_selected_style_ram = {
    'backgroundColor': '#ffcebd',
    'color': 'black',
    'padding': '15px',
    'borderBottom': '2px solid #ffb89e',
    'borderTop': '2px solid #ffb89e',
    'font-size': '15px'
}
tab_selected_style_rom = {
    'backgroundColor': '#fff6d1',
    'color': 'black',
    'padding': '15px',
    'borderBottom': '2px solid #ffec9e',
    'borderTop': '2px solid #ffec9e',
    'font-size': '15px'
}
tab_selected_style_network = {
    'backgroundColor': '#dceadc',
    'color': 'black',
    'padding': '15px',
    'borderBottom': '2px solid #c9dec9',
    'borderTop': '2px solid #c9dec9',
    'font-size': '15px'
}
tab_selected_style_info = {
    'backgroundColor': '#d3e2ee',
    'color': 'black',
    'padding': '15px',
    'borderBottom': '2px solid #a7c4dd',
    'borderTop': '2px solid #a7c4dd',
    'font-size': '15px'
}
tab_selected_style_setting = {
    'backgroundColor': '#ddddf8',
    'color': 'black',
    'padding': '15px',
    'borderBottom': '2px solid #c3c3f3',
    'borderTop': '2px solid #c3c3f3',
    'font-size': '15px'
}


dash_app.layout = dbc.Container(
    [
        header,
        dcc.Tabs(

            [
                dcc.Tab(label='CPU', children=[
                    dcc.Graph(id="graph_cpu"),
                    dcc.Graph(id="graph_cpu_avg"),       
                ], style=tab_style, selected_style=tab_selected_style_cpu),

                dcc.Tab(label='RAM', children=[
                    dcc.Graph(id="graph_ram"),
                    dcc.Graph(id="graph_swap"),
                ], style=tab_style, selected_style=tab_selected_style_ram),
                
                dcc.Tab(label='ROM', children=[
                    dcc.Graph(id="graph_rom"),
                ], style=tab_style, selected_style=tab_selected_style_rom),
                
                dcc.Tab(label='Network', children=[
                    dcc.Graph(id="network"),
                    dcc.Graph(id="graph_connections"),
                ], style=tab_style, selected_style=tab_selected_style_network),

                dcc.Tab(label='Information', children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("CPU Information", className="card-title"),
                                html.P("Number of CPU Cores: " + str(CPU_COUNT)),
                    
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("CPU Average Load", className="card-title"),
                                html.P("CPU Average Load: " + str(psutil.cpu_percent())),
                            ]
                        )
                    ), 
                ], style=tab_style, selected_style=tab_selected_style_info),

                dcc.Tab(label='Setting', style=tab_style, selected_style=tab_selected_style_info),
            
            ], style=tabs_styles
        ),
        dcc.Interval(id="timer", interval=UPDATE_INTERVAL),
    ],
    fluid=True,
)


@dash_app.callback(
    Output("timer", "interval"),
    Input("update-interval-slider", "value")
)
def update_interval(value):
    return value 

@dash_app.callback(
    Output("graph_cpu", "style"),
    Output("graph_ram", "style"),
    Output("graph_swap", "style"),
    Input("display-data-checkbox", "value")
)
def update_displayed_data(value):
    cpu_style = {} if "cpu" in value else {"display": "none"}
    ram_style = {} if "ram" in value else {"display": "none"}
    swap_style = {} if "swap" in value else {"display": "none"}
    return cpu_style, ram_style, swap_style


@callback(Output("graph_cpu", 'figure'), Input("timer", 'n_intervals'))
def update_graph(n):
    update_df()
    traces = list()
    for t in df.columns[:CPU_COUNT]:
        traces.append(
            plotly.graph_objs.Line(
                x=df.index,
                y=df[t],
                name=t
            )
        )
    return {"data": traces, "layout": {"template": "plotly_dark"}}

@callback(Output("graph_cpu_avg", 'figure'), Input("timer", 'n_intervals'))
def update_cpu_avg_graph(n):
    update_df()
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['cpu_avg'],
            name='CPU Average'
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark"}}


@callback(Output("graph_ram", 'figure'), Input("timer", 'n_intervals'))
def update_ram_graph(n):
    
    update_df()

    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['ram'],
            name='RAM',
            yaxes_range=[0, 100]
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark", "yaxis": {"range": (0, 100)}}}

@callback(Output("graph_swap", 'figure'), Input("timer", 'n_intervals'))
def update_swap_graph(n):

    update_df()
    
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['swap'],
            name='SWAP'
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark", "yaxis": {"range": (0, 100)}}}



@callback(Output("graph_rom", 'figure'), Input("timer", 'n_intervals'))
def update_rom_graph(n):
    update_df()
    

    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['disk_usage'],
            name='ROM'
        )
    )

    return {"data": traces, "layout": {"template": "plotly_dark", "yaxis": {"range": (0, 100)}}}


@callback(Output("network", 'figure'), Output("net_sent", "children"), Input("timer", 'n_intervals'))
def update_network_graph(n):
    
    update_df()
    
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['network_sent'],
            name='Sent'
        )
    )

    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['network_received'],
            name='Received'
        )
    )

    return {"data": traces, "layout": {"template": "plotly_dark"}}, f"Total sent: {df.loc[299, 'network_sent'] / (2 ** 20):.2f}"

@callback(Output("graph_connections", 'figure'), Input("timer", 'n_intervals'))
def update_connections_graph(n):
   
    update_df()
    

    traces = list()
    traces.append(
        plotly.graph_objs.Bar(
            x=list(conections.keys()),
            y=list(conections.values()),
            name=f"Connection {len(traces)+1}"
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark"}}

if __name__ == "__main__":
    
    update_df()

    dash_app.run_server(debug=True)