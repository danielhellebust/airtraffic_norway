import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime as dt


#Load data
df = pd.read_csv('airport_location.csv')

#Create app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H3('Total passengers on board at departure and arrival at selected airports'),
                style={'textAlign': 'center', 'color': 'black', 'font-size': '50px', 'font-weight': 'bold', 'font-family': 'Arial', 'margin-top': '20px'}),
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            html.H6('Start date'),
            dcc.Dropdown(
            id='date-dropdown_start',
            options=[{'label': i, 'value': i} for i in df['Date'].unique()],
            value=None,
            placeholder='Select a start date. Year-Month. Default 2009-01',
            clearable=True
        )], width=3),
        dbc.Col([
            html.H6('End date'),
            dcc.Dropdown(
            id='date-dropdown_end',
            options=[{'label': i, 'value': i} for i in df['Date'].unique()],
            value=None,
            placeholder='Select an end date. Year-Month. Default 2023-02.',
            clearable=True

        )], width=3),
        dbc.Col([
            html.H6('Airport(s)'),
            dcc.Dropdown(
            id='airport-dropdown',
            options=[{'label': i, 'value': i} for i in df['Airport'].unique()],
            value=None,
            placeholder='Select an airport(s). Default all airports.',
            multi=True,
            clearable=True

        )], width=4),
    ], justify="center"),
        dbc.Col([
            dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id='airport-graph', config={'scrollZoom': False, 'staticPlot': False, 'doubleClick': False}))),
            dbc.Col(dcc.Loading(dcc.Graph(id='airport-graph3', config={'scrollZoom': False})))
        ])

        ],md=12),
        dbc.Col([
            dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id='airport-graph2', config={'scrollZoom': False}))),
        ])

        ]),

])


@app.callback(
    [Output('airport-graph', 'figure'),
     Output('airport-graph2', 'figure'),
     Output('airport-graph3', 'figure')],
    [
        Input('date-dropdown_start', 'value'),
        Input('date-dropdown_end', 'value'),
        Input('airport-dropdown', 'value')
    ]
)

