# -*- coding: utf-8 -*-

import csv
import datetime as dt
import os


'''leagues represent the name of leagues for which we have the results
0 stands for first division(initially i had england's first 4 leagues)
trainLeagues represent the leagues for ML training
startYears - first chronologically year for which we have the results
errorYears - years for which we don't have the results
all_props represent the contents of a csv line:
FT stands for full time and HT for half time
H - home , A - away, G - goals, FTR - full time result(H / D / A),
S - shots, ST - shots on target, F -fouls, Y - yellow, R - red(cards)
'''

leagues = ['spain0', 'italy0', 'england0',
           'germany0', 'france0', 'portugal0', 'netherlands0']

trainleagues = ['italy0', 'england0', 'germany0', 'france0',
           'portugal0', 'netherlands0']

trainleagues = []

errorYears = {'england0' : [2014], 'france0' : [2011, 2016],
              'germany0' : [], 'italy0' : [2012, 2014, 2015, 2016],
              'netherlands0' : [], 'portugal0' : [], 'spain0' : []}

startYears = {'england0' : 2004, 'france0' : 2007, 'germany0' : 2006,
              'italy0' : 2006, 'netherlands0' : 2017, 'portugal0' : 2017,
              'spain0' : 2005}

all_props = ['FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'HS', 'AS', 'HST',
             'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']

# this function gets the team list for a given championship(it adds teams while
# the total number of teams is unreached)
def getTeamsFromData(mpg):
    count = 0
    teams = []
    for d in mpg:
        if d['HomeTeam'] not in teams:
            teams.append(d['HomeTeam'])
            count += 1
        if d['AwayTeam'] not in teams:
            teams.append(d['AwayTeam'])
            count += 1
        if count == nr_teams:
            break
    return teams

def getLeagueProps(mpg):
    leagueProp = []
    for d in mpg[0].keys():
        if d in all_props:
            leagueProp.append(d)
    return leagueProp

# this function finds out where to output data
def settings(country, league, year):
    country = country[:-1]
    path = os.getcwd()
    countryupp = country[0]
    countryupp = chr(ord(countryupp) - 32)
    dataFile = countryupp + str(league) + str(year)
    relPath = '\\' + country + '\\' + str(league) + '\\' + dataFile + '.csv'
    gen_data_folder = country + '\\' + str(league) + '\\' + str(year) + '\\'
    print(gen_data_folder)
    file_path = path + relPath 
    print(file_path)
    return [gen_data_folder, file_path]

def getcurrentRoundFromNrGame(games_played):
    return (int)(games_played / games_per_round) + 1

# this function converts a csv file to a list of dicts 
def getMpg(file_path):
    with open(file_path) as csvfile:
        mpg = list(csv.DictReader(csvfile))    
    return mpg

# we can get the number of teams by looking at the date of games.
# Normally, first round is played in at most 4 days, but i extend the number
# of days to 15 to be sure all teams played at least once
def getNrTeams(mpg):
    firstMatch = mpg[0]['Date'].split('/')
    date1 = dt.datetime(int(firstMatch[2]),
                        int(firstMatch[1]), int(firstMatch[0]))
    nr_teams = 0
    teams_played = []
    for d in mpg:
        matchTime = d['Date'].split('/')
        currDate = dt.datetime(int(matchTime[2]), int(matchTime[1]),
                               int(matchTime[0]))
        if d['HomeTeam'] not in teams_played:
            teams_played.append(d['HomeTeam'])
            nr_teams += 1
        if d['AwayTeam'] not in teams_played:
            teams_played.append(d['AwayTeam'])
            nr_teams += 1
        expDate = date1 + dt.timedelta(days = 15)
        if currDate > expDate:
            break
    return nr_teams
    
# this function gets the team list, games props, rounds etc
def getDt(mpg):
    teams = getTeamsFromData(mpg)
    leagueProp = getLeagueProps(mpg)
    games_per_round = (int) (nr_teams / 2)
    rounds_played = 2 * nr_teams - 2
    games_played = games_per_round * rounds_played
    return [teams, leagueProp, games_played, games_per_round, rounds_played]

# in this file we can set for which country and year we want statistics
# for instance, csv_maker.py functions gets mpg from here    

country = 'netherlands0'
league = 0
year = 2018

[gen_data_folder, file_path] = settings(country, league, year)
mpg = getMpg(file_path)
nr_teams = getNrTeams(mpg)
[teams, leagueProp, games_played, games_per_round, rounds_played] = getDt(mpg)    
