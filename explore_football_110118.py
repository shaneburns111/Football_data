# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 13:47:47 2018

@author: sburns2
"""
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import csv 
from numpy import array
from numpy import argmax

from collections import OrderedDict
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import requests
import io
import pickle
def one_hot_ecode(data):
    
    values = array(data)
  #  print(values)
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    #print(integer_encoded)
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
  #  print(onehot_encoded)
    # invert first example
    inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])
 #   print(inverted)
    return inverted

def read_to_array(csvfile,key):
    vec = []
    unique = []
    with open(csvfile) as file:
        reader = csv.DictReader(file,delimiter = ",")
        for row in reader:
            vec.append(row[key])
    for i in vec:
        if i not in unique:
            unique.append(i)
   # print(unique)     
    return unique

def team_stats(df,team,index):
   
    df_home = df[df['HoA'] == 'Home' ]
    FTHG_ITH = (df_home['FT'+index+'G']).mean()

    FTAG_ITH = (df_home['FT_Opp_G']).mean()
    
    HTHG_ITH = (df_home['HT'+index+'G']).mean()
    SHHG_ITH = (df_home['SH'+index+'G']).mean()
    
    HTAG_ITH = (df_home['HT_Opp_G']).mean()
        
    CH_ITH = (df_home[''+index+'C']).mean()
    CA_ITH = (df_home['Opp_C']).mean()
    SHAG_ITH = df_home['SH_Opp_G'].mean()
    # Away stats
    
    df_away = df[df['HoA'] == 'Away' ]
    FTAG_ITA = (df_away['FT'+index+'G']).mean()
    FTHG_ITA = (df_away['FT_Opp_G']).mean()
    
    HTAG_ITA = (df_away['HT'+index+'G']).mean()
  
    HTHG_ITA = (df_away['HT_Opp_G']).mean()
   
    print("HTHG_ITA",HTHG_ITA)
    
    SHHG_ITA = df_away['SH_Opp_G'].mean()
    #SHHG_ITA
    print("SHHG_ITA",SHHG_ITA)
    SHAG_ITA = (df_away['SH'+index+'G']).mean()
    
    CA_ITA = (df_away[''+index+'C']).mean()
    
    
    print(""+team+" Corners",CA_ITA)
    CH_ITA = (df_away['Opp_C']).mean()
    print("CH_ITA",CH_ITA)
    
    print("\n")
    #gh_FT,ga_opp_FT, gh_HT,ga_opp_HT,cor_h,cor_a_opp,g_a_FT,g_h_opp_FT,g_a_HT,g_h_opp_HT,cor_a,cor_h_opp_HT,g_h_SH,g_h_o_SH
    return FTHG_ITH,FTAG_ITH,HTHG_ITH,SHHG_ITH,HTAG_ITH,CH_ITH,CA_ITH,SHAG_ITH,FTAG_ITA,FTHG_ITA,HTAG_ITA,SHHG_ITA,SHAG_ITA,CA_ITA,CH_ITA
    #return goals_home_FT,goals_Away_opp_FT, goals_home_HT,goals_Away_opp_HT,corners_home,corners_Away_opp,goals_away_FT,goals_home_opp_FT,goals_away_HT,goals_home_opp_HT,corners_away,CORNERS_home_opp,goals_home_SH,goals_home_opp_SH
    
    
    
    
def ref_stats(df,refs):
    """
    Function to parse csv and calculate Referee-level stats
    """
    Refs = []
    goals_vec = []
    y_cards = []
    r_cards = []
    for i in range(0,len(refs)):
        Ref = refs[i]
     #   print(Ref)
    #Ref = 'D Whitestone' 
        df_ref = df[ (df['Referee'] == Ref)]
        df_ref = (df_ref[['FTHG','FTAG',	'HTHG',	'HTAG','HY','AY','HR','AR']])
        df_ref['Total Yellow'] = df_ref['HY']+ df_ref['AY']    
        df_ref['Total Red'] = df_ref['HR']+ df_ref['AR']    
        df_ref['Total Goals'] = df_ref['FTHG']+ df_ref['FTAG']
   
        reds = (df_ref['Total Red']).mean()
        yellows =  (df_ref['Total Yellow']).mean()
        goals = (df_ref['Total Goals']).mean()
        #print(df_ref)
        Refs.append(Ref)
        goals_vec.append(goals)
        y_cards.append(yellows)
        r_cards.append(reds)
    dataset = pd.DataFrame({'Referee': Refs, 'Avg Goals': goals_vec, 'Avg Yellow': y_cards, 'Avg Red': r_cards}, columns=['Referee', 'Avg Goals', 'Avg Yellow', 'Avg Red'])
    #print(dataset)
def parse_csv_team(df,Team,index):
    """
    Parse team-level dataframe
    """
    
    df_home = df[ (df['HomeTeam'] == Team)]
    df_home.loc[:,'HoA'] = 'Home'
    df_home.rename(columns = {'AwayTeam':'Opposition','HTHG':'HT'+index+'G','FTHG':'FT'+index+'G','HC':''+index+'C','FTAG':'FT_Opp_G','HTAG':'HT_Opp_G','AC':'Opp_C'}, inplace = True)

    df_home['SH'+index+'G'] = df_home['FT'+index+'G']-df_home['HT'+index+'G']
    df_home['SH_Opp_G'] = df_home['FT_Opp_G']-df_home['HT_Opp_G']
    print("here home \n", df_home['SH'+index+'G']) # index team at home SHG
    print("here opp goals \n", df_home['SH_Opp_G']) # index team at home opp SHG
    df_home_red = df_home[ ['Opposition','Date','HT'+index+'G','SH'+index+'G','FT'+index+'G',''+index+'C','FTR','SH_Opp_G','FT_Opp_G','HT_Opp_G','Opp_C','HoA']]
    print("Team" ,Team)
    print("home red \n",df_home_red['SH'+index+'G'])
    
    df_away = df[ (df['AwayTeam'] == Team)]
    df_away.loc[:,'HoA'] = 'Away'
    df_away.rename(columns = {'HomeTeam':'Opposition','HTAG':'HT'+index+'G','FTAG':'FT'+index+'G','AC':''+index+'C' ,'FTHG':'FT_Opp_G','HTHG':'HT_Opp_G','HC':'Opp_C'}, inplace = True)

    df_away['SH_Opp_G']= df_away['FT_Opp_G']-df_away['HT_Opp_G']
    
    df_away['SH'+index+'G'] = df_away['FT'+index+'G']-df_away['HT'+index+'G']
    
    df_away_red = df_away[ ['Opposition','Date','HT'+index+'G','SH'+index+'G','FT'+index+'G',''+index+'C','FTR','HT_Opp_G','SH_Opp_G','FT_Opp_G','Opp_C','HoA']]
    frames = [df_away_red,df_home_red]
    print("here away \n", df_away['SH'+index+'G']) # index team goals when away from home
    print("here opp goals \n", df_away['SH_Opp_G'])# home team goals when index team away from home
    
    print("away red \n",df_away_red['SH'+index+'G'])
    dfc = pd.concat(frames) 
    
    print("combined home and away dfc \n",dfc.head(15))
    return pd.concat(frames)    
    
def get_team_index(teams):
    index = []
    for i in range(0,len(teams)):
        team = teams[i]
        parsed = list(team)
        a = [parsed[0],parsed[1],parsed[2]]
        index.append(''.join(a))
    return index    

def df_all_teams(teams,df,League):
    FTHG_ITH_vec = []
    FTAG_ITH_vec = []
    HTHG_ITH_vec = []
    SHHG_ITH_vec = []
    HTAG_ITH_vec = []
    CH_ITH_vec = []
    CA_ITH_vec = []
    SHAG_ITH_vec = []
    FTAG_ITA_vec = []
    FTHG_ITA_vec = []
    HTAG_ITA_vec = []
    SHHG_ITA_vec = []
    SHAG_ITA_vec = []
    CA_ITA_vec = []
    CH_ITA_vec = []
    team_vec = []
    
    for i in range(0,len(teams)):
        team = teams[i]
        parsed = list(team)
        a = [parsed[0],parsed[1],parsed[2]]
        ind = ''.join(a)
        df_team = parse_csv_team(df,team,ind)
        #print(df_team)   
        #gh_FT,ga_opp_FT, gh_HT,ga_opp_HT,cor_h,cor_a_opp,g_a_FT,g_h_opp_FT,g_a_HT,g_h_opp_HT,cor_a,cor_h_opp_HT,g_h_SH,g_h_o_SH = team_stats(df_team,team,ind)
        FTHG_ITH,FTAG_ITH,HTHG_ITH,SHHG_ITH,HTAG_ITH,CH_ITH,CA_ITH,SHAG_ITH,FTAG_ITA,FTHG_ITA,HTAG_ITA,SHHG_ITA,SHAG_ITA,CA_ITA,CH_ITA = team_stats(df_team,team,ind)
        FTHG_ITH_vec.append(FTHG_ITH) # Full time home goals_interest team home?
        FTAG_ITH_vec.append(FTAG_ITH)
        HTHG_ITH_vec.append(HTHG_ITH) # Half time home goal interest team at home
        SHHG_ITH_vec.append(SHHG_ITH)
        HTAG_ITH_vec.append(HTAG_ITH)
        CH_ITH_vec.append(CH_ITH) #
        CA_ITH_vec.append(CA_ITH) # away tean corners, team of interest at home
        SHAG_ITH_vec.append(SHAG_ITH)
        FTAG_ITA_vec.append(FTAG_ITA)
        FTHG_ITA_vec.append(FTHG_ITA)
        HTAG_ITA_vec.append(HTAG_ITA)
        SHHG_ITA_vec.append(SHHG_ITA)
        SHAG_ITA_vec.append(SHAG_ITA)
        CA_ITA_vec.append(CA_ITA)
        CH_ITA_vec.append(CH_ITA)
        team_vec.append(team)    
        df_team["Date"] = pd.to_datetime(df_team.Date, format = "%d/%m/%Y")
        df_team = df_team.sort_values(by = ["Date"])
        
        df_team.to_pickle("./CSV_data/"+League+"/df_"+team+".pkl")
    df_stats = pd.DataFrame(OrderedDict({"Team":team_vec,"FTHG_ITH": FTHG_ITH_vec,"FTAG_ITH":FTAG_ITH_vec,"HTHG_ITH":HTHG_ITH_vec,"SHHG_ITH":SHHG_ITH_vec,"HTAG_ITH":HTAG_ITH_vec,"CH_ITH":CH_ITH_vec,"CA_ITH":CA_ITH_vec,"SHAG_ITH":SHAG_ITH_vec,"FTAG_ITA":FTAG_ITA_vec,"FTHG_ITA":FTHG_ITA_vec,"HTAG_ITA":HTAG_ITA_vec,"SHHG_ITA":SHHG_ITA_vec,"SHAG_ITA":SHAG_ITA_vec,"CA_ITA":CA_ITA_vec,"CH_ITA":CH_ITA_vec }  ) )   
    
    #df_stats = pd.DataFrame(OrderedDict({"Team":team_vec,"Team_home_FTG": gh_FT_vec,"Opp_away_FTG":ga_opp_FT_vec,"Team_home_HTG":gh_HT_vec,"Opp_away_HTG":ga_opp_HT_vec,"Team_home_cor":cor_h_vec,"Opp_away_cor":cor_a_opp_vec,"Home_second_half_goals":g_h_SH_vec,"Away_opp_second_half_goals":g_h_o_SH_vec}) )   
    #print(cor_h_opp_HT_vec)    
    
    #print(df_stats)
    return df_stats
def poisson_stats(df):
   # print("dlksjdsklds",df.head(10))
    Avg_home_FTG = df['FTHG_ITH'].mean()
    Avg_away_FTG = df['FTAG_ITH'].mean()
    Avg_home_HTG = df['HTHG_ITH'].mean()
    Avg_away_HTG = df['HTAG_ITH'].mean()
    Avg_home_SHG = df['SHHG_ITH'].mean()
    Avg_away_SHG = df['SHAG_ITH'].mean()
    Avg_Team_home_cor = df['CH_ITH'].mean()
    Avg_Opp_away_cor = df['CA_ITH'].mean()
    #print("Avg_home_FTG",Avg_home_FTG)
    #print("Avg_away_FTG",Avg_away_FTG)
    #print("Avg_home_HTG",Avg_home_HTG)
    #print("Avg_away_HTG",Avg_away_HTG)
    #print("Avg_Team_home_corr",Avg_Team_home_cor)
    #print("Avg_Opp_away_corr",Avg_Opp_away_cor)
    #print(df)
    df['Team_home_FTG'] = df['FTHG_ITH']/ Avg_home_FTG
    df['Team_home_HTG'] = df['HTHG_ITH']/ Avg_home_HTG
    df['Opp_away_FTG'] = df['FTAG_ITH']/Avg_away_FTG
    df['Opp_away_HTG'] = df['HTAG_ITH']/Avg_away_HTG
    df['Team_home_cor'] = df['CH_ITH']/Avg_Team_home_cor
    df['Opp_away_cor'] = df['CA_ITH']/Avg_Opp_away_cor
   # print(df)
    
    return Avg_home_HTG,Avg_away_HTG, Avg_home_SHG,Avg_away_SHG,df

def attack_defence_strength(poisson_df,home_team,away_team,Avg_home_HTG,Avg_away_HTG, Avg_home_SHG,Avg_away_SHG):
    """
    Home goals = attack_strength_home_team*defence_strength_away_team*avg_home_goals
    Away goals = attack_strength_away_team*defence_strength_home_team*avg_away_goals
    
    """
    df1 = poisson_df[(poisson_df['Team'] == home_team)]
    df2 = poisson_df[(poisson_df['Team'] == away_team)]
    HTG = df1['Team_home_HTG']*df2['Opp_away_HTG'] 
   
def download_csv():
    url_E0 = 'http://www.football-data.co.uk/mmz4281/1819/E0.csv'
    url_E1 = 'http://www.football-data.co.uk/mmz4281/1819/E1.csv'
    url_E2 = 'http://www.football-data.co.uk/mmz4281/1819/E2.csv'
    url_E3 = 'http://www.football-data.co.uk/mmz4281/1819/E3.csv'
    
    E0=requests.get(url_E0).content
    E1=requests.get(url_E1).content
    E2=requests.get(url_E2).content
    E3=requests.get(url_E3).content
    
    df_E0 = pd.read_csv(io.StringIO(E0.decode('utf-8')))
    df_E1 = pd.read_csv(io.StringIO(E1.decode('utf-8')))
    df_E2 = pd.read_csv(io.StringIO(E2.decode('utf-8')))
    df_E3 = pd.read_csv(io.StringIO(E3.decode('utf-8')))
    
    df_E0.to_csv("./CSV_data/PremierLeague/E0.csv")
    df_E1.to_csv("./CSV_data/Championship/E1.csv")
    df_E2.to_csv("./CSV_data/League1/E2.csv")
    df_E3.to_csv("./CSV_data/league2/E3.csv")
    
def main():
    download_csv()
    #filepath = "./CSV_data/League2/E3.csv";League = "League2"
    filepath = "./CSV_data/PremierLeague/E0.csv"; League = "Premierleague"
 
    
    refs = read_to_array(filepath,'Referee')
    teams = read_to_array(filepath,'HomeTeam')  
    #index = get_team_index(teams)
    
    df = pd.read_csv(filepath)
   
    #refs_encoded = one_hot_ecode(refs)
    #ref_stats(df,refs)
 
    stats  = df_all_teams(teams,df,League)
    print(stats)
    Avg_home_HTG,Avg_away_HTG, Avg_home_SHG,Avg_away_SHG,poisson_df = poisson_stats(stats)
    attack_defence_strength(poisson_df,"Liverpool","Wolves",Avg_home_HTG,Avg_away_HTG, Avg_home_SHG,Avg_away_SHG)
  
main()    