def update_graph(start_date,end_date,airport):
    if start_date == None:
        start_date = '2009-01'

    if end_date == None:
        end_date = '2023-02'

    if airport == None or airport == []:
        df_new = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        df_new2 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        # df_new['Date'] = pd.to_datetime(df_new['Date'])
        # df_new['month_name'] = df_new['Date'].dt.strftime('%b')
        # df_new['year'] = df_new['Date'].dt.strftime('%Y')
        # df_new_sunburst = df_new.copy()
        # df_new_sunburst['year_number'] = df_new_sunburst['year'].astype(int)
        # df_new_sunburst = df_new_sunburst.groupby(['Airport','year_number','year','month_name']).sum().reset_index()

        df_new = df_new.groupby(['Airport','lat','lon']).sum().reset_index()
        df_new.sort_values(by=['passengers'], inplace=True, ascending=False)
        df_new2.sort_values(by=['Date','passengers'], inplace=True, ascending=False)

        fig = px.scatter_mapbox(df_new, lat="lat", lon="lon", hover_name="Airport",size="passengers",hover_data=["passengers"], zoom=4,
                                height=800,width=800, size_max=70, color_discrete_map={"passengers": "red"},
                                 color="Airport")
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        fig2 = px.scatter(df_new2, x="Date", y="passengers", color="Airport", hover_name="Airport", hover_data=["passengers"],
                          color_discrete_map={"passengers": "red"}, height=800)

        fig2.update_traces(mode='markers+lines')

        fig3 = px.bar(df_new, x="passengers", y="Airport", hover_name="Airport", hover_data=["passengers"],color="Airport", color_discrete_map={"passengers": "red"}, orientation='h',
                      height=900)

        # fig3 =px.sunburst(df_new_sunburst, path=['Airport','year','month_name'], values='passengers', color='Airport', color_discrete_map={"passengers": "red"}, height=1200, width=1200)
        # fig3.update_traces(maxdepth=2)
        #hide legend for fig3
        fig3.update_layout(showlegend=False),

        # update y-axis marker for fig3 to left



        # add padding to fig1
        fig.update_layout(
            margin=dict(
                l=50,
                r=0,
                b=0,
                t=50,
            ),
        )

        # add padding to fig2
        fig2.update_layout(
            margin=dict(
                l=0,
                r=50,
                b=0,
                t=50,
            ),
        )

        # add title to fig
        fig.update_layout(
            title_text="Airport Location",
            title_x=0.5,
            title_y=0.99,
            title_font_family="Arial",
            title_font_color="black",
            title_font_size=18,
            legend=dict(
                itemclick=False,
                itemdoubleclick=False,)
        ),
        fig2.update_layout(
            title_text=f'Monthly time series of passengers per airport for the selected period {start_date} to {end_date}',
            title_x=0.5,
            title_y=0.99,
            title_font_family="Arial",
            title_font_color="black",
            title_font_size=18,
            legend=dict(
                itemclick=False,
                itemdoubleclick=False, )
        ),
        fig3.update_layout(
            title_text=f'Number of passengers summed per airport for the selected period {start_date} to {end_date}',
            title_x=0.5,
            title_y=0.99,
            title_font_family="Arial",
            title_font_color="black",
            title_font_size=18,
        ),


        return fig, fig2,fig3
    else:
        df_new = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        df_new2 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        df_new = df_new.groupby(['Airport','lat','lon']).sum().reset_index()
        df_new.sort_values(by=['passengers'], inplace=True, ascending=False)
        df_new2.sort_values(by=['Date', 'passengers'], inplace=True, ascending=False)
        df_new = df_new[df_new['Airport'].isin(airport)]
        df_new2 = df_new2[df_new2['Airport'].isin(airport)]
        fig = px.scatter_mapbox(df_new, lat="lat", lon="lon", hover_name="Airport",size="passengers",hover_data=["passengers"], zoom=4,size_max=80,
                                height=800, color_discrete_map={"passengers": "red"},
                                 color="Airport")
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        fig2 = px.scatter(df_new2, x="Date", y="passengers", hover_name="Airport",
                          hover_data=["passengers"],color="Airport", color_discrete_map={"passengers": "red"})
        fig2.update_xaxes(rangeslider_visible=False, rangeselector=dict(buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward")])))

        fig2.update_traces(mode='markers+lines')

        fig3 = px.bar(df_new, x="passengers", y="Airport", hover_name="Airport", hover_data=["passengers"],
                      color="Airport", color_discrete_map={"passengers": "red"}, orientation='h',
                      height=800)
        fig3.update_traces(width=0.05)

        # hide legend for fig3
        fig3.update_layout(showlegend=False)

        # add padding to fig1
        fig.update_layout(
            margin=dict(
                l=50,
                r=0,
                b=0,
                t=50,
            ),
        )

        # add padding to fig2
        fig2.update_layout(
            margin=dict(
                l=0,
                r=50,
                b=0,
                t=50,
            ),
        )

        # add title to fig
        fig.update_layout(
            title_text="Airport Location",
            title_x=0.5,
            title_y=0.99,
            title_font_family="Arial",
            title_font_color="black",
            title_font_size=18,
            legend=dict(
                itemclick=False,
                itemdoubleclick=False, )
        ),
        fig2.update_layout(
            title_text=f'Monthly time series of passengers per airport for the selected period {start_date} to {end_date}',
            title_x=0.5,
            title_y=0.99,
            title_font_family="Arial",
            title_font_color="black",
            title_font_size=18,
            legend=dict(
                itemclick=False,
                itemdoubleclick=False, )
        ),
        fig3.update_layout(
            title_text=f'Number of passengers summed per airport for the selected period {start_date} to {end_date}',
            title_x=0.5,
            title_y=0.99,
            title_font_family="Arial",
            title_font_color="black",
            title_font_size=18,
        ),


        return fig, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)