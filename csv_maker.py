# -*- coding: utf-8 -*-

import data
import teamstats as tst
import pandas as pd
import os

# this containers were explained in data.py
leagues = ['spain0', 'italy0', 'england0',
           'germany0', 'france0', 'portugal0', 'netherlands0']

trainleagues = ['italy0', 'england0', 'germany0', 'france0',
           'portugal0', 'netherlands0']

errorYears = {'england0' : [2014], 'france0' : [2011, 2016],
              'germany0' : [], 'italy0' : [2012, 2014, 2015, 2016],
              'netherlands0' : [], 'portugal0' : [], 'spain0' : []}

startYears = {'england0' : 2004, 'france0' : 2007, 'germany0' : 2006,
              'italy0' : 2006, 'netherlands0' : 2017, 'portugal0' : 2017,
              'spain0' : 2005}


# this functions returns a h2h data frame for team1 and team2 with stats from
# matchday start to matchday end(not for every round, but the average-shots,
# corners, yellow cards etc)
def compareTeamsDataFrame(team1, team2, start, end):
    d1 = tst.getTeamStats(team1, start, end, 0)
    d2 = tst.getTeamStats(team2, start, end, 0)
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
    return df

# this function takes the data frame from the previous function and convert it
# to csv format
def h2hCsvStats(team1, team2, end):
    df = compareTeamsDataFrame(team1, team2, 1, end)
    df_len = len(df)
    csv_string = ''
    for i in range(df_len):
        csv_string += ''.join([str(df.iloc[i][0]), ',', str(df.iloc[i][1]), ','])
    csv_string = csv_string[:-1]
    return csv_string

# these short functions compute the output for game d.
# that output will represent the label in a ML context
def homeScoresBool(d):
    return int(int(d['FTHG']) > 0)

def awayScoresBool(d):
    return int(int(d['FTAG']) > 0)

def homeScoresHTBool(d):
    return int(int(d['HTHG']) > 0)

def awayScoresHTBool(d):
    return int(int(d['HTAG']) > 0)

def bothScoredBool(d):
    return int(homeScoresBool(d) and awayScoresBool(d))
    
def overNBool(d, n):
    return int(int(d['FTAG']) + int(d['FTHG']) > n)

def overHTBool(d, n):
    return int(int(d['HTAG']) + int(d['HTHG']) > n)

def underNBool(d, n):
    return int(int(d['FTAG']) + int(d['FTHG']) < n)

def underHTBool(d, n):
    return int(int(d['HTAG']) + int(d['HTHG']) < n)
    
def over15Bool(d):
    return overNBool(d, 1.5)

def over25Bool(d):
    return overNBool(d, 2.5)

def over35Bool(d):
    return overNBool(d, 3.5)

def over05HTBool(d):
    return overHTBool(d, 0.5)

def over15HTBool(d):
    return overHTBool(d, 1.5)

def over25HTBool(d):
    return overHTBool(d, 2.5)

def under15Bool(d):
    return underNBool(d, 1.5)

def under25Bool(d):
    return underNBool(d, 2.5)

def under35Bool(d):
    return underNBool(d, 3.5)

def under05HTBool(d):
    return underHTBool(d, 0.5)

def under15HTBool(d):
    return underHTBool(d, 1.5)

def under25HTBool(d):
    return underHTBool(d, 2.5)

def resultBool(d, winner, prop):
    return int(d[prop] == winner)

def homeWinsBool(d):
    return resultBool(d, 'H', 'FTR')

def awayWinsBool(d):
    return resultBool(d, 'A', 'FTR')

def drawResultBool(d):
    return resultBool(d, 'D', 'FTR')

def homeHTBool(d):
    return resultBool(d, 'H', 'HTR')

def awayHTBool(d):
    return resultBool(d, 'A', 'HTR')

def drawHTBool(d):
    return resultBool(d, 'D', 'HTR')

def Bool1X(d):
    return int(d['FTR'] == 'H' or d['FTR'] == 'D')

def BoolX2(d):
    return int(d['FTR'] == 'A' or d['FTR'] == 'D')

def Bool12(d):
    return int(d['FTR'] == 'H' or d['FTR'] == 'A')

def HT1XBool(d):
    return int(d['HTR'] == 'H' or d['HTR'] == 'D')

def HTX2Bool(d):
    return int(d['HTR'] == 'A' or d['HTR'] == 'D')

