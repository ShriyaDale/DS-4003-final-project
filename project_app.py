from dash import Dash, dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.graph_objects as go

#load the dataset
df = pd.read_csv('data.csv')

#initialize the Dash app
app = Dash(__name__, external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css'])

#define the minimum and maximum values for the calories range slider
min_value = df['calories'].min()
max_value = df['calories'].max()

#define the layout of the app
app.layout = html.Div([
    # header
    html.H1('Nutrition Dashboard', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': 30, 'color': 'white', 'backgroundColor': '#8BB174', 'padding': '50px'}),
    dcc.Markdown('''Choose a food item from the dropdown menu to see its nutritional information.''', style={'textAlign': 'center'}), 

    #dropdowns for restaurant selection and caloric range
    html.Div(className='row', style={'padding': '10px'}, children=[
        html.Div(className='col-sm-6', children=[ 
            html.H3('Select Restaurants', style={'textAlign': 'center', 'color': 'white', 'backgroundColor': '#426B69', 'padding': '10px', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='multiple-restaurant-dropdown',
                options=[{'label': restaurant, 'value': restaurant} for restaurant in df['restaurant'].unique()],
                multi=True, 
                value=["Select a restaurant..."],  
                style={'textAlign': 'center',
                       'color': 'black',
                       'backgroundColor': 'white'}, 
            )
        ]),
        html.Div(className='col-sm-6', children=[
            html.H3('Select Caloric Range', style={'textAlign': 'center', 'color': 'white', 'backgroundColor': '#426B69', 'padding': '10px', 'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='caloric-range-slider',
                min=df['calories'].min(),
                max=df['calories'].max(),
                marks={int(cal): str(cal) for cal in range(int(df['calories'].min()), int(df['calories'].max()) + 1, 50)},
                value=[df['calories'].min(), df['calories'].max()],
            )
        ])
    ]),
    
    #output display area for menu items
    html.Div(id='menu-items-output')
])

#callback to update the menu items based on user selection
@app.callback(
    Output('menu-items-output', 'children'),
    [Input('multiple-restaurant-dropdown', 'value'),
     Input('caloric-range-slider', 'value')]
)
def update_menu_items(selected_restaurants, selected_calories):
    if selected_restaurants and selected_calories:
        #filter the menu items based on selected restaurants and caloric range
        filtered_menu_items = df[(df['restaurant'].isin(selected_restaurants)) & 
                                 (df['calories'] >= selected_calories[0]) & 
                                 (df['calories'] <= selected_calories[1])]
        if filtered_menu_items.empty:
            #display a message if no menu items match the criteria
            return html.P("No menu items found for the selected criteria.")
        else:
            #create a Plotly table to display the filtered menu items
            table = go.Figure(data=[go.Table(
                header=dict(values=['Item Name', 'Calories'],
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[filtered_menu_items['item_name'], filtered_menu_items['calories']],
                           fill_color='lavender',
                           align='left'))
            ])
            table.update_layout(title="Menu Items Based on Your Selection",
                                width=500,  
                                margin=dict(l=20, r=20, t=50, b=20))  
            return dcc.Graph(figure=table)
    else:
        #prompt the user to make a selection if no criteria are chosen
        return html.P("Please select at least one restaurant and one caloric range.")


if __name__ == "__main__":
    app.run_server(debug=True)
