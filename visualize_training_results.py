import dash
import pandas as pd
import plotly.express as px
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

def run_viz_app():
    # Get dataset and get sample
    df = pd.read_csv('stats.csv',
                    parse_dates = ['Date/time']
                    )
    print(df.dtypes)
    # Preping Data

    # Exercise Sessions per day (meaningless)
    df_date = df.groupby([df['Date/time'].dt.date]).count()
    print(df_date.head())
    print(df_date.columns)

    fig_date = px.line(df_date, x=df_date.index, y='Exercise')

    # Individual exercises per day
    # df_date = df.groupby([df['Date/time'].dt.date], as_index=False)['Exercises'].sum()
    df_date2 = df.groupby([df['Date/time'].dt.date]).sum()
    print(df_date2.head())

    fig_date2 = px.line(df_date2, x=df_date.index, y='Exercises')
    
    # Raw Daily avg score
    df_avg_score = df.groupby([df['Date/time'].dt.date]).mean()

    fig_avg_score = px.line(df_avg_score, x=df_avg_score.index, y='Score')

    # Daily Total Score
    df_total_score = df.groupby([df['Date/time'].dt.date])[['Exercises', 'Correct']].sum()
    df_total_score['Total_Score'] = df_total_score['Correct']/df_total_score['Exercises']
    print(df_total_score.head())

    fig_total_score = px.line(df_total_score, x=df_avg_score.index, y='Total_Score')

    # Create a dash application
    app = dash.Dash(__name__)

    # Creating the layout and content for the application
    app.layout = html.Div(children=[html.H1('Teoria Training Progression Dashboard',
                                            style={'textAlign': 'center',
                                                    'color': '#503D36',
                                                    'font-size': 40}),
                                    html.P('Exercise Sessions per Day',
                                            style={'textAlign':'center', 'color': '#F57241'}),
                                    dcc.Graph(figure=fig_date),
                                    html.P('Individual Interval Exercises per Day',
                                            style={'textAlign':'center', 'color': '#F57241'}),
                                    dcc.Graph(figure=fig_date2),
                                    html.P('Exercise Session Daily Average Score',
                                            style={'textAlign':'center', 'color': '#F57241'}),
                                    dcc.Graph(figure=fig_avg_score),
                                    html.P('Combined Daily percent Correct',
                                            style={'textAlign':'center', 'color': '#F57241'}),
                                    dcc.Graph(figure=fig_total_score),


                                    ])

    # TODO: Add user callback to filter out days with less than some number of exercises
    #   this will get rid of small sample sice days so you see a more accurate progression
    # TODO: Add regression line including error areas to %Correct graphs
    # TODO: Auto open browser window 
    app.run_server()

# Run the application
# if __name__ == '__main__':
#     app.run_server()
if __name__ == '__main__':
    run_viz_app()