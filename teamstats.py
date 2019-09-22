# -*- coding: utf-8 -*-
import shots as sh
import pandas as pd
import tables
import data
import numpy as np
import defense as df
import matplotlib as mpl
import matplotlib.pyplot as plt
import overunder as ovr
import corners as crn
import os

homeLoses = dict()
homeDraws = dict()
homeWins = dict()
awayLoses = dict()
awayDraws = dict()
awayWins = dict()
pointsAway = dict()
pointsHome = dict()
points = dict()
            
hist_params = {'overNHome' : ovr.makeHist, 'overNAway' : ovr.makeHist,
               'overNOverAll' : ovr.makeHist, 'foulsHome' : df.makeHist,
               'foulsAway' : df.makeHist, 'yellowHome' : df.makeHist,
               'yellowAway' : df.makeHist, 'redHome' : df.makeHist,
               'redAway' : df.makeHist, 'goalsConcededHome' : df.makeHist,
               'goalsConcededAway' : df.makeHist, 'avgSOTHome' : sh.makeHist,
               'oponentShotsAway' : df.makeHist, 'avgShotsAway' : sh.makeHist,
               'oponentShotsHome' : df.makeHist, 'avgShotsHome' : sh.makeHist,
               'oponentSOTHome' : df.makeHist, 'goalsScoreAway' : sh.makeHist,
               'oponentSOTAway' : df.makeHist, 'goalsScoredHome' : sh.makeHist,
               'avgSOTAway' : sh.makeHist, 'overNCornersHome' : crn.makeHist,
       'overNCornersAway' : crn.makeHist, 'overNCornersOverAll' : crn.makeHist,
       'overNCornersHConc' : crn.makeHist, 'overNCornersAConc' : crn.makeHist,
       'bothScored' : sh.makeHist, 'bothScored_3' : sh.makeHist,
       'handicap15A' : sh.makeHist, 'handicap15H' : sh.makeHist,
       'handicap15OverAll' : sh.makeHist, 'overNFirstHalf' : ovr.makeHist}


def makeHist(prop, n = None):
    f = hist_params[prop]
    if n == None:
        f(prop)
    else:
        f(prop, n)

listFunctions = {'shotsList' : sh.shotsList,
                 'SOTList' : sh.SOTList,
                 'foulsList' : df.foulsList,
                 'goalsConcededList' : df.goalsConcededList,
                 'opShotsList' : df.opShotsList,
                 'opSOTList' : df.opSOTList,
                 'yellowsList' : df.yellowsList}


def showLeagueTableInterval(start, end):
    [homeWins, homeDraws, homeLoses, awayWins, awayDraws, awayLoses,
 pointsHome, pointsAway, points] = tables.computeResults(start, end)
    table = pd.DataFrame([homeWins, homeDraws, homeLoses,
            pointsHome, awayWins, awayDraws, awayLoses,
            pointsAway, points],
    index = ['HW', 'HD', 'HL', 'PH', 'AW', 'AD', 'AL', 'PA', 'P'])
    table = table.T
    table = table.sort_values('P', ascending = False)
    return table

def showLeagueTable():
    return showLeagueTableInterval(1, data.rounds_played)

def showLeagueTableLastN(n):
    return showLeagueTableInterval(data.rounds_played - n + 1, data.rounds_played)
    
# returns two lists - one for position after each round and one for points
def teamProgress(team, start, end):
    lst = list(np.arange(1, data.nr_teams + 1))
    pts = []
    pos = []
    i = start
    while i <= end:
        t = showLeagueTableInterval(start, i)
        t['index'] = lst
        t.set_index('index')
        pos.append(t.loc[team]['index'])
        pts.append(t.loc[team]['P'])
        i += 1
    return [pos, pts]

def getInfoTeam(team, start, end):
    d = []
    lst = list(np.arange(1, data.nr_teams + 1))
    t = showLeagueTableInterval(start, end)
    t['index'] = lst
    t.set_index('index')
    d.append(('Position', t.loc[team]['index']))
    d.append(('Points', t.loc[team]['P']))
    d.append(('Home Wins', t.loc[team]['HW']))
    d.append(('Home Draws', t.loc[team]['HD']))
    d.append(('Home Loses', t.loc[team]['HL']))
    d.append(('Away Wins', t.loc[team]['AW']))
    d.append(('Away Draws', t.loc[team]['AD']))
    d.append(('Away Loses', t.loc[team]['AL']))
    return d

