# Description 

Simple package which allow to figure out more about maccabi tel-aviv football team while manipulating statistics.
Atm all the data parsed from maccabi-tlv site.


# TL;DR
You can get the serialized maccabi games from [mega](https://mega.nz/#F!iX4y1CrJ!sCRXAGcImG8nK4jk8hUMEA)
(separate by maccabistats version).
after that you can just load the games:

```
from maccabistats import get_maccabi_stats
games = get_maccabi_stats(your_maccabi.games_file_path)  # Use the local path you've downloaded the file from mega.
```

You might want to use:
```
games = games.get_first_league_games()
```
because there are not only league games.

now, enjoy :)

# Manipulating maccabi statistics

  ### Loading games
```
>>> from maccabistats import get_maccabi_stats
>>> games = get_maccabi_stats()  # From default folder path (Home folder - %userprofile%)
>>> games = get_maccabi_stats(r"C:\maccabi\maccabi.games")  # From local custom file path
```

Each list of games is from the same type - MaccabiGamesStats.  
All the below manipulating can be done on every sub-category of games, like:  
old_games, old_home_games and old_home_wins.  
 
Getting only old home wins can be done in this way:
```
>>> old_games = games.played_before("1.1.2000")
>>> old_home_games = old_games.home_games
>>> old_home_wins = old_home_games.maccabi_wins
>>>
>>> or just:
>>> games.played_before("1.1.2000").home_games.maccabi_wins
```


  ### Basic usage
```
>>> games.averages.goals_for_maccabi  # Avg goals for maccabi, for all the games in the list.
>>> games.results.wins_percentage  #  the win % from the games in the list.
>>>
>>> game.get_games_* = use to filter games.
>>> Lets combine all, wins % against hapoel haifa in league games:
>>> game.get_first_league_games().get_games_against_team("הפועל חיפה").results.wins_percentage
```


   ### Players
All of the names are very intuitive, some examples:
```
>>> games.players.best_scorers
>>> games.players.get_most_winners_by_percentage()
>>> games.players.most_played
>>>
>>> Getting top 5 scored players in league derby:
>>> games.get_first_league_games().get_games_against_team("הפועל תל אביב").players.best_scorers[0:5]
```

   ### Coaches and Referees
You can get the win\lose percentages of each one just by:
```
>>> games.coaches.most_winner_coach_by_percentage
>>> games.referees.best_referee_by_percentage[0:2]  # Top 2 referees (in all maccabi games history).
>>>
>>> Getting best derby coaches:
>>> games.get_first_league_games().get_games_against_team("הפועל תל אביב").coaches.most_winner_coach_by_percentage
```


   ### Comebacks
You can get the craziest maccabi comebacks:
```
>>> games.comebacks.won_from_exactly_two_goal_diff()
>>> games.comebacks.won_from_exactly_x_goal_diff(goals=3)  # Wow!
```

   ### Streaks
You can get the longest (or by streak length) streaks of any subset of maccabi games:
```
>>> games.streaks.get_longest_* = use to get the longest streak by condition, like:
>>> games.streaks.get_longest_clean_sheet_games()  #  Games in a row without goal against maccabi.
>>>
>>> games.streak.get_similar_* = use to get similar with len of at least X and by condition.
>>> # All the unbeaten rows of at least len of 20:
>>> games.streaks.get_similar_unbeaten_streak_by_length(minimum_streak_length=20)   
```

   ### Players Streaks
You can get the longest players streaks of any subset of maccabi games:
```
>>> # Use to get the players with best streak of scoring (count the game only if the player played).
>>> games.players_streaks.get_players_with_best_goal_scoring_streak()
>>>
>>> # Same for unbeaten:
>>> games.players_streaks.get_players_with_best_unbeaten_streak()
```


   ### Seasons
You can get the games grouped by seasons sorted by any condition, such as:
```
>>> seasons = games.seasons.get_seasons_stats()  # At default the season will be sorted by year.
>>> seasons.sort_by_wins_percentage()  # Sort the season by winning percentage, you should print the season object).
>>> seasons  # Print it
```


# Crawling maccabi games

When crawling maccabi games each page will be saved on your disk to allow optimization for the next time.
To serialize maccabi games (it might take some time), use:
```
>>> from maccabistats import serialize_maccabi_games
    # The object will be serialized to home folder (%userprofile%) with its version and the current date.
>>> serialize_maccabi_games(maccabi_games_stats_object)
```

Manual-fixes will be run after crawling is finished and before serializing to disk.

You can 'use_multi-process-crawl' from settings to allow multi-processing,  
BUT atm logging does not support multi-processing, so don't use that if you need to debug.


# Manual fixes

There are some information that need to be fix manually.  
When serializing maccabi games that done automatically.
If you Add anything to run_general_fixes, you can re-run it by:
```
>>> from maccabistats import get_maccabi_stats, run_general_fixes, serialize_maccabi_games
>>> 
>>> games = get_maccabi_stats()
>>> new_games = run_general_fixes(games)
>>> serialize_maccabi_games(new_games)
```

# Logging

All of the log files will be saved at 'maccabistats\logs' folder under the user home folder (%userprofile%)
There are several log files, each one has this pattern - maccabistats-{suffix}.log (at the mentioned folder): 

* all - save all log levels
* info - save just the info log level
* warning - save just the warn log level
* exception - save just exceptions (log.exception)
* stdout - not a file but log handler that print to stdout (info level +) 


# Known issues

* Ignoring events after 120 min (in game_events_parser -> fully_game_time_without_penalties)
* Logging with multi-process crawling mode isn't working.


# Optimization 
* You can use 'use-disk-to-crawl-when-available' to crawl from disk when available, each page that will be crawled from internet wil be save on disk. 
* For the first time, you can get some of the html files from: https://mega.nz/#F!szxTUDRQ ( key will be available at forum.12p.co.il)
* You can reduce logging when crawling by use :
```
>>> from maccabistats import faster_logging
>>> faster_logging() will disable the stdout & debug handlers.
```


# Errors Finder

Manual check for errors might be helpful, this is can be done by:
```
>>> from maccabistats import get_maccabi_stats
>>> from maccabistats.error_finder.error_finder import ErrorsFinder
>>> games = get_maccabi_stats()
>>> e = ErrorsFinder(games)
>>> e.get_all_errors_numbers()  # run all the manual errors exists
```


# MaccabiPedia Source

You can manipulate [MaccabiPedia](http:\\www.maccabipedia.co.il) data by downloading it and then loading it 
(You may have to install some 'advanced' packages such as pywikibot), as the following:

```
>>> from maccabistats import run_maccabipedia_source
>>>
>>> # You should run this once a while, this is a heavy action to do:
>>> maccabipedia = run_maccabipedia_source()
>>> # Now you can manipulate maccabipedia data as explain above (its MaccabiGamesStats object, referred as "games" above") 
```

