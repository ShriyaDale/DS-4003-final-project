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
ideal_protein_intake = 50
ideal_carbs_intake = 300
ideal_fats_intake = 65

#layout w/ components
app.layout = html.Div(children=[
    #header
    html.Div([
        html.H1('Foods from American Restaurants Classified through Nutritional Value', className='title is-1 has-text-centered', style={'font': 'Helvetica','color': 'white', 'backgroundColor': '#8BB174', 'padding': '20px'}),
    ], style={'marginBottom': '20px'}),
    #instructions
    html.Div([
        html.Div([
            html.H3([html.Strong('Instructions')], className='card-title'),
            html.P('Welcome to the Nutrition Dashboard! Use the selector widgets below to customize your analysis.'),
            html.P([
                html.Strong('1. '), 'Choose one or more restaurants from the dropdown menu to filter the data.'
            ], className='card-text', style={'padding': '5px 0'}),
            html.P([
                html.Strong('2. '), 'Use the search bar to find specific food items within the selected restaurants.'
            ], className='card-text', style={'padding': '5px 0'}),
            html.P([
                html.Strong('3. '), 'Adjust the sliders to select the desired range of protein, carbs, fats, and calories.'
            ], className='card-text', style={'padding': '5px 0'}),
            html.P([
                html.Strong('4. '), 'Explore the nutritional information of the filtered items in the table on the left side.'
            ], className='card-text', style={'padding': '5px 0'}),
            html.P([
                html.Strong('5. '), 'FINISH adding directions here.'
            ], className='card-text', style={'padding': '5px 0'})
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
        ], className='column is-one-quarter'),
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
        ], className='column is-one-quarter'),
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
        ], className='column is-one-quarter'),
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
        ], className='column is-one-quarter'),
        html.Div([
            html.Div([
                html.Label('Select Caloric Range', className='label has-text-white has-background-dark is-rounded has-text-centered', style={'fontWeight': 'bold', 'padding': '10px'}),
                dcc.RangeSlider(
                    id='caloric-range-slider',
                    min=min_calories,
                    max=max_calories,
                    marks={int(cal): str(cal) for cal in range(int(min_calories), int(max_calories) + 1, 50)},
                    value=[min_calories, max_calories],
                ),
            ], className='box is-rounded'),
        ], className='column is-one-quarter'),
    ], className='columns', style={'marginBottom': '20px'}),
    
    #visualizations
    html.Div([
    html.Div(id='menu-items-output', className='column is-two-thirds', style={'paddingRight': '20px'}),
    html.Div([
        dcc.Graph(id='scatter-plot', className='column', style={'width': '100%', 'height': '100%'}),
        dcc.Graph(id='pie-chart', className='column', style={'width': '100%', 'height': '100%'}),
        html.P('The default values for these are the recommended values for a 2000 calorie diet. When selected, the pie chart shows the average nutrient composition of the selected items.'),
    ], className='column', style={'display': 'flex', 'flexDirection': 'column', 'width': '100%', 'height': '100%'})
], className='columns'),

    html.Div([
        html.Footer([ 
        html.P('This dashboard was created by Shriya Dale for DS 4003.'),
        html.P(['See the GitHub repository with all work for this project ',html.A('here', 
            href='https://github.com/ShriyaDale/DS-4003_SD/tree/main', className='text-success'),'.'])
            ], className='row text-light bg-dark p-4', style={'text-align':'center', 'backgroundColor': '#8BB174'})
        ], className='container-fluid')
    ], style={'margin': '20px', 'backgroundColor': '#0F0F0F0'}
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
        filtered_df = filtered_df[filtered_df['food_item'].str.contains(search_input, case=False)]
    filtered_df = filtered_df[(filtered_df['protein'] >= protein_range[0]) & (filtered_df['protein'] <= protein_range[1])]
    filtered_df = filtered_df[(filtered_df['carbohydrates'] >= carbs_range[0]) & (filtered_df['carbohydrates'] <= carbs_range[1])]
    filtered_df = filtered_df[(filtered_df['total_fat'] >= fats_range[0]) & (filtered_df['total_fat'] <= fats_range[1])]
    filtered_df = filtered_df[(filtered_df['calories'] >= caloric_range[0]) & (filtered_df['calories'] <= caloric_range[1])]
    fig = px.scatter(filtered_df, x='protein', y='carbohydrates', color='calories', title = 'Protein vs. Carbs')
    fig.update_layout(
        xaxis_title='Protein (g)',
        yaxis_title='Carbs (g)',
    )
    return fig

# Standard values for comparison
standard_protein = 50
standard_carbs = 300
standard_fat = 65

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
        filtered_df = filtered_df[filtered_df['food_item'].str.contains(search_input, case=False)]
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
    fig = px.pie(nutrient_data, values='Value', names='Nutrient', title='Average Nutrient Composition of Selected Restaurant(s)', hole=0.3)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode='closest'
    )
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=False)