def plotTeamProgressPosition(team, start, end):
    [pos, pts] = teamProgress(team, start, end)
    plt.figure(num=None, figsize=(10, 6), dpi=100)
    plt.xticks(np.linspace(start, end, end - start + 1))
    plt.yticks(np.linspace(1, data.nr_teams, data.nr_teams))
    plt.plot(np.linspace(start, end, end - start + 1), pos)
    plt.savefig('progress.png')
    plt.show()
    
def plotTeamProgressPoints(team, start, end):
    [pos, pts] = teamProgress(team, start, end)
    plt.figure(num=None, figsize=(10, 6), dpi=100)
    plt.xticks(np.linspace(start, end, end - start + 1))
    plt.yticks(np.arange(0, 100, 3))
    plt.plot(np.linspace(start, end, end - start + 1), pts)
    plt.savefig('progress.png')
    plt.show()

# makes a plot of some property for any number of teams given as a list
def plotProp(teams, start, end, prop):
    func = listFunctions[prop]
    pos = []
    for team in teams:
        pos.append(func(team, start, end))
    plt.figure(num=None, figsize = (10, 6), dpi = 100)
    plt.xticks(np.linspace(start, end, end - start + 1))
    plt.yticks(np.linspace(1, 30, 30))
    for i in range(len(teams)):
        plt.plot(np.linspace(start, end, end - start + 1), pos[i],
                 c = np.random.rand(3,), label = teams[i])
    plt.legend(loc = 'upper right')
    plt.savefig('prop.png')
    plt.show()
    
    
def plotTeamsProgressPos(teams, start, end):
    pos = []
    for team in teams:
        pos.append(teamProgress(team, start, end)[0])
    plt.figure(num=None, figsize=(10, 6), dpi=100)
    plt.xticks(np.linspace(start, end, end - start + 1))
    plt.yticks(np.linspace(1, data.nr_teams, data.nr_teams))
    for i in range(len(teams)):
        plt.plot(np.linspace(start, end, end - start + 1), pos[i],
                 c = np.random.rand(3,), label = teams[i])
    plt.legend(loc = 'upper right')
    plt.savefig('progress.png')
    plt.show()
    
def plotTeamsProgressPts(teams, start, end):
    pos = []
    for team in teams:
        pos.append(teamProgress(team, start, end)[1])
    plt.figure(num=None, figsize=(10, 6), dpi=100)
    plt.xticks(np.linspace(start, end, end - start + 1))
    plt.yticks(np.arange(0, 100, 3))
    for i in range(len(teams)):
        plt.plot(np.linspace(start, end, end - start + 1), pos[i],
                 c = np.random.rand(3,), label = teams[i])
    plt.legend(loc = 'bottom right')
    plt.savefig('progress.png')
    plt.show()
    
def lastNFixtures(team, n, end):
    start = end - n + 1
    startRound = (start - 1) * data.games_per_round
    endRound = min((end) * data.games_per_round, len(data.mpg))
    fixtures = []
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team or d['AwayTeam'] == team:
            fixtures.append(''.join([d['HomeTeam'], ' ', d['FTHG'], ' - ', d['FTAG'],
                        ' ', d['AwayTeam']]))
    return fixtures
            
def last5Fixtures(team, end):
    return lastNFixtures(team, 5, end)
    
def teamFormLastN(team, n, end):
    start = end - n + 1
    startRound = (start - 1) * data.games_per_round
    endRound = min((end) * data.games_per_round, len(data.mpg))
    form = ''
    for d in data.mpg[startRound : endRound]:
        if d['HomeTeam'] == team:
            if d['FTR'] == 'H':
                form = form + 'W-'
            elif d['FTR'] == 'A':
                form = form + 'L-'
            else:
                form = form + 'D-'
        if d['AwayTeam'] == team:
            if d['FTR'] == 'H':
                form = form + 'L-'
            elif d['FTR'] == 'A':
                form = form + 'W-'
            else:
                form = form + 'D-'
    form = form[:-1]
    return form
 