def HT12Bool(d):
    return int(d['HTR'] == 'H' or d['HTR'] == 'A')

def homePSFBool(d):
    return int(d['FTR'] == 'H' or d['HTR'] == 'H')

def drawPSFBool(d):
    return int(d['FTR'] == 'D' or d['HTR'] == 'D')

def awayPSFBool(d):
    return int(d['FTR'] == 'A' or d['HTR'] == 'A')

# this dictionary maps function names(the things we can bet on) to function   
csvResults = {'bothScored' : bothScoredBool, 'homeScores' : homeScoresBool,       
        'awayScores' : awayScoresBool, 'over15' : over15Bool,
        'over25' : over25Bool, 'over35' : over35Bool,
        'homeWins' : homeWinsBool, 'awayWins' : awayWinsBool,
        'drawResult' : drawResultBool, 'homeHT' : homeHTBool,
        'awayHT' : awayHTBool, 'drawHT' : drawHTBool,
        'homePSF' : homePSFBool, 'awayPSF' : awayPSFBool,
        'drawPSF' : drawPSFBool, 'over05HT' : over05HTBool,
        'over15HT' : over15HTBool, 'over25HT' : over25HTBool,
        'under15' : under15Bool, 'under25' : under25Bool,
        'under35' : under35Bool, 'under05HT' : under05HTBool,
        'under15HT' : under15HTBool, 'under25HT' : under25HTBool,
        '1X' : Bool1X, 'X2' : BoolX2, '12' : Bool12, 'HT1X' : HT1XBool,
        'HTX2' : HTX2Bool,'HT12' : HT12Bool,'homeHTScores' : homeScoresHTBool,
        'awayHTScores' : awayScoresHTBool}
    
# this function returns the list of bools(True / False) for an entire
# championship for the specified function
def allMatchesListProp(function):
    f = csvResults[function]
    results = []
    for i in range(data.games_played):
        results.append(f(data.mpg[i]))
    return results

# this function is the complementary of the previous one(it returns the list
# of stats for the entire championship). Note that for a game in matchday x
# we get the stats from stage 1 to stage x - 1
def cacheh2h():
    h2h_res = []
    for i in range(data.games_played):
        crtRound = data.getcurrentRoundFromNrGame(i)
        homeTeam = data.mpg[i]['HomeTeam']
        awayTeam = data.mpg[i]['AwayTeam']
        csv_string = h2hCsvStats(homeTeam, awayTeam, crtRound - 1)
        h2h_res.append(csv_string)
    return h2h_res


def makeCsvForProp(function, h2h_res):
    final_string = ''
    results = allMatchesListProp(function)
    for i in range(data.games_played):
        final_string += str(results[i]) + ',' + h2h_res[i] + '\n'
    return final_string[:-1]

#this function creates the csv file for the specified function
def outputCsvForProp(function, h2h_res):
    big_string = makeCsvForProp(function, h2h_res)
    filename = 'csv_' + function
    print(filename)
    d = os.getcwd() + '\generated_data\\' + data.gen_data_folder + filename
    print(d)
    with open(d, 'w') as my_csv:
        my_csv.write(big_string)
        my_csv.close()
        
def outputCsvForAllProps():
    h2h_res = cacheh2h()
    for prop in csvResults.keys():
        outputCsvForProp(prop, h2h_res)
    
# this function makes a big csv for property 'function' with all matches from
# trainleagues, starting with starYears and skipping errorYears. For every
# league and year it opens the coresponding file and write the content to the
# big file
def createBigCsv(function):
    path = os.getcwd()
    filename = 'csv_' + function
    fl = open(filename, "w")    
    for country in trainleagues:
        league = int(country[-1])
        for year in range(startYears[country], 2019):
            if year not in errorYears[country]:
                country = country[:-1]
                path = os.getcwd()
                countryupp = country[0]
                countryupp = chr(ord(countryupp) - 32)
                gen_data_folder = country + '\\' + str(league) + '\\' + str(year) + '\\'
                filename = 'csv_' + function
                relPath = '\generated_data\\' + gen_data_folder + filename
                path = os.getcwd() + relPath
                with open(path, 'r') as my_csv:
                    s = my_csv.read()
                    fl.write(s)
                    if country == 'netherlands' and year == 2018:
                        fl.close()
                    else:
                        fl.write('\n')
                country = country + str(league)
                print(path)

                
# example             
#createBigCsv('over25')