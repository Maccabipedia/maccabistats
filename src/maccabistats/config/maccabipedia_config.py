from dataclasses import dataclass


@dataclass
class _MaccabiPediaQueryGamesDataConfig:
    tables_names = 'Games_Catalog, Competitions_Catalog, Stadiums, Opponents'
    fields_names = 'Games_Catalog._pageName, Games_Catalog.Date, Games_Catalog.Hour, Games_Catalog.MatchDay, Games_Catalog.Season, Competitions_Catalog.Name=Competition, Games_Catalog.Leg, Opponents.OriginalName=Opponent, Games_Catalog.HomeAway, Stadiums.OriginalName=Stadium, Games_Catalog.ResultMaccabi, Games_Catalog.ResultOpponent, Games_Catalog.CoachMaccabi, Games_Catalog.CoachOpponent, Games_Catalog.Refs, Games_Catalog.Crowd, Games_Catalog.Technical'
    join_on = 'Games_Catalog.Competition=Competitions_Catalog.CompID, Games_Catalog.Stadium=Stadiums.CanonicalName, Games_Catalog.Opponent=Opponents.CanonicalName'


@dataclass
class _MaccabiPediaQueryGamesEventsConfig:
    tables_names = 'Games_Events'
    fields_names = '_pageName, Date, PlayerName, PlayerNumber, Minute, EventType, SubType, Team, Part'


@dataclass
class MaccabiPediaConfig:
    base_crawling_address = 'http://www.maccabipedia.co.il/index.php?title=Special:CargoExport&format=json'

    games_data_query = _MaccabiPediaQueryGamesDataConfig()
    games_events_query = _MaccabiPediaQueryGamesEventsConfig()
