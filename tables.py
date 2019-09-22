# -*- coding: utf-8 -*-

import pandas as pd
import data

homeLoses = dict()
homeDraws = dict()
homeWins = dict()
awayLoses = dict()
awayDraws = dict()
awayWins = dict()
pointsAway = dict()
pointsHome = dict()
points = dict()

# returns a list of dicts for wins / draws / loses away and at home and points 
def computeResults(start, end):
    for team in data.teams:
        homeLoses[team] = 0
        homeDraws[team] = 0
        homeWins[team] = 0
        awayWins[team] = 0
        awayDraws[team] = 0
        awayLoses[team] = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['FTR'] == 'A':
            homeLoses[d['HomeTeam']] += 1
            awayWins[d['AwayTeam']] += 1
        elif d['FTR'] == 'D':
            homeDraws[d['HomeTeam']] += 1
            awayDraws[d['AwayTeam']] += 1
        else:
            homeWins[d['HomeTeam']] += 1
            awayLoses[d['AwayTeam']] += 1
    for team in data.teams:
        pointsAway[team] = 3 * awayWins[team] + awayDraws[team]
        pointsHome[team] = 3 * homeWins[team] + homeDraws[team]
        points[team] = pointsAway[team] + pointsHome[team]
    return [homeWins, homeDraws, homeLoses, awayWins, awayDraws, awayLoses,
 pointsHome, pointsAway, points]

def computeResultsAll():
    return computeResults(1, data.rounds_played)

def computeResultsLastN(n):
    return computeResults(data.rounds_played - n + 1, n)    

def showFirstHalfTable(start, end):
    hl = dict()
    hd = dict()
    hw = dict()
    al = dict()
    ad = dict()
    aw = dict()
    pa = dict()
    ph = dict()
    pts = dict()
    for team in data.teams:
        hl[team] = 0
        hd[team] = 0
        hw[team] = 0
        aw[team] = 0
        ad[team] = 0
        al[team] = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        if d['HTR'] == 'A':
            hl[d['HomeTeam']] += 1
            aw[d['AwayTeam']] += 1
        elif d['FTR'] == 'D':
            hd[d['HomeTeam']] += 1
            ad[d['AwayTeam']] += 1
        else:
            hw[d['HomeTeam']] += 1
            al[d['AwayTeam']] += 1
    for team in data.teams:
        pa[team] = 3 * aw[team] + ad[team]
        ph[team] = 3 * hw[team] + hd[team]
        pts[team] = pa[team] + ph[team]
    table = pd.DataFrame([hw, hd, hl, ph, aw,
                          ad, al, pa, pts],
    index = ['HW', 'HD', 'HL', 'PH', 'AW', 'AD', 'AL', 'PA', 'P'])
    table = table.T
    table = table.sort_values('P', ascending = False)
    return table

def showHomeTable(start, end):
    l = dict()
    dr = dict()
    w = dict()
    gm = dict()
    gp = dict()
    pts = dict()
    for team in data.teams:
        l[team] = 0
        dr[team] = 0
        w[team] = 0
        gm[team] = 0
        gp[team] = 0
        pts[team] = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        gm[d['HomeTeam']] += int(d['FTHG'])
        gp[d['HomeTeam']] += int(d['FTAG'])
        if d['FTR'] == 'A':
            l[d['HomeTeam']] += 1
        elif d['FTR'] == 'D':
            dr[d['HomeTeam']] += 1
        else:
            w[d['HomeTeam']] += 1
    for team in data.teams:
        pts[team] = 3 * w[team] + dr[team]
    table = pd.DataFrame([w, dr, l, gm, gp, pts],
            index = ['W', 'D', 'L', 'GM', 'GP', 'P'])
    table = table.T
    table = table.sort_values('P', ascending = False)
    return table

def showAwayTable(start, end):
    l = dict()
    dr = dict()
    w = dict()
    gm = dict()
    gp = dict()
    pts = dict()
    for team in data.teams:
        l[team] = 0
        dr[team] = 0
        w[team] = 0
        gm[team] = 0
        gp[team] = 0
        pts[team] = 0
    startRound = (start - 1) * data.games_per_round
    endRound = min(len(data.mpg), (end) * data.games_per_round)
    for d in data.mpg[startRound : endRound]:
        gm[d['AwayTeam']] += int(d['FTAG'])
        gp[d['AwayTeam']] += int(d['FTHG'])
        if d['FTR'] == 'H':
            l[d['AwayTeam']] += 1
        elif d['FTR'] == 'D':
            dr[d['AwayTeam']] += 1
        else:
            w[d['AwayTeam']] += 1
    for team in data.teams:
        pts[team] = 3 * w[team] + dr[team]
    table = pd.DataFrame([w, dr, l, gm, gp, pts],
            index = ['W', 'D', 'L', 'GM', 'GP', 'P'])
    table = table.T
    table = table.sort_values('P', ascending = False)
    return table

def showFTTableAll():
    return showFirstHalfTable(1, data.rounds_played)

def showFTTableLastN(n):
    start = data.rounds_played - n + 1
    return showFirstHalfTable(start, data.rounds_played)