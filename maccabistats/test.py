# -*- coding: utf-8 -*-


from maccabistats.parse.parse_from_all_sites import parse_maccabi_games_from_all_sites
from maccabistats.stats.serialized_games import serialize_maccabi_games, get_maccabi_stats
from maccabistats.models.player_game_events import GameEventTypes, GoalTypes

if __name__ == "__main__":

    g = get_maccabi_stats()
    a = g.most_loser_coach_by_percentage
    b = 6
    n = g.played_after("1.10.2000")
    b = n.best_scorers_by_penalty

    b = n[0].maccabi_team.scored_players_with_score_amount
    for i in n:
        for p in i.maccabi_team.players:
            goals = p.get_events_by_type(GameEventTypes.GOAL_SCORE)
            for g in goals:
                if g.goal_type != GoalTypes.UNKNOWN:
                    print(p)

a = 6
