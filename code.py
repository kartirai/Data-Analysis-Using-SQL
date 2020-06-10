# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:44:03 2020

@author: karti
"""


import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

path = 'C:/Users/karti/Documents/Kartikey DS/SQL Kaggle/'
database = path + 'database.sqlite'

conn = sqlite3.connect(database)
tables = pd.read_sql("""SELECT * FROM sqlite_master WHERE type = 'table';""",conn)
tables

countries = pd.read_sql("""SELECT * FROM country;""",conn)
countries

leagues = pd.read_sql("""SELECT * from league JOIN Country ON country.id = league.country_id;""",conn)
print(leagues)

teams = pd.read_sql("""SELECT * FROM Team ORDER BY team_long_name LIMIT 10""",conn)
print(teams)

detailed_matches = pd.read_sql("""SELECT Match.id,
                               Country.name AS Country_name,
                               season,
                               stage,
                               date,
                               HT.team_long_name AS home_team,
                               AT.team_long_name AS away_team,
                               home_team_goal,
                               away_team_goal FROM Match
                               JOIN Country on Country.id = Match.country_id
                               JOIN League on League.id = Match.league_id
                               LEFT JOIN Team as HT ON HT.team_api_id = Match.home_team_api_id
                               LEFT JOIN Team as AT ON AT.team_api_id = Match.away_team_api_id
                               WHERE country_name = 'Spain'
                               ORDER BY Date
                               LIMIT 10;""",conn)
                               
                               
leagues_by_season = pd.read_sql("""SELECT Country.name as country_name,
                                League.name as league_name,
                                season,
                                COUNT(DISTINCT stage) AS number_of_stages,
                                COUNT(DISTINCT HT.team_long_name) AS number_of_teams,
                                AVG(home_team_goal) AS avg_home_team_scores,
                                AVG(away_team_goal) AS avg_away_team_scores,
                                AVG(home_team_goal - away_team_goal) AS avg_goal_diff,
                                AVG(home_team_goal + away_team_goal) AS avg_goals,
                                SUM(home_team_goal + away_team_goal) AS total_goals
                                FROM Match
                                JOIN Country ON Country.id = Match.Country_id
                                JOIN League ON League.id = Match.League_id
                                LEFT JOIN Team as HT ON HT.team_api_id = Match.home_team_api_id
                                WHERE Country_name IN ('Spain','Germany','France','Italy','England')
                                GROUP BY 1,2,3 
                                HAVING COUNT(DISTINCT stage) > 10
                                ORDER BY Country.name,League.name,season DESC;""",conn
                                )

players_height = pd.read_sql(""" SELECT CASE
                                         WHEN ROUND(height)<165 THEN 165
                                         WHEN ROUND(height)>195 THEN 195
                                         ELSE ROUND(height)
                                         END AS calc_height,
                                         COUNT(height) As distribution,
                                         (AVG(PA_Grouped.avg_overall_rating)) AS avg_overall_rating,
                                         (AVG(PA_Grouped.avg_potential)) AS avg_potential,
                                         AVG(weight) AS avg_weight
                                         FROM PLAYER
                                         LEFT JOIN(SELECT Player_attributes.player_api_id,
                                         AVG(Player_attributes.overall_rating) AS avg_overall_rating,
                                         AVG(Player_attributes.overall_rating) AS avg_potential
                                         FROM Player_attributes
                                         GROUP BY Player_attributes.player_api_id)
                                         AS PA_grouped ON PLAYER.player_api_id = PA_grouped.player_api_id
                                         GROUP BY calc_height
                                         ORDER BY calc_height;""",conn)
print(players_height)