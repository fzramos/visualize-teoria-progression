import dash
import pandas as pd
import plotly.express as px
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer


def run_viz_app():
    # Get dataset and get sample
    df = pd.read_csv('./assets/historical_stats.csv',
                    parse_dates = ['Date/time']
                    )
    print(df.dtypes)
    # Preping Data

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
    app.layout = html.Div(children=[html.Div([
                                    html.H2('Interactive Scatter', 
                                        style={'textAlign':'center', 'color': '#F57241'}),
                                    html.Div([
                                        'Minimum Daily Exercise Count:',
                                        dcc.Input(
                                            id='input-min-1',
                                            type='number', 
                                            value=1),
                                        html.Br(),
                                        'Group by Day, Week, Month, or Year:',
                                        dcc.Dropdown(
                                            id='input-date-group-1', 
                                            options=[
                                                {'label': 'Day', 'value': 'D'},
                                                {'label': 'Week', 'value': 'W'},
                                                {'label': 'Month', 'value': 'M'},
                                                {'label': 'Year', 'value': 'Y'}
                                            ], 
                                            value='D')
                                    ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(dcc.Graph(id='scatter-1'))

    ])
    ], style={'textAlign': 'center',
                                'color': '#503D36',
                                'font-size': 40,})

    # TODO: User callback for filtering by exercise (need to have a drop down generated)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
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

        # For trendline, need X variable to by a normal nubmer, now doing days between
        # TODO: Make it (day/week/years) inbetween depending on drop down
        start_date = df_grouped['Date/time'].min()
        df_grouped['day_count'] = (df_grouped['Date/time'] - start_date).dt.days

        fig_scores = px.scatter(df_grouped, x='day_count', y='Total_Score', color = 'Options',
                                            title="Trend of Daily Scores", trendline='ols',trendline_color_override="green",
                                            template="plotly_dark")
        # fig_scores.layout.update(showlegend=False)


        fig_scores.update_layout(
            title="Musical Interval Practice Score Progression",
            xaxis_title=f"Time ({date_group})",
            yaxis_title="Percentage Correct",
            font = dict(
                    size=18
            )
        )
        return fig_total_score 

    # user input with scatter, group by DAY, WEEK, OR MONTH dropdown input
    Timer(1, open_browser).start()
    app.run_server()

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(8050))

if __name__ == '__main__':
    run_viz_app()