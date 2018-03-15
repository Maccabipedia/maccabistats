# Description 

Simple package which allow to figure out more about maccabi tel-aviv football team while manipulating statistics.
Atm all the data parsed from maccabi-tlv site.

# Examples

Loading all the games:
```
from maccabistats.stats.serialized_games import get_maccabi_stats
games = get_maccabi_stats()
```
or shorter

```
from maccabistats import get_maccabi_stats
games = get_maccabi_stats()
```

Trying to get only old home wins:
```
old_games = games.played_before("1.1.2000")
old_home_games = old_games.home_games
old_home_wins = old_home_games.maccabi_wins
```

or just:
```
games.played_before("1.1.2000").home_games.maccabi_wins
```



Show best scorers of 'games':
```
games.best_scorers
```

Or the same for old home wins:
```
old_home_wins.best_scorers
```



# Known issues

* Atm, players assist does not implemented.
* Players which opened as (captain or had different shirt number between games) will be counted as different players.
* Ignoring events after 120 min (in game_events_parser -> fully_game_time_without_penalties)


# Optimization 
 You can use 'use-disk-to-crawl-when-available' to crawl from diskwhen available, each page that will be crawled from internet wil be save on disk.
 
 You can get some of the html files from:
 https://mega.nz/#F!szxTUDRQ ( key will be available at forum.12p.co.il) 
 
 
# Versioning
ATM minor version change 0.X.0 may indicate API CHANGES.
 