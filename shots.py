# -*- coding: utf-8 -*-
import pandas as pd
import data
import matplotlib.pyplot as plt
import collections
import numpy as np

def SOT_GoalsAllTeams(start, end):
    d = dict()
    for team in data.teams:
        [home, away] = awayHome(team, start, end)
        goals = (goalsScoreAway(team, start, end) * away +
                 goalsScoredHome(team, start, end) * home ) / (home + away) if home + away != 0 else 0
        d[team] = goals / ((avgShotsAway(team, start, end) * away +
             avgShotsHome(team, start, end) * home) / (home + away)) * 100 if home + away != 0 else 0
    return d

def bothScored(team, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team or d['AwayTeam'] == team:
            count += 1
            if int(d['FTAG']) > 0 and int(d['FTHG']) > 0:
                total += 1
    return total / count * 100 if count != 0 else 0

# both scored and over 2.5
def bothScored_3(team, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team or d['AwayTeam'] == team:
            count += 1
            if int(d['FTAG']) > 0 and int(d['FTHG']) > 0:
                if int(d['FTAG']) + int(d['FTHG']) > 2.5:
                    total += 1
    return total / count * 100 if count != 0 else 0

def handicap15H(team, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team:
            count += 1
            if int(d['FTHG']) - int(d['FTAG']) > 1:
                total += 1
    return total / count * 100 if count != 0 else 0

def handicap15A(team, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['AwayTeam'] == team:
            count += 1
            if int(d['FTAG']) - int(d['FTHG']) > 1:
                total += 1
    return total / count * 100 if count != 0 else 0

def handicap15OverAll(team, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team:
            count += 1
            if int(d['FTHG']) - int(d['FTAG']) > 1:
                total += 1
        if d['AwayTeam'] == team:
            count += 1
            if int(d['FTAG']) - int(d['FTHG']) > 1:
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

def getProperty(team, prop, home, start, end):
    total = 0
    count = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d[home] == team:
            total += int(d[prop])
            count += 1
    return total / count if count != 0 else 0

def goalsScoredHome(team, start, end):
    return getProperty(team, 'FTHG', 'HomeTeam', start, end)

def goalsScoreAway(team, start, end):
    return getProperty(team, 'FTAG', 'AwayTeam', start, end)

def avgShotsHome(team, start, end):
    return getProperty(team, 'HS', 'HomeTeam', start, end)

def avgShotsAway(team, start, end):
    return getProperty(team, 'AS', 'AwayTeam', start, end)

def avgSOTHome(team, start, end):
    return getProperty(team, 'HST', 'HomeTeam', start, end)

def avgSOTAway(team, start, end):
    return getProperty(team, 'AST', 'AwayTeam', start, end)

def shotsList(team, start, end):
    return propList(team, start, end, 'HS', 'AS')

def SOTList(team, start, end):
    return propList(team, start, end, 'HST', 'AST')


func_dict = {'goalsScoredHome' : goalsScoredHome,
             'goalsScoreAway' : goalsScoreAway,
             'avgShotsHome' : avgShotsHome,
             'avgShotsAway' : avgShotsAway,
             'avgSOTHome' : avgSOTHome,
             'avgSOTAway' : avgSOTAway,
             'bothScored' : bothScored,
             'bothScored_3' : bothScored_3,
             'handicap15A' : handicap15A,
             'handicap15H' : handicap15H,
             'handicap15OverAll' : handicap15OverAll}

def forAllTeams(function, start, end):
    d = dict()
    f = func_dict[function]
    for team in data.teams:
        d[team] = f(team, start, end)
    return d

def SOTpercent(sh, sa, hsot, asot):
    percent = dict()
    for team in sh.keys():
        percent[team] = (hsot[team] + asot[team]) / (sh[team] + sa[team]) * 100
    return percent

def totalShots(sh, sa, start, end):
    total = dict()
    for team in sh.keys():
        [home, away] = awayHome(team, start, end)
        total[team] = (sh[team] * home + sa[team] * away) / (home + away)
    return total

def shotsStats(start, end):
    goalsH = forAllTeams('goalsScoredHome', start, end)
    goalsA = forAllTeams('goalsScoreAway', start, end)
    sh = forAllTeams('avgShotsHome', start, end)
    sa = forAllTeams('avgShotsAway', start, end)
    hsot = forAllTeams('avgSOTHome', start, end)
    asot = forAllTeams('avgSOTAway', start, end)
    totS = totalShots(sh, sa, start, end)
    eff = SOT_GoalsAllTeams(start, end)
    percent = SOTpercent(sh, sa, hsot, asot)
    df = pd.DataFrame([goalsH, goalsA, totS, sh, hsot, sa, asot, percent, eff],
            index = ['GH', 'GA', 'Total', 'H', 'H SOT', 'A', 'A SOT', 'OnTarget%', 'Goals/SOT'])
    df = df.T
    return df.to_string()

def shotsStatsAllMatches():
    return shotsStats(1, data.rounds_played)
    
def shotsStatsLastNMatches(n):
    start = data.rounds_played - n + 1
    return shotsStats(start, data.rounds_played)

def makeHist(function):
    ylimit = 7 if function in ['goalsScoredHome', 'goalsScoreAway'] else 30
    if function in ['bothScored', 'bothScored_3', 'handicap15A', 'handicap15H',
                        'handicap15OverAll']:
        ylimit = 100
    dict = forAllTeams(function, 1, data.rounds_played)
    sorted_x = sorted(dict.items(), key=lambda kv: kv[1])
    sorted_dict = collections.OrderedDict(sorted_x)
    plt.figure(num=None, figsize=(14, 8), dpi=100)
    plt.xticks(rotation = 'vertical')
    plt.yticks(np.linspace(1, ylimit, ylimit))
    plt.title(function)
    plt.bar(sorted_dict.keys(), sorted_dict.values())
    plt.savefig('hist_over.png')