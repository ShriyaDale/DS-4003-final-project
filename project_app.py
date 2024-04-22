from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#load the dataset
df = pd.read_csv('data.csv')

#initialize the Dash app w/ server
app = Dash(__name__, external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css'])
server = app.server

#define the minimum and maximum values for the nutrient range sliders/constant values for future callbacks
min_protein = df['protein'].min()
max_protein = df['protein'].max()
min_carbs = df['carbohydrates'].min()
max_carbs = df['carbohydrates'].max()
min_fats = df['total_fat'].min()
max_fats = df['total_fat'].max()
min_calories = df['calories'].min()
max_calories = df['calories'].max()
#standard values for the pie chart (shown below)
standard_protein = 50
standard_carbs = 300
standard_fat = 65

#layout with components
app.layout = html.Div(children=[
    #header
    html.Div([
        html.H1('Foods from American Restaurants Classified through Nutritional Value', className='title is-1 has-text-centered', style={'font': 'Helvetica','color': 'white', 'backgroundColor': '#8BB174', 'padding': '20px'}),
    ], style={'marginBottom': '20px'}),
    #dashboard introduction
    html.Div([
        html.Div([
            html.H3([html.Strong('Dashboard Introduction')], className='card-title1'),
            html.P("This dashboard allows you to explore the nutritional makeup of menu items from various American restaurants. Customize your analysis by filtering items based on your dietary preferences and requirements. The visualizations provide insights into nutrient distribution, aiding in informed decision-making for healthier eating habits. Discover and compare the nutritional value of restaurant offerings to support your dietary goals.", className='card-text', style={'padding': '5px 0'})
        ], className='card border-primary mb-3', style={'text-align':'justify', 'padding': '20px'})
    ], className='container'),
    #dropdowns
    html.Div([
        html.Div([
            html.Div([
                html.Label('Select Restaurants', className='label has-text-white has-background-dark is-rounded has-text-centered', style={'fontWeight': 'bold', 'padding': '10px'}),
                dcc.Dropdown(
                    id='multiple-restaurant-dropdown',
                    options=[{'label': restaurant, 'value': restaurant} for restaurant in df['restaurant'].unique()],
                    multi=True,
                    value=[],
                ),
            ], className='box is-rounded'),
            html.Div([
                html.Label('Search', className='label has-text-white has-background-dark is-rounded has-text-centered', style={'fontWeight': 'bold', 'padding': '10px'}),
                dcc.Input(
                    id='search-input',
                    type='text',
                    placeholder='Search items...',
                    debounce=True,
                ),
            ], className='box is-rounded'),
        ], className='column is-one-fifth'),
        html.Div([
            html.Div([
                html.Label('Select Protein Range (g)', className='label has-text-white has-background-dark is-rounded has-text-centered', style={'fontWeight': 'bold', 'padding': '10px'}),
                dcc.RangeSlider(
                    id='protein-range-slider',
                    min=min_protein,
                    max=max_protein,
                    marks={int(pro): str(pro) for pro in range(int(min_protein), int(max_protein) + 1, 10)},
                    value=[min_protein, max_protein],
                ),
            ], className='box is-rounded'),
        ], className='column is-one-fifth'),
        html.Div([
            html.Div([
                html.Label('Select Carbs Range (g)', className='label has-text-white has-background-dark is-rounded has-text-centered', style={'fontWeight': 'bold', 'padding': '10px'}),
                dcc.RangeSlider(
                    id='carbs-range-slider',
                    min=min_carbs,
                    max=max_carbs,
                    marks={int(carb): str(carb) for carb in range(int(min_carbs), int(max_carbs) + 1, 20)},
                    value=[min_carbs, max_carbs],
                ),
            ], className='box is-rounded'),
        ], className='column is-one-fifth'),
        html.Div([
            html.Div([
                html.Label('Select Fats Range (g)', className='label has-text-white has-background-dark is-rounded has-text-centered', style={'fontWeight': 'bold', 'padding': '10px'}),
                dcc.RangeSlider(
                    id='fats-range-slider',
                    min=min_fats,
                    max=max_fats,
                    marks={int(fat): str(fat) for fat in range(int(min_fats), int(max_fats) + 1, 10)},
                    value=[min_fats, max_fats],
                ),
            ], className='box is-rounded'),
        ], className='column is-one-fifth'),
        html.Div([
            html.Div([
                html.Label('Select Caloric Range', className='label has-text-white has-background-dark is-rounded has-text-centered', style={'fontWeight': 'bold', 'padding': '10px'}),
                dcc.RangeSlider(
                    id='caloric-range-slider',
                    min=min_calories,
                    max=max_calories,
                    marks={int(cal): str(cal) for cal in range(int(min_calories), int(max_calories) + 1, 200)},
                    value=[min_calories, max_calories],
                ),
            ], className='box is-rounded'),
        ], className='column is-one-fifth'),
    ], className='columns', style={'marginBottom': '20px', 'margin': '20px'}),
    
    #visualizations
    html.Div([
    html.Div(id='menu-items-output', className='column is-one-half', style={'paddingRight': '20px'}), #table layout
    html.Div([ #graphs layout
        dcc.Graph(id='scatter-plot', className='col-lg-6 col-md-6 col-sm-12', style={'width': '100%', 'height': '100%', 'marginBottom': '15px'}),
        dcc.Graph(id='pie-chart', className='col-lg-6 col-md-6 col-sm-12', style={'width': '100%', 'height': '100%'}),
        html.P('The default values for these are the recommended macronutrient values for a 2000 calorie diet. When selected, the pie chart shows the average macronutrient composition of the selected items from each restaurant.'),
    ], className='column', style={'display': 'flex', 'flexDirection': 'column', 'width': '100%', 'height': '100%', 'overflowX': 'auto','marginRight': '40px'})
], className='columns'),
    #dashboard footer with link to github + project background
    html.Div([
        html.Footer([ 
        html.P([html.Strong('Dataset Provenance')]),
        html.P("The dataset is sourced from MenuStat and serves as a valuable resource for researchers, policymakers, and health professionals interested in restaurant food nutrition. Developed by the New York City Department of Health and Mental Hygiene and now managed by Harvard Pilgrim Health Care Institute, MenuStat aims to provide comprehensive insights into restaurant food nutrition. This dataset holds significant relevance due to the pivotal role that out-of-home dining plays in shaping the American diet. Studies have shown that meals consumed away from home contribute substantially to daily caloric intake, constituting approximately one-third of total calories consumed, and represent nearly half of an average household's food expenditure. My interest lies in delving deep into the diverse spectrum of nutrients present in these restaurant offerings and exploring how they contribute to overall dietary patterns."),
        html.P(" "),
        html.P('This dashboard was created by Shriya Dale for DS 4003.'),
        html.P(['See the GitHub repository with all work for this project ',html.A('here', 
            href='https://github.com/ShriyaDale/DS-4003_SD/tree/main', className='text-success'),'.'])
            ], className='row text-light bg-dark p-4', style={'text-align':'center', 'backgroundColor': '#8BB174'})
        ], className='container-fluid')
    ], style={'backgroundColor': '#C1E1C1'}
)
#callbacks for menu tables
@app.callback(
    Output('menu-items-output', 'children'),
    [Input('multiple-restaurant-dropdown', 'value'),
     Input('protein-range-slider', 'value'),
     Input('carbs-range-slider', 'value'),
     Input('fats-range-slider', 'value'),
     Input('caloric-range-slider', 'value'),
     Input('search-input', 'value')]
)
def update_menu_items(selected_restaurants, selected_protein, selected_carbs, selected_fats, selected_calories, search_value):
    if selected_restaurants and selected_protein and selected_carbs and selected_fats and selected_calories:
        filtered_menu_items = df[(df['restaurant'].isin(selected_restaurants)) &
                                 (df['protein'] >= selected_protein[0]) & (df['protein'] <= selected_protein[1]) &
                                 (df['carbohydrates'] >= selected_carbs[0]) & (df['carbohydrates'] <= selected_carbs[1]) &
                                 (df['total_fat'] >= selected_fats[0]) & (df['total_fat'] <= selected_fats[1]) &
                                 (df['calories'] >= selected_calories[0]) & (df['calories'] <= selected_calories[1])]

        if search_value:
            filtered_menu_items = filtered_menu_items[filtered_menu_items['item_name'].str.contains(search_value, case=False)]

        if filtered_menu_items.empty:
            return [html.Div(html.P("No menu items found for the selected criteria.", className='has-text-centered'), className='column is-full')]
        else:
            filtered_menu_items = filtered_menu_items.sort_values(by='calories')
            grouped_menu_items = filtered_menu_items.groupby('restaurant')
            restaurant_outputs = []

            for restaurant, items in grouped_menu_items:
                table = go.Figure(data=[go.Table(
                    header=dict(values=['Item Name', 'Protein (g)', 'Carbs (g)', 'Fats (g)', 'Calories'],
                                fill_color='#426B69',
                                font=dict(color='white'),
                                align='left'),
                    cells=dict(values=[items['item_name'], items['protein'], items['carbohydrates'], items['total_fat'], items['calories']],
                               fill_color='lavender',
                               align='left'))
                ])
                table.update_layout(title=restaurant,
                                    width=700,
                                    height=500,
                                    margin=dict(l=20, r=20, t=30, b=20),
                                    hovermode='closest')
                restaurant_outputs.append(html.Div(dcc.Graph(figure=table), className='column is-qu'))
            return restaurant_outputs
    else:
        return [html.Div(html.P("Please select at least one restaurant and one nutrient/caloric range.", className='has-text-centered'), className='column is-full')]
#callback to update the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('multiple-restaurant-dropdown', 'value'),
     Input('search-input', 'value'),
     Input('protein-range-slider', 'value'),
     Input('carbs-range-slider', 'value'),
     Input('fats-range-slider', 'value'),
     Input('caloric-range-slider', 'value')]
)
def update_scatter_plot(restaurants, search_input, protein_range, carbs_range, fats_range, caloric_range):
    filtered_df = df[df['restaurant'].isin(restaurants)]
    if search_input:
        filtered_df = filtered_df[filtered_df['item_name'].str.contains(search_input, case=False)]
    filtered_df = filtered_df[(filtered_df['protein'] >= protein_range[0]) & (filtered_df['protein'] <= protein_range[1])]
    filtered_df = filtered_df[(filtered_df['carbohydrates'] >= carbs_range[0]) & (filtered_df['carbohydrates'] <= carbs_range[1])]
    filtered_df = filtered_df[(filtered_df['total_fat'] >= fats_range[0]) & (filtered_df['total_fat'] <= fats_range[1])]
    filtered_df = filtered_df[(filtered_df['calories'] >= caloric_range[0]) & (filtered_df['calories'] <= caloric_range[1])]
    fig = px.scatter(filtered_df, x='protein', y='carbohydrates', color='calories', title = 'Protein vs. Carbohydrates')
    fig.update_layout(
        xaxis_title='Protein (g)',
        yaxis_title='Carbs (g)',
    )
    return fig

