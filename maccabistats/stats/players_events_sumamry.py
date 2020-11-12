import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats

logger = logging.getLogger(__name__)


class MaccabiGamesPlayersEventsSummaryStats(object):
    """
    This class will handle all players events statistics.
    """

    def __init__(self, maccabi_games_stats: MaccabiGamesStats):
        self.maccabi_games_stats = maccabi_games_stats

    @property
    def total_goals_assists_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.best_assisters)

    @property
    def total_goals_scoring_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers)

    @property
    def total_penalties_goals_scoring_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_penalty)

    @property
    def total_freekicks_goals_scoring_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_freekick)

    @property
    def total_own_goals_scoring_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_own_goal)

    @property
    def total_head_goals_scoring_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_head)

    @property
    def total_goals_involved_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.most_goals_involved)

    @property
    def total_yellow_card_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.most_yellow_carded)

    @property
    def total_red_card_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.most_red_carded)

    @property
    def total_captains_counted_for_maccabi_players(self) -> int:
        return sum(player[1] for player in self.maccabi_games_stats.players.most_captains)

    def compare_to_other_maccabi_games_stats(self, other) -> None:
        """
        Prints the comparison of the current (self) maccabi games stats to the given object.
        All of the shown numbers will be relevant to the other.
        If we will show for example "+2", means that self has two more items in the given field than "other".
        :type other: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        :rtype: str
        """

        def compared_field(field_name):
            return getattr(self, field_name) - getattr(other.players_events_summary, field_name)

        comparison = f"Comparing self <---> other events summary for maccabi players:\n\n" \
                     f"   Games Count: {len(self.maccabi_games_stats) - len(other)}\n" \
                     f"   Goals: {compared_field('total_goals_scoring_counted_for_maccabi_players')}\n" \
                     f"        By head: {compared_field('total_head_goals_scoring_counted_for_maccabi_players')}\n" \
                     f"        By freekick: {compared_field('tot    al_freekicks_goals_scoring_counted_for_maccabi_players')}\n" \
                     f"        By penalty: {compared_field('total_penalties_goals_scoring_counted_for_maccabi_players')}\n" \
                     f"        Own: {compared_field('total_own_goals_scoring_counted_for_maccabi_players')}\n" \
                     f"   Assists: {compared_field('total_goals_assists_counted_for_maccabi_players')}\n" \
                     f"   Goals involved: {compared_field('total_goals_involved_counted_for_maccabi_players')}\n" \
                     f"   Cards:\n" \
                     f"        Yellow cards: {compared_field('total_yellow_card_counted_for_maccabi_players')}\n" \
                     f"        Red cards: {compared_field('total_red_card_counted_for_maccabi_players')}\n" \
                     f"   Captains: {compared_field('total_captains_counted_for_maccabi_players')}\n"
        print(comparison)

    def __str__(self) -> str:
        return f"Total event counting for maccabi players:\n\n" \
               f"   Games Count: {len(self.maccabi_games_stats)}\n" \
               f"   Goals: {self.total_goals_scoring_counted_for_maccabi_players}\n" \
               f"        By head: {self.total_head_goals_scoring_counted_for_maccabi_players}\n" \
               f"        By freekick: {self.total_freekicks_goals_scoring_counted_for_maccabi_players}\n" \
               f"        By penalty: {self.total_penalties_goals_scoring_counted_for_maccabi_players}\n" \
               f"        Own: {self.total_own_goals_scoring_counted_for_maccabi_players}\n" \
               f"   Assists: {self.total_goals_assists_counted_for_maccabi_players}\n" \
               f"   Goals involved: {self.total_goals_involved_counted_for_maccabi_players}\n" \
               f"   Cards:\n" \
               f"        Yellow cards: {self.total_yellow_card_counted_for_maccabi_players}\n" \
               f"        Red cards: {self.total_red_card_counted_for_maccabi_players}\n" \
               f"   Captains: {self.total_captains_counted_for_maccabi_players}\n"

    def __repr__(self) -> str:
        return str(self)
