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


play_minutes = round(df["Elapsed time (minutes)"].sum())

# Create a dash application
app = dash.Dash(__name__)

# Creating the layout and content for the application
# TODO: Put titles inside of figures as very large
app.layout = html.Div(children=[

        html.H1('Teoria Training Progression Dashboard',
                style={'textAlign': 'center',
                        'color': 'white',
                        'font-size': 60}),
        html.H4(f'Total individual exercises completed: {df.Exercises.sum()}',
                style={'textAlign': 'center',
                        'color': '#00FF7F',
                        'font-size': 20}),
        html.H4(f'Total exercise time (hours:minutes): {play_minutes//60}:{play_minutes%60}',
                style={'textAlign': 'center',
                        'color': '#00FF7F',
                        'font-size': 20}),
        # html.H4(f'Average exercise time per day: {avg_daily_time} minutes',
        #         style={'textAlign': 'center',
        #                 'color': '#00FF7F',
        #                 'font-size': 20}),
        # html.P('Individual Interval Exercises per Day',
        #         style={'textAlign':'center', 'color': '#F57241'}),
        dcc.Graph(id='line-ex-per-day-1'),
        # html.P('Daily Exercise Time',
        #         style={'textAlign':'center', 'color': '#F57241'}),
        dcc.Graph(id='line-daily-time-2'),
        # html.P('Combined Daily percent Correct with Trendline',
        #         style={'textAlign':'center', 'color': '#F57241'}),
    html.Div([
        html.Div([
            html.Div([
                'Minimum exercises per time period: ',
                dcc.Input(
                    id='input-min-1',
                    type='number', 
                    value=1),
            ], style={
                'width': '48%', 
                'display': 'inline-block', 
                'font-size': 'large',
                'padding-top': '10px',
                'padding-bottom': '20px'
            }),

            html.Div([
                dcc.Dropdown(
                    id='input-date-group-1', 
                    options=[
                        {'label': 'Group by Day', 'value': 'D'},
                        {'label': 'Group by Week', 'value': 'W'},
                        {'label': 'Group by Month', 'value': 'M'},
                        {'label': 'Group by Year', 'value': 'Y'}
                    ], 
                    value='D',
                    style = {'color': 'black'}),         
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='scatter-1'),

    ], className='divInput')

        ],
        style={
                # 'textAlign': 'center',
                # 'color': '#503D36',
                # 'font-size': 40,
                'color': '#b9b9b9',
        })
        # style={'background-color' : '#cccaaa'})

# TODO: Add user callback to filter out days with less than some number of exercises
#   this will get rid of small sample sice days so you see a more accurate progression
# TODO: User callback for filtering by exercise (need to have a drop down generated)
# TODO: Add regression line including error areas to %Correct graphs
@app.callback(Output(component_id='line-ex-per-day-1', component_property='figure'))
def graph_ex_per_day(min_count, date_group):  
    print('trying')     
    #     df_date = df[['Date/time', 'Exercises', 'Correct', 'Options']].set_index('Date/time')
    df_date = df.groupby([df['Date/time'].dt.date]).sum()
    fig_per_day = px.line(df_date, x=df_date.index, y='Exercises', template="plotly_dark")


    # Group by Exercise Type, and date grouping (day, week, month, year)
#     df_grouped = df_date.groupby([pd.Grouper(freq=date_group), 'Options']).sum().reset_index()
    # Removing groups if they have a size smaller than user chosen cutoff
#     df_grouped = df_grouped[df_grouped['Exercises']>=min_count]
#     df_grouped['Total_Score'] = df_grouped['Correct']/df_grouped['Exercises'] * 100

#     start_date = df_grouped['Date/time'].min()
#     df_grouped['time_interval'] = (df_grouped['Date/time'] - start_date).dt.days

#     fig_scores = px.scatter(df_grouped, x='time_interval', y='Total_Score', color = 'Options',
#                                         title="Trend of Daily Scores", trendline='ols',
#                                         template="plotly_dark")

#     for i in range(len(fig_scores.data)):
#         if i%2==0:
#             fig_scores.data[i].name = str(int(i/2))
    fig_per_day.update_layout(
        title="Individual Interval Exercises per Day",
        xaxis_title=f"Days",
        yaxis_title="Individual Exercises",
        #legend_title_text='Exercise Types',
        #font = dict(
        #        size=18
        #)
    )
    return fig_per_day 

# @app.callback([
#         Output(component_id='line-daily-time-2', component_property='figure'),
#         Output(component_id='avg-daily-time', component_property='value'),
# ])
@app.callback(Output(component_id='line-daily-time-2', component_property='figure'))
def graph_daily_time(min_count, date_group):       
    df_daily_time = df.groupby([df['Date/time'].dt.date])[['Elapsed time (minutes)']].sum()
    avg_daily_time = round(df_daily_time['Elapsed time (minutes)'].mean())
    fig_daily_time = px.line(df_daily_time, x=df_daily_time.index, y='Elapsed time (minutes)', template="plotly_dark")
    fig_daily_time.update_layout(
        title="Training Time per Day",
        xaxis_title=f"Days",
        yaxis_title="Elasped time (minutes)",
    )
    return [fig_daily_time, avg_daily_time]
#     return [fig_daily_time, avg_daily_time]

####################
# TODO: Make this graph more useful (daily total score is more useful than this graph)
# Raw Daily avg score




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