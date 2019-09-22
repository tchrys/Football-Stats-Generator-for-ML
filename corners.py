# -*- coding: utf-8 -*-

import pandas as pd
import data
import matplotlib.pyplot as plt
import collections
import numpy as np


# this function looks through matchday start to matchday end for some team
# and returns in how many matches prop(related to corners) is greater than n
def overNCorners(team, n, home, prop, start, end):
    total = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d[home] == team and float(d[prop]) > n:
            total += 1
    return total

# this function returns how many matches a team played at home and away as a
# tuple, from matchday start to end
def awayHome(team, start, end):
    away = 0
    home = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team:
            home += 1
        if d['AwayTeam'] == team:
            away += 1
    return [home, away]

# this function does the same as the first, but it refers to total number of
# corners (home team + away team)
def overNCornersOverAll(team, n, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team or d['AwayTeam'] == team:
            count += 1
            t = float(d['HC']) + float(d['AC'])
            if t > n:
                total += 1
    return total / count * 100 if count != 0 else 0

# the following functions compute the percentage of corners at home / away
def overNCornersHome(team, n, start , end):
    [home, away] = awayHome(team, start, end)
    return overNCorners(team, n, 'HomeTeam', 'HC', start, end) / home * 100 if home != 0 else 0

def overNCornersAway(team, n, start, end):
    [home, away] = awayHome(team, start, end)
    return overNCorners(team, n, 'AwayTeam', 'AC', start, end) / away * 100 if away != 0 else 0

def overNCornersHConc(team, n, start, end):
    [home, away] = awayHome(team, start, end)
    return overNCorners(team, n, 'HomeTeam', 'AC', start, end) / home * 100 if home != 0 else 0

def overNCornersAConc(team, n, start, end):
    [home, away] = awayHome(team, start, end)
    return overNCorners(team, n, 'AwayTeam', 'HC', start, end) / away * 100 if away != 0 else 0

func_dict = {'overNCornersHome' : overNCornersHome,
             'overNCornersAway' : overNCornersAway,
             'overNCornersOverAll' : overNCornersOverAll,
             'overNCornersHConc' : overNCornersHConc,
             'overNCornersAConc' : overNCornersAConc}

# this function has as input the name of the function we want and a number
# (over n corners) and returns a dict containing all teams results
def forAllTeams(function, n):
    d = dict()
    f = func_dict[function]
    for team in data.teams:
        d[team] = f(team, n, 1, data.rounds_played)
    return d

# the following functions returns stats as a string table for reading
def showCornersHome():
    over35H = forAllTeams('overNCornersHome', 3.5)
    over45H = forAllTeams('overNCornersHome', 4.5)
    over55H = forAllTeams('overNCornersHome', 5.5)
    over65H = forAllTeams('overNCornersHome', 6.5)
    
    df = pd.DataFrame([over35H, over45H, over55H, over65H],
    index = ['3.5H','4.5H','5.5H','6.5H'])
    df = df.T
    df = df.sort_values('6.5H')
    return df.to_string()
    
def showCornersAway():
    over35A = forAllTeams('overNCornersAway', 3.5)
    over45A = forAllTeams('overNCornersAway', 4.5)
    over55A = forAllTeams('overNCornersAway', 5.5)
    over65A = forAllTeams('overNCornersAway', 6.5)
    df = pd.DataFrame([over35A,over45A, over55A, over65A],
    index = ['3.5A','4.5A','5.5A','6.5A'])
    df = df.T
    df = df.sort_values('6.5A')
    return df.to_string()

def showCornersConcHome():
    over35H = forAllTeams('overNCornersHConc', 3.5)
    over45H = forAllTeams('overNCornersHConc', 4.5)
    over55H = forAllTeams('overNCornersHConc', 5.5)
    over65H = forAllTeams('overNCornersHConc', 6.5)
    
    df = pd.DataFrame([over35H, over45H, over55H, over65H],
    index = ['3.5H','4.5H','5.5H','6.5H'])
    df = df.T
    df = df.sort_values('6.5H')
    return df.to_string()

def showCornersConcAway():
    over35A = forAllTeams('overNCornersAConc', 3.5)
    over45A = forAllTeams('overNCornersAConc', 4.5)
    over55A = forAllTeams('overNCornersAConc', 5.5)
    over65A = forAllTeams('overNCornersAConc', 6.5)
    df = pd.DataFrame([over35A,over45A, over55A, over65A],
    index = ['3.5A','4.5A','5.5A','6.5A'])
    df = df.T
    df = df.sort_values('6.5A')
    return df.to_string()

def showCornersTotal():
    over75T = forAllTeams('overNCornersOverAll', 7.5)
    over85T = forAllTeams('overNCornersOverAll', 8.5)
    over95T = forAllTeams('overNCornersOverAll', 9.5)
    over105T = forAllTeams('overNCornersOverAll', 10.5)
    over115T = forAllTeams('overNCornersOverAll',11.5)
    df = pd.DataFrame([over75T,over85T, over95T,over105T, over115T],
    index = ['7.5T','8.5T','9.5T','10.5T','11.5T'])
    df = df.T
    df = df.sort_values('11.5T')
    return df.to_string()

# this function plots a histogram for any property in func_dict and shows
# it in ascending order
def makeHist(function, n):
    dictt = forAllTeams(function, n)
    sorted_x = sorted(dictt.items(), key=lambda kv: kv[1])
    sorted_dict = collections.OrderedDict(sorted_x)
    plt.figure(num=None, figsize=(14, 8), dpi=100)
    plt.xticks(rotation = 'vertical')
    plt.yticks(np.linspace(1, 100, 20))
    plt.title(function)
    plt.bar(sorted_dict.keys(), sorted_dict.values())
    plt.savefig('hist_over.png')