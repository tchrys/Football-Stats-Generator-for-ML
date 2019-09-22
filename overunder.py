# -*- coding: utf-8 -*-

import pandas as pd
import data
import matplotlib.pyplot as plt
import collections
import numpy as np

def overN(team, n, home, start, end):
    total = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d[home] == team and (float(d['FTHG']) + float(d['FTAG'])) > n:
            total += 1
    return total

def overNFirstHalf(team, n, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team or d['AwayTeam'] == team:
            count += 1
            if (float(d['HTHG']) + float(d['HTAG'])) > n:
                total += 1
    return total / count * 100 if count != 0 else 0

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

def overNHome(team, n, start, end):
    [home, away] = awayHome(team, start, end)
    return overN(team, n, 'HomeTeam', start, end) / home * 100 if home != 0 else 0

def overNAway(team, n, start, end):
    [home, away] = awayHome(team, start, end)
    return overN(team, n, 'AwayTeam', start, end) / away * 100 if away != 0 else 0

def overNOverAll(team, n, start, end):
    [home, away] = awayHome(team, start, end)
    return (overNHome(team, n, start, end) / 100 * home +
            overNAway(team, n, start, end) / 100 * away) / (home + away) * 100 if home + away != 0 else 0

func_dict = {'overNHome' : overNHome,
             'overNAway' : overNAway,
             'overNOverAll' : overNOverAll,
             'overNFirstHalf' : overNFirstHalf}

def forAllTeams(function, n):
    d = dict()
    f = func_dict[function]
    for team in data.teams:
        d[team] = f(team, n, 1, data.rounds_played)
    return d

def showOverHome():
    over0 = forAllTeams('overNHome', 0.5)
    over1 = forAllTeams('overNHome', 1.5)
    over2 = forAllTeams('overNHome', 2.5)
    over3 = forAllTeams('overNHome', 3.5)
    over4 = forAllTeams('overNHome', 4.5)
    df = pd.DataFrame([over0, over1, over2, over3, over4],
                      index = ['+0.5', '+1.5', '+2.5', '+3.5', '+4.5'])
    df = df.T
    return df.to_string()

def showOverAway():
    over0 = forAllTeams('overNAway', 0.5)
    over1 = forAllTeams('overNAway', 1.5)
    over2 = forAllTeams('overNAway', 2.5)
    over3 = forAllTeams('overNAway', 3.5)
    over4 = forAllTeams('overNAway', 4.5)
    df = pd.DataFrame([over0, over1, over2, over3, over4],
                      index = ['+0.5', '+1.5', '+2.5', '+3.5', '+4.5'])
    df = df.T
    return df.to_string()

def showOverAll():
    over0 = forAllTeams('overNOverAll', 0.5)
    over1 = forAllTeams('overNOverAll', 1.5)
    over2 = forAllTeams('overNOverAll', 2.5)
    over3 = forAllTeams('overNOverAll', 3.5)
    over4 = forAllTeams('overNOverAll', 4.5)
    df = pd.DataFrame([over0, over1, over2, over3, over4],
                      index = ['+0.5', '+1.5', '+2.5', '+3.5', '+4.5'])
    df = df.T
    return df.to_string()

def makeHist(function, n):
    dict = forAllTeams(function, n)
    sorted_x = sorted(dict.items(), key=lambda kv: kv[1])
    sorted_dict = collections.OrderedDict(sorted_x)
    plt.figure(num=None, figsize=(14, 8), dpi=100)
    plt.xticks(rotation = 'vertical')
    plt.yticks(np.linspace(1, 100, 20))
    plt.title(function)
    plt.bar(sorted_dict.keys(), sorted_dict.values())
    plt.savefig('hist_over.png')
    
