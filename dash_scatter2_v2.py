# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 11:00:12 2018

@author: sburns2
"""



import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
app = dash.Dash()
app.scripts.config.serve_locally=True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/dZVMbK.css"})

team2 = "Yeovil"
ind3 = "Yeovil"
df3 = pd.read_pickle("df_"+team2+".pkl") 
filepath = "./CSV_data/League2/E3.csv"
filepathPL = "./CSV_data/PremierLeague/E0.csv"

df_full = pd.read_csv(filepath)
available_teams = df_full["HomeTeam"].unique()
df_fullPL = pd.read_csv(filepathPL)
available_teamsPL = df_fullPL["HomeTeam"].unique()
all_options = {'League2': available_teams,
               'PremierLeague': available_teamsPL        
        }

print(available_teams)

def generate_table(dataframe, max_rows=50):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
    
#index  = 'Yeo'
app.layout = html.Div([
        html.Div([
                html.H1('Team analytics'),
                html.H3('Histogram Crossfiltering Selections'),
                
                #html.Hr(),
                html.Label('League'),
                dcc.Dropdown(
                        id = 'league',
                        options=[{'label': i, 'value': i} for i in all_options.keys()],
                        style = {'width' : '50%','display':'inline-block'},                        
                        value  = 'League2'),
                        
                html.Label('Team'),        
                dcc.Dropdown(id = 'team',
                             style = {'width' : '50%','display':'inline-block'},
                             ),
                html.Hr(),
                html.Div(id = 'display selected value'),
                
                            
                dcc.RadioItems(
                        id='bin2',
                        options=[{'label': i, 'value': i} for i in ['Home Corner', 'Opp_C','Home HT Goals','SH_home_G','Home FT Goals','HT_Opp_G','SH_Opp_G','FT_Opp_G']],
                        #options=[{'label': i, 'value': i} for i in [''+team+'C', 'HT'+team+'G', 'FT'+team+'G', 'Opp_C']],
                        value='Home Corner',
                        labelStyle={'display': 'inline'}
                 ),
                html.Div([
                html.Div(
                className='five columns',
                children=dcc.Graph(id='fig1')
                     )  
                ]),
                html.Div([
                html.Div(
                className='five columns',
                children=dcc.Graph(id='fig2')
                     )  
                ])
        ]),
                
           
        html.Div(
                className='nine columns',
                children=[
        #html.H4(children=ind3),
        
        html.Div(id =  'table'),
        
        #generate_table(df3)   
        ])                  
])
       


@app.callback(

    dash.dependencies.Output('team', 'options'),

    [dash.dependencies.Input('league', 'value')])

def set_team_option(selected_team):

    return [{'label': i, 'value': i} for i in all_options[selected_team]]

 

@app.callback(

    dash.dependencies.Output('team', 'value'),

    [dash.dependencies.Input('league', 'options')])

def set_leaugue_value(available_options):

    return available_options[0]['value']   
@app.callback(
    dash.dependencies.Output('fig1', 'figure'),
    [dash.dependencies.Input('bin2', 'value'),
     dash.dependencies.Input('team', 'value'),
     dash.dependencies.Input('league', 'value')])
def display_stores_over_time(bin2,team,league):
    #team = "Yeovil"
    df2 = pd.read_pickle("./CSV_data/"+league+"/df_"+team+".pkl") 
    parsed = list(team)
    a = [parsed[0],parsed[1],parsed[2]]
    team_par = ''.join(a)
    if bin2 == 'Home Corner':
        val = ''+team_par+'C'
        val2 = ''+team+' Corners'
    elif bin2 == 'Opp_C':
        val = 'Opp_C'
        val2 = 'Opposition Corners'
    elif bin2 == 'Home HT Goals':
        val = 'HT'+team_par+'G'
        val2 = 'HT '+team+' Goals'
        
    elif bin2 == 'Home FT Goals':
        val = 'FT'+team_par+'G'    
        val2 = 'FT '+team+' Goals'  
    elif bin2 == 'SH_home_G':
         val = 'SH'+team_par+'G'    
         val2 = 'SH '+team+' Goals'  
    elif bin2 =='SH_Opp_G':
         val = 'SH_Opp_G'
         val2 = 'Second half opposition Goals'   
    elif bin2 == 'HT_Opp_G':
         val = 'HT_Opp_G'
         val2 = 'Half time opposition Goals'
    elif bin2 == 'FT_Opp_G':
         val = 'FT_Opp_G'
         val2 = 'Full time opposition Goals'
     
    #'HT_Opp_G','SH_Opp_G','FT_Opp_G'    
    return {
        'data': [
            {
                   
                'x': df2[val], #ind  = "Yeovil"df2 = pd.read_pickle("df_"+ind+".pkl")    
                #'customdata': df['storenum'],
                'name': 'Open Date',
                'type': 'histogram',
                'autobinx': False,
                
                'xbins': {
                    'start': 0,
                    'end': 10,
                    'size': (
                        'M18' if bin2 == 'Home Corner' else
                        'M1' if bin2 == 'Opp_C' else
                        'M1' if bin2 == 'Home FT Goals' else 
                        'M1'                       
                      
                    )
                }
            }
        ],
    'layout': go.Layout(
            
              xaxis={
                'title': val2,
                #'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
      
    }
@app.callback(
    dash.dependencies.Output('fig2', 'figure'),
    [dash.dependencies.Input('bin2', 'value'),
     dash.dependencies.Input('team', 'value'),
     dash.dependencies.Input('league', 'value')])
def display_stores_over_time2(bin2,team,league):
    #team = "Yeovil"
    df2 = pd.read_pickle("./CSV_data/"+league+"/df_"+team+".pkl") 
    parsed = list(team)
    a = [parsed[0],parsed[1],parsed[2]]
    team_par = ''.join(a)
    if bin2 == 'Home Corner':
        val = ''+team_par+'C'
        val2 = ''+team+' Corners'
    elif bin2 == 'Opp_C':
        val = 'Opp_C'
        val2 = 'Opposition Corners'
    elif bin2 == 'Home HT Goals':
        val = 'HT'+team_par+'G'
        val2 = 'HT '+team+' Goals'
        
    elif bin2 == 'Home FT Goals':
        val = 'FT'+team_par+'G'    
        val2 = 'FT '+team+' Goals'    
    elif bin2 == 'SH_home_G':
         val = 'SH'+team_par+'G'    
         val2 = 'SH '+team+' Goals'  
    elif bin2 =='SH_Opp_G':
         val = 'SH_Opp_G'
         val2 = 'Second half opposition Goals'          
    elif bin2 == 'HT_Opp_G':
         val = 'HT_Opp_G'
         val2 = 'Half time opposition Goals'
    elif bin2 == 'FT_Opp_G':
         val = 'FT_Opp_G'
         val2 = 'Full time opposition Goals'
        
        
    return {
        'data': [go.Scatter(
            x=df2['Date'],
            y=df2[val],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': "Date",
                #'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': val2,
                #'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'

})
@app.callback(
        dash.dependencies.Output('table','children'),
        [dash.dependencies.Input('team','value'),
        dash.dependencies.Input('league','value')])
def show_table(team,league):
    if team is None:
        return generate_table(df3,50)
    dff = pd.read_pickle("./CSV_data/"+league+"/df_"+team+".pkl") 
    return generate_table(dff,50)
    
if __name__ == '__main__':
    app.run_server(debug=True,port = 8093)
 

