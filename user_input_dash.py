import dash
import pandas as pd
import plotly.express as px
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer

# Get dataset and get sample
df = pd.read_csv('./assets/historical_stats.csv',
                parse_dates = ['Date/time']
                )

# Create a dash application
app = dash.Dash(__name__)

# Creating the layout and content for the application
app.layout = html.Div(children=[html.Div([
                                html.H1('Interactive Scatter', 
                                    style={'textAlign':'center', 'color': '#F57241'}),
                                html.Div(children=[
                                    html.Div(children=[
                                        'Minimum exercises per time period: ',
                                        dcc.Input(
                                            id='input-min-1',
                                            type='number', 
                                            value=1),
                                        ]
                                        # , style={
                                        #     'font-size': 30,
                                        #     'height':'35px',
                                        #     'font-size':'30'},
                                    ),
                                    html.Div(children=[
                                        'Group by Day, Week, Month, or Year:',
                                        dcc.Dropdown(
                                            id='input-date-group-1', 
                                            options=[
                                                {'label': 'Day', 'value': 'D'},
                                                {'label': 'Week', 'value': 'W'},
                                                {'label': 'Month', 'value': 'M'},
                                                {'label': 'Year', 'value': 'Y'}
                                            ], 
                                            value='D',
                                            style = {'color': 'black'}),
                                            
                                        ],
                                        style = {
                                            'font-size': '40',
                                            "width": "30%"
                                        }                                  
                                    ),
                                    html.Br(),
                                    html.Div(dcc.Graph(id='scatter-1'))
                                ], className='divInput')
                            ]),

], 
style={
    'color': '#b9b9b9',
})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
@app.callback(Output(component_id='scatter-1', component_property='figure'), [
                Input(component_id='input-min-1', component_property='value'),
                Input(component_id='input-date-group-1', component_property='value')
])
def graph_scatter_w_min(min_count, date_group):       
    df_date = df[['Date/time', 'Exercises', 'Correct', 'Options']].set_index('Date/time')
    # Group by Exercise Type, and date grouping (day, week, month, year)
    df_grouped = df_date.groupby([pd.Grouper(freq=date_group), 'Options']).sum().reset_index()
    # Removing groups if they have a size smaller than user chosen cutoff
    df_grouped = df_grouped[df_grouped['Exercises']>=min_count]
    df_grouped['Total_Score'] = df_grouped['Correct']/df_grouped['Exercises'] * 100

    start_date = df_grouped['Date/time'].min()
    df_grouped['time_interval'] = (df_grouped['Date/time'] - start_date).dt.days

    fig_scores = px.scatter(df_grouped, x='time_interval', y='Total_Score', color = 'Options',
                                        title="Trend of Daily Scores", trendline='ols',
                                        template="plotly_dark")

    for i in range(len(fig_scores.data)):
        if i%2==0:
            fig_scores.data[i].name = str(int(i/2))
    fig_scores.update_layout(
        title="Musical Interval Practice Score Progression",
        xaxis_title=f"Days",
        yaxis_title="Percentage Correct",
        legend_title_text='Exercise Types',
        font = dict(
                size=18
        )
    )
    return fig_scores 

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(8050))

if __name__ == '__main__':
    # Timer(1, open_browser).start()
    app.run_server()