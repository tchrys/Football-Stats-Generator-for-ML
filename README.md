# Football-Stats-Generator-for-betting purpose

  This projects uses free csv files from http://www.football-data.co.uk/. I took the most important football championships(Premier League,
Serie A, La Liga, Ligue 1, Bundesliga - datasets from around 2006 to 2019, Portugal and Netherlands - last 2 years). Every csv contains
every game in that championship with the following main attributes:
- HomeTeam, AwayTeam, FTR(final time result), FTHG / FTAG (final time home / away goals)
- HTR(half time result), HTHG / HTAG(half time home / goals)
- HS / AS (home / away shots), HST / AST (home / away shots on target)
- HC / AC (home / away corners), HY / AY (home / away yellow cards), HR / AR (home / away red cards)

  Almost every function contains parameters start and end(from start matchday to end matchday)
  I've made all posible functions that came to my head(most of them are football-betting oriented):
- over N goals at home / away / overall (with N from 0.5 to 4.5)
- home / away / overall / firsthalf / last N matches league table
- fouls / yellow cards / opponent total shots(shots on target) / goals conceded at home / away / overall
- corners given / corners conceded / total corners at home / away / overall
- shots / shots on target at home / away / overall + handicap/both scored functions and all possible ratios
- histograms in ascending ordered containing all league teams for every stat that implies percentages
- plots that show evolution of points / league position / shots / shots conceded etc

  After all of this, I've tried to apply some Machine Learning techniques on these stats for betting purposes. For all champs, I've taken
every match and computed stats related to that stage(averages from matchday 1 to that matchday) for those teams. I've gathered these stats:
- position , points , home / away wins / draws / losses, form(points in last 5 games)
- goals / shots / shots on targets / fouls at home / away for that team and the team who played against it(to highlight somehow defensive
strength)
I've get 54 parameters for every game and made csv for main betting categories:
- 1 / X / 2 and 1X / X2 and for half time (home wins / draw / away wins
- half time or full time(PSF) - 1 / X / 2
- home scores, away scores, both score and for half time
- over 1.5 / 2.5 / 3.5 and for half time

  The last number of every line represents the label for that category: 1 if in that game that thing occured, otherwise 0
  These files are created hierarchically in /generated_data/ + 'country name' + /0 + 'year' + csv_filename
  I've made a function in csv_maker.py to gather more files for a specified category(1 , bothScored etc) for training. I've put some files
aside as test datasets(under 20% from all data). A big csv has around 17500 instances which is pretty good.
  I've tried some machine learning techniques on these training sets(logistic regression , build a deep network from scratch , build a
deep net with keras and svm technique) and I've uploaded the last two. There are too few parameters , so there is no big difference
between regression and a deep net.

The accuracy is better than random choice, but you cannot make a fortune from it(for instance, it has 66% accuracy for 1(home wins))
I've looked at some examples and realize it finds what is more likely to happen in many situations(for example finds out which is
the favourite team). I've found that the predictions are less accurate at the beginning of the championship because there is less
insight of teams strengths. For example, if Liverpool starts with a draw and Burnley with a win, Burnley is considered better. So we
need some data about players.

After this, I've made a fifa crawler to get more data, but I haven't introduced it yet to csv files. The crawler creates json-format
files for every team from a specified country and year, with its players attributes from FIFA.

You can  try to integrate player stats or your own ideas because there are a lot of insightful football statistics that can be aplied.
For example, statisticians found out that home advantage can be objectified by + 2 / 3 goals for home team.
