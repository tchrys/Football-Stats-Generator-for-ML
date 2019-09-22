from bs4 import BeautifulSoup as soup
import urllib
import ast
import io

# this file represents a crawler for fifaindex.com. It has three big functions:
# getAllTeams - it constructs the link regarding to country and year and
# access all teams from that page.
# getTeamInfo - it founds the table with team's players and get the hyperlink
# for each player
# getPlayerInfo: player abiliies start with ball control label, we must be
# careful beacuse we can have a goalkeeper and not a field player
# I've used BeautifulSoup as html parser.
# Fifaindex didn't change page design in last years so I hope this will be
# useful for FIFA 20 too
# output files have json format

currentYear = 2019
leagues = {'england' : 13, 'spain' : 53, 'france' : 16, 'germany' : 19,
           'italy' : 31, 'netherlands' : 10, 'portugal' : 308}

site_url = 'https://www.fifaindex.com'

def workRate(wkr):
    if wkr == 'High':
        return 3
    elif wkr == 'Medium':
        return 2
    else:
        return 1

qualities = {'Ball Skills' : 3, 'Defence' : 4, 'Mental' : 5, 'Passing' : 6,
             'Physical' : 7, 'Shooting' : 8, 'Goalkeeper' : 9}


def getPlayerInfo(my_url):
    req = urllib.request.Request(my_url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    page_html = con.read()
    con.close()
    page_soup = soup(page_html, "html.parser")
    res = dict()
    name = page_soup.h1.text.split("FIFA")[0]
    res['name'] = page_soup.h1.text.split("FIFA")[0]
    generalInfo = page_soup.findAll("div", {"class" : "card-body"})
    genStats = generalInfo[1].findAll("p", {"class" : ""})
    res['height'] = int(genStats[0].span.span.text.split(" ")[0])
    res['weight'] = int(genStats[1].span.span.text.split(" ")[0])
    res['position'] = genStats[5].span.text
    allStats = page_soup.find_all("div", {"class" : "card mb-5"})
    start = 2
    while "Ball Control" not in str(generalInfo[start].text):
        start += 1
    end = start + 6
    if res['position'] == 'GK':
        start = end
        end += 1
    for i in range(start, end):
        stats = allStats[i].find_all('p')
        for j in range(len(stats)):
            single_stat = stats[j].text.split(" ")
            ovr = single_stat[len(single_stat) - 1]
            string = ''
            for k in range(len(single_stat) - 1):
                string += single_stat[k] + ' '
            string = string[:-1]
            res[string] = ovr
    res.pop("Composure", None)
    return res, name

def getTeamInfo(my_url):
    print(my_url)
    req = urllib.request.Request(my_url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    page_html = con.read()
    con.close()
    page_soup = soup(page_html, "html.parser")
    res = dict()
    
    res['name'] = page_soup.h1.text.split("FIFA")[0]    
    players = dict()
    players_html = page_soup.findAll("table",
                            {"class" : "table table-players table-striped"})
    rows = players_html[0].findAll('tr')
    for i in range(1, len(rows)):
        link = site_url + rows[i].a['href']
        playerinfo, playername = getPlayerInfo(link)
        players[playername] = playerinfo
    res['players'] = players
    return res

def getUrl(country, year):
    my_url = 'https://www.fifaindex.com/teams/'
    if year != currentYear:
        year_ending = 'fifa' + str(year)[-2] + str(year)[-1]
        my_url += year_ending
    my_url += '/?league='
    my_url += str(leagues[country])
    my_url += '&order=desc'
    return my_url

def getAllTeams(country, year):
    my_url = getUrl(country, year)
    split_index = -2 if year == currentYear else -3
    req = urllib.request.Request(my_url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    page_html = con.read()
    con.close()
    page_soup = soup(page_html, "html.parser")
    teams_table = page_soup.findAll("table",
                                {"class" : "table table-striped table-teams"})
    rows = teams_table[0].findAll('tr')
    for i in range(1, len(rows)):
        team = rows[i].a['href'].split("/")[split_index]
        link = site_url + rows[i].a['href']
        team_dict = getTeamInfo(link)
        path = 'teams_' + country + '\\' + str(year) + '\\' + team
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(str(team_dict))

def readFromFile(filename):
    fl = open(filename, "r")
    str1 = fl.read()
    dict1 = ast.literal_eval(str1)
    return dict1


# use example

#getAllTeams('italy', 2019)

#for country in ['germany', 'france']:
#    for year in range(2011, 2020):
#        getAllTeams(country, year)
