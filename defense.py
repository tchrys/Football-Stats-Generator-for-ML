# -*- coding: utf-8 -*-

# this file is very similar to corners.py, but refers to defense stats:
# corners, fouls, goals or shots conceded and yellow / red cards

import pandas as pd
import data
import matplotlib.pyplot as plt
import collections
import numpy as np

def getPropertyNoDivision(team, home, prop, start, end):
    total = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d[home] == team:
            total += int(d[prop])
    return total

def propList(team, start, end, prop1, prop2):
    pos = []
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team:
            pos.append(int(d[prop1]))
        if d['AwayTeam'] == team:
            pos.append(int(d[prop2]))
    return pos

def getProperty(team, home, prop, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d[home] == team:
            total += int(d[prop])
            count += 1
    return total / count if count != 0 else 0

def foulsHome(team, start, end):
    return getProperty(team, 'HomeTeam', 'HF', start, end)

def foulsAway(team, start, end):
    return getProperty(team, 'AwayTeam', 'AF', start, end)

def yellowHome(team, start, end):
    return getProperty(team, 'HomeTeam', 'HY', start, end)

def yellowAway(team, start, end):
    return getProperty(team, 'AwayTeam', 'AY', start, end)

def redHome(team, start, end):
    return getPropertyNoDivision(team, 'HomeTeam', 'HR', start, end)

def redAway(team, start, end):
    return getPropertyNoDivision(team, 'AwayTeam', 'AR', start, end)

def goalsConcededHome(team, start, end):
    return getProperty(team, 'HomeTeam', 'FTAG', start, end)

def goalsConcededAway(team, start, end):
    return getProperty(team, 'AwayTeam', 'FTHG', start, end)

def oponentShotsHome(team, start, end):
    return getProperty(team, 'HomeTeam', 'AS', start, end)

def oponentShotsAway(team, start, end):
    return getProperty(team, 'AwayTeam', 'HS', start, end)

def oponentSOTHome(team, start, end):
    return getProperty(team, 'HomeTeam', 'AST', start, end)

def oponentSOTAway(team, start, end):
    return getProperty(team, 'AwayTeam', 'HST', start, end)

def foulsList(team, start, end):
    return propList(team, start, end, 'HF', 'AF')

def yellowsList(team, start, end):
    return propList(team, start, end, 'HY', 'AY')

def goalsConcededList(team, start, end):
    return propList(team, start, end, 'FTAG', 'FTHG')

def opShotsList(team, start, end):
    return propList(team, start, end, 'AS', 'HS')

def opSOTList(team, start, end):
    return propList(team, start, end, 'AST', 'HST')

func_dict = {'foulsHome' : foulsHome, 'foulsAway' : foulsAway,
             'yellowHome' : yellowHome, 'yellowAway' : yellowAway,
             'redHome' : redHome, 'redAway' : redAway,
             'goalsConcededHome' : goalsConcededHome,
             'goalsConcededAway' : goalsConcededAway,
             'oponentShotsAway' : oponentShotsAway,
             'oponentShotsHome' : oponentShotsHome,
             'oponentSOTHome' : oponentSOTHome,
             'oponentSOTAway' : oponentSOTAway}

def forAllTeams(function, start, end):
    d = dict()
    f = func_dict[function]
    for team in data.teams:
        d[team] = f(team, start, end)
    return d

def showDefenceHome(start, end):
    foulsH = forAllTeams('foulsHome', start, end)
    yH = forAllTeams('yellowHome', start, end)
    rH = forAllTeams('redHome', start, end)
    sH = forAllTeams('oponentShotsHome', start, end)
    sotH = forAllTeams('oponentSOTHome', start, end)
    gH = forAllTeams('goalsConcededHome', start, end)
    
    df = pd.DataFrame([foulsH, yH, rH, sH, sotH, gH],
                      index = ['F', 'Y', 'R', 'S', 'SOT', 'G'])
    df = df.T
    df = df.sort_values('G')
    return df.to_string()
    

def showDefenceAway(start, end):
    foulsA = forAllTeams('foulsAway', start, end)
    yA = forAllTeams('yellowAway', start, end)
    rA = forAllTeams('redAway', start, end)
    sA = forAllTeams('oponentShotsAway', start, end)
    sotA = forAllTeams('oponentSOTAway', start, end)
    gA = forAllTeams('goalsConcededAway', start, end)
    
    df = pd.DataFrame([foulsA, yA, rA, sA, sotA, gA],
                      index = ['F', 'Y', 'R', 'S', 'SOT', 'G'])
    df = df.T
    df = df.sort_values('G')
    return df.to_string()

def showDefenceHomeAllMatches():
    return showDefenceHome(1, data.rounds_played)
    
def showDefenceAwayAllMatches():
    return showDefenceAway(1, data.rounds_played)
    
def showDefenceHomeLastNMatches(n):
    return showDefenceHome(data.rounds_played - 2 * n + 1, data.rounds_played)
    
def showDefenceAwayLastNMatches(n):
    return showDefenceAway(data.rounds_played - 2 * n + 1, data.rounds_played)

def makeHist(function):
    dict = forAllTeams(function, 1, data.rounds_played)
    sorted_x = sorted(dict.items(), key=lambda kv: kv[1])
    sorted_dict = collections.OrderedDict(sorted_x)
    plt.figure(num=None, figsize=(14, 8), dpi=100)
    plt.xticks(rotation = 'vertical')
    plt.yticks(np.linspace(1, 30, 30))
    plt.title(function)
    plt.bar(sorted_dict.keys(), sorted_dict.values())
    plt.savefig('hist_over.png')
    