#callback to update the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('multiple-restaurant-dropdown', 'value'),
     Input('search-input', 'value'),
     Input('protein-range-slider', 'value'),
     Input('carbs-range-slider', 'value'),
     Input('fats-range-slider', 'value'),
     Input('caloric-range-slider', 'value')]
)
def update_pie_chart(restaurants, search_input, protein_range, carbs_range, fats_range, caloric_range):
    filtered_df = df[df['restaurant'].isin(restaurants)]
    if search_input:
        filtered_df = filtered_df[filtered_df['item_name'].str.contains(search_input, case=False)]
    filtered_df = filtered_df[(filtered_df['protein'] >= protein_range[0]) & (filtered_df['protein'] <= protein_range[1])]
    filtered_df = filtered_df[(filtered_df['carbohydrates'] >= carbs_range[0]) & (filtered_df['carbohydrates'] <= carbs_range[1])]
    filtered_df = filtered_df[(filtered_df['total_fat'] >= fats_range[0]) & (filtered_df['total_fat'] <= fats_range[1])]
    filtered_df = filtered_df[(filtered_df['calories'] >= caloric_range[0]) & (filtered_df['calories'] <= caloric_range[1])]
    avg_protein = filtered_df['protein'].mean()
    avg_carbs = filtered_df['carbohydrates'].mean()
    avg_fat = filtered_df['total_fat'].mean()
    nutrient_data = {
        'Nutrient': ['Protein', 'Carbohydrates', 'Total Fat', 'Standard Protein', 'Standard Carbs', 'Standard Fat'],
        'Value': [avg_protein, avg_carbs, avg_fat, standard_protein, standard_carbs, standard_fat]
    }
    fig = px.pie(nutrient_data, values='Value', names='Nutrient', title='Marco Composition for Selected Restaurants', hole=0.3)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        hovermode='closest'
    )
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=False)