def teamFormLast5(team, end):
    return teamFormLastN(team, 5, end)
    
def formPoints(form):
    total = 0
    for letter in form:
        if letter == 'W':
            total += 3
        if letter == 'D':
            total += 1
    return total

def getTeamStatsForOutput(team, start, end, formStr):
    d = getInfoTeam(team, start, end)
    if data.rounds_played > 4 and end > 4:
        if formStr == 1:
            d.append(('Form', teamFormLast5(team, end)))
            fxt = last5Fixtures(team, end)
            d.append(('Last 1', fxt[4]))
            d.append(('Last 2', fxt[3]))
            d.append(('Last 3', fxt[2]))
            d.append(('Last 4', fxt[1]))
            d.append(('Last 5', fxt[0]))
        else:
            form = teamFormLast5(team, end)
            d.append(('Last5Points', formPoints(form)))
    else:
        form = teamFormLastN(team, end, end)
        d.append(('Last5Points', formPoints(form)))
    d.append(('GG', sh.bothScored(team, start, end)))
    d.append(('GG3+', sh.bothScored_3(team, start, end)))
    d.append(('Handicap 1.5 H', sh.handicap15H(team, start, end)))
    d.append(('Handicap 1.5 A', sh.handicap15A(team, start, end)))
    d.append(('Handicap 1.5 T', sh.handicap15OverAll(team, start, end)))
    d.append(('Goals Home', sh.goalsScoredHome(team, start, end)))
    d.append(('Goals Away', sh.goalsScoreAway(team, start, end)))
    d.append(('Shots Home', sh.avgShotsHome(team, start, end)))
    d.append(('Shots Away', sh.avgShotsAway(team, start, end)))
    d.append(('SOT Home', sh.avgSOTHome(team, start, end)))
    d.append(('SOT Away', sh.avgSOTAway(team, start, end)))
    d.append(('Fouls Home', df.foulsHome(team, start, end)))
    d.append(('Fouls Away', df.foulsAway(team, start, end)))
    d.append(('Yellow Home', df.yellowHome(team, start, end)))
    d.append(('Yellow Away', df.yellowAway(team, start, end)))
    d.append(('Red Home', df.redHome(team, start, end)))
    d.append(('Red Away', df.redAway(team, start, end)))
    d.append(('Goals Op Home', df.goalsConcededHome(team, start, end)))
    d.append(('Goals Op Away', df.goalsConcededAway(team, start, end)))
    d.append(('Shots Op Home', df.oponentShotsHome(team, start, end)))
    d.append(('Shots op Away', df.oponentShotsAway(team, start, end)))
    d.append(('SOT Op Home', df.oponentSOTHome(team, start, end)))
    d.append(('SOT Op Away', df.oponentSOTAway(team, start, end)))
    d.append(('+0.5H', ovr.overNHome(team, 0.5, start, end)))
    d.append(('+1.5H', ovr.overNHome(team, 1.5, start, end)))
    d.append(('+2.5H', ovr.overNHome(team, 2.5, start, end)))
    d.append(('+3.5H', ovr.overNHome(team, 3.5, start, end)))
    d.append(('+0.5A', ovr.overNAway(team, 0.5, start, end)))
    d.append(('+1.5A', ovr.overNAway(team, 1.5, start, end)))
    d.append(('+2.5A', ovr.overNAway(team, 2.5, start, end)))
    d.append(('+3.5A', ovr.overNAway(team, 3.5, start, end)))
    d.append(('+0.5T', ovr.overNOverAll(team, 0.5, start, end)))
    d.append(('+1.5T', ovr.overNOverAll(team, 1.5, start, end)))
    d.append(('+2.5T', ovr.overNOverAll(team, 2.5, start, end)))
    d.append(('+3.5T', ovr.overNOverAll(team, 3.5, start, end)))
    d.append(('+0.5 FH', ovr.overNFirstHalf(team, 0.5, start, end)))
    d.append(('+1.5 FH', ovr.overNFirstHalf(team, 1.5, start, end)))
    d.append(('+2.5 FH', ovr.overNFirstHalf(team, 2.5, start, end)))
    d.append(('+3.5H CK', crn.overNCornersHome(team, 3.5, start, end)))
    d.append(('+4.5H CK', crn.overNCornersHome(team, 4.5, start, end)))
    d.append(('+5.5H CK', crn.overNCornersHome(team, 5.5, start, end)))
    d.append(('+6.5H CK', crn.overNCornersHome(team, 6.5, start, end)))
    d.append(('+3.5A CK', crn.overNCornersAway(team, 3.5, start, end)))
    d.append(('+4.5A CK', crn.overNCornersAway(team, 4.5, start, end)))
    d.append(('+5.5A CK', crn.overNCornersAway(team, 5.5, start, end)))
    d.append(('+6.5A CK', crn.overNCornersAway(team, 6.5, start, end)))
    d.append(('+7.5T CK', crn.overNCornersOverAll(team, 7.5, start, end)))
    d.append(('+8.5T CK', crn.overNCornersOverAll(team, 8.5, start, end)))
    d.append(('+9.5T CK', crn.overNCornersOverAll(team, 9.5, start, end)))
    d.append(('+10.5T CK', crn.overNCornersOverAll(team, 10.5, start, end)))
    d.append(('+11.5T CK', crn.overNCornersOverAll(team, 11.5, start, end)))
    return d
   
