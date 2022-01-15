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

# Preping Data


# Exercise Sessions per day (meaningless)
df_date = df.groupby([df['Date/time'].dt.date]).count()


fig_date = px.line(df_date, x=df_date.index, y='Exercise', template="plotly_dark")

# Time
play_minutes = round(df["Elapsed time (minutes)"].sum())

# Individual exercises per day
df_date2 = df.groupby([df['Date/time'].dt.date]).sum()
print(df_date2.head())

fig_date2 = px.line(df_date2, x=df_date.index, y='Exercises', template="plotly_dark")

# TODO: Make this graph more useful (daily total score is more useful than this graph)
# Raw Daily avg score
df_daily_time = df.groupby([df['Date/time'].dt.date])[['Elapsed time (minutes)']].sum()
avg_daily_time = round(df_daily_time['Elapsed time (minutes)'].mean())
fig_daily_time = px.line(df_daily_time, x=df_daily_time.index, y='Elapsed time (minutes)', template="plotly_dark")

# Daily Total Score
df_total_score = df.groupby([df['Date/time'].dt.date, 'Options'])[['Exercises', 'Correct']].sum()
df_total_score = df_total_score.reset_index()
df_total_score['Total_Score'] = df_total_score['Correct']/df_total_score['Exercises']*100

fig_total_score = px.line(df_total_score, x='Date/time', y='Total_Score', color='Options', template="plotly_dark")
fig_total_score.layout.update(showlegend=False)
# Daily Total Score with trend line
# for regression line, you need 
# TODO: Change axes titles
start_date = df['Date/time'].dt.date.min()
print(start_date)
print(df_total_score['Date/time'])
df_total_score['day_count'] = (df_total_score['Date/time'] - start_date).dt.days
print(df_total_score['day_count'])
fig_total_score_trend = px.scatter(df_total_score, x='day_count', y='Total_Score', color = 'Options',
                                title="Trend of Daily Scores", trendline='ols',trendline_color_override="green",
                                template="plotly_dark")
fig_total_score_trend.layout.update(showlegend=False)
fit_result = px.get_trendline_results(fig_total_score_trend).px_fit_results.iloc[0]
r2 = fit_result.rsquared
slope = fit_result.params[1]
intercept = fit_result.params[0]
# TODO: Make sure separate trendlines for different Options
print(px.get_trendline_results(fig_total_score_trend).px_fit_results.iloc[0])
fig_total_score_trend.add_annotation(x=1, y=50,
        text=f"R^2 = {r2}",
        showarrow=False,
        font=dict(
        # family="Courier New, monospace",
        size=18,
        # color="#7f7f7f"
)
        )
fig_total_score_trend.add_annotation(x=1, y=43,
        text=f"Y = {slope}*x + {intercept}",
        showarrow=False,
        font=dict(
        size=18
        )
        )

# TODO: add this to all graphs
fig_total_score_trend.update_layout(
        title="Title",
        xaxis_title="X Axis Title",
        yaxis_title="Y Axis title",
        font = dict(
                size=18
        )
)

# Create a dash application
app = dash.Dash(__name__)

# Creating the layout and content for the application
# TODO: Put titles inside of figures as very large
app.layout = html.Div(children=[html.H1('Teoria Training Progression Dashboard',
                                        style={'textAlign': 'center',
                                                'color': 'white',
                                                'font-size': 60}),
                                html.H2(f'Total individual exercises completed: {df.Exercises.sum()}',
                                        style={'textAlign': 'center',
                                                'color': '#00FF7F',
                                                'font-size': 40}),
                                html.H2(f'Total exercise time (hours:minutes): {play_minutes//60}:{play_minutes%60}',
                                        style={'textAlign': 'center',
                                                'color': '#00FF7F',
                                                'font-size': 40}),
                                html.H2(f'Average exercise time per day: {avg_daily_time} minutes',
                                        style={'textAlign': 'center',
                                                'color': '#00FF7F',
                                                'font-size': 40}),
                                html.P('Exercise Sessions per Day',
                                        style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig_date),
                                html.P('Individual Interval Exercises per Day',
                                        style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig_date2),
                                html.P('Daily Exercise Time',
                                        style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig_daily_time),
                                html.P('Combined Daily percent Correct',
                                        style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig_total_score),
                                html.P('Combined Daily percent Correct with Trendline',
                                        style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig_total_score_trend),


                                ],
                style={'textAlign': 'center',
                        'color': '#503D36',
                        'font-size': 40,})
        # style={'background-color' : '#cccaaa'})

# TODO: Add user callback to filter out days with less than some number of exercises
#   this will get rid of small sample sice days so you see a more accurate progression
# TODO: User callback for filtering by exercise (need to have a drop down generated)
# TODO: Add regression line including error areas to %Correct graphs


def open_browser():
	webbrowser.open_new("http://localhost:{}".format(8050))

if __name__ == '__main__':
        Timer(1, open_browser).start()
        app.run_server()