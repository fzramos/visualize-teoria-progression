from cProfile import run
import dash
import pandas as pd
import plotly.express as px
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer
import plotly.express as px


# Get dataset and get sample
df = pd.read_csv('./assets/historical_stats.csv',
                parse_dates = ['Date/time']
                )


play_minutes = round(df["Elapsed time (minutes)"].sum())

#########
df_date = df.groupby([df['Date/time'].dt.date]).sum()
fig_per_day = px.line(df_date, x=df_date.index, y='Exercises', template="plotly_dark")
fig_per_day.update_layout(
    title="Individual Interval Exercises per Day",
    xaxis_title=f"Days",
    yaxis_title="Individual Exercises",
    legend_title_text='Exercise Types',
    font = dict(
        size=18
    )
)
######
df_daily_time = df.groupby([df['Date/time'].dt.date])[['Elapsed time (minutes)']].sum()
avg_daily_time = round(df_daily_time['Elapsed time (minutes)'].mean())
fig_daily_time = px.line(df_daily_time, x=df_daily_time.index, y='Elapsed time (minutes)', template="plotly_dark")
fig_daily_time.update_layout(
    title="Training Time per Day",
    xaxis_title=f"Days",
    yaxis_title="Elasped time (minutes)",
    font = dict(
        size=18
    )    
)
###
# Create a dash application
app = dash.Dash(__name__)

# Creating the layout and content for the application
app.layout = html.Div([
    html.H1('Teoria Training Progression Dashboard',
        style={'textAlign': 'center',
                'color': 'white',
                'font-size': 60}),
    html.Div([
        html.P(f'Total individual exercises completed: {df.Exercises.sum()}'),
        html.P(f'Total exercise time (hours:minutes): {play_minutes//60}:{play_minutes%60}'),
        html.P(f'Average exercise time per day: {avg_daily_time} minutes'),        
    ], className='container'
    # ,style={
    #     'margin': 'auto'
    # }
    ),
    html.Br(),
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

    ], className='divInput'),
    html.Br(),
    dcc.Graph(figure=fig_per_day),
    html.Br(),
    dcc.Graph(figure=fig_daily_time),
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

def run_viz_app():
    Timer(1, open_browser).start()
    app.run_server()

if __name__ == '__main__':
    run_viz_app()