def getTeamStats(team, start, end, formStr):
    d = getInfoTeam(team, start, end)
    if data.rounds_played > 4 and end > 4:
        if formStr == 1:
            d.append(('Form', teamFormLast5(team, end)))
            fxt = last5Fixtures(team, end)
            d.append(('Last 1', fxt[4]))
            d.append(('Last 2', fxt[3]))
            d.append(('Last 3', fxt[2]))
            d.append(('Last 4', fxt[1]))
            d.append(('Last 5', fxt[0]))
        else:
            form = teamFormLast5(team, end)
            d.append(('Last5Points', formPoints(form)))
    else:
        form = teamFormLastN(team, end, end)
        d.append(('Last5Points', formPoints(form)))
    d.append(('Goals Home', sh.goalsScoredHome(team, start, end)))
    d.append(('Goals Away', sh.goalsScoreAway(team, start, end)))
    d.append(('Shots Home', sh.avgShotsHome(team, start, end)))
    d.append(('Shots Away', sh.avgShotsAway(team, start, end)))
    d.append(('SOT Home', sh.avgSOTHome(team, start, end)))
    d.append(('SOT Away', sh.avgSOTAway(team, start, end)))
    d.append(('Fouls Home', df.foulsHome(team, start, end)))
    d.append(('Fouls Away', df.foulsAway(team, start, end)))
    d.append(('Yellow Home', df.yellowHome(team, start, end)))
    d.append(('Yellow Away', df.yellowAway(team, start, end)))
    d.append(('Red Home', df.redHome(team, start, end)))
    d.append(('Red Away', df.redAway(team, start, end)))
    d.append(('Goals Op Home', df.goalsConcededHome(team, start, end)))
    d.append(('Goals Op Away', df.goalsConcededAway(team, start, end)))
    d.append(('Shots Op Home', df.oponentShotsHome(team, start, end)))
    d.append(('Shots op Away', df.oponentShotsAway(team, start, end)))
    d.append(('SOT Op Home', df.oponentSOTHome(team, start, end)))
    d.append(('SOT Op Away', df.oponentSOTAway(team, start, end)))
    return d
    
def compareTeams(team1, team2, start, end, formStr):
    d1 = getTeamStats(team1, start, end, formStr)
    d2 = getTeamStats(team2, start, end, formStr)
    df = pd.DataFrame([d1, d2] )
    df = df.T
    pos = []
    for i in range(0, len(df)):
        pos.append(df[0][i][0])
        df[0][i] = df[0][i][1]
        df[1][i] = df[1][i][1]
    df['Property'] = pos
    df = df.set_index('Property')
    df = df.rename(columns = {0: team1, 1 : team2})
    return df.to_string()
