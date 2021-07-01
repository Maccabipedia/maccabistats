# MaccabiPedia data

The nearby files contains the data we have in MaccabiPedia (https://maccabipedia.co.il).  
Some of the fields may be empty (such as stadiums or goal-type) or contain partial data (such as assist) -  
take this into consideration while analyzing the data, we are still trying to fill every data we can.

# Intro

Each game in MaccabiPedia is built from many "player events", each one is an occurrence from the game,  
such as: Player started the game as part of the line-up, got a yellow card, was the captain and so on.

Each record in the attached files contains two parts merged together:  
1. Player Data
    * player_name
    * player_number
    * player_time_occur: in this format: "h:mm:ss", the lowest resolution in minutes
    * player_event_type
        1. ScoreGoal
        1. RedCard
        1. YellowCard
        1. LineUp
        1. SubstitutionIn
        1. SubstitutionOut
        1. AssistGoal
        1. Captain
        1. PenaltyMissed
        1. PenaltyStopped: Goalkeeper event only
        1. Benched
        1. Unknown
    * player_goal_type:
        1. FreeKickGoal
        1. PenaltyGoal
        1. HeaderGoal
        1. OwnGoal
        1. BicycleKickGoal
        1. NormalGoal: The goal is not relevant for every other category
        1. UnknownGoal
    * player_assist_type:
        1. NormalAssist: The assist is not relevant for every other category
        1. FreeKickAssist
        1. CornerAssist
        1. ThrowInAssist
        1. PenaltyWinningAssist
        1. UnknownAssist
    * player_team: The name of the team this player belongs to
2. Game Data
    * stadium
    * date: lowest resolution will be mostly - hour
    * crowd
    * referee
    * competition: We write the specific competition name, for example: "Ligat ha'al" and "Liga leumit" will count as different competitions, you can merge them in your analytics if such required
    * fixture: Which round in the competition is played?
    * season
    * technical_result: Whether this game ends by forfeit of one of the team, or in any non-regular decision, In this case the displayed scores may not reflect the final decided result, but the in-game score
    * home_team_name
    * home_team_score
    * home_team_coach
    * away_team_name
    * away_team_score
    * away_team_coach
    
    
    
# Code
Make sure to check out our Github repositories at:
* [MaccabiStats](https://github.com/Maccabipedia/maccabistats)
* [MaccabiPedia org](https://github.com/Maccabipedia)
    
# Contact Us
We will be glad to help with any question or hear your new ideas and requests,  
you can contact us at:
* [MaccabiPedia Telegram](https://t.me/MaccabiPedia)
* maccabipedia@gmail.com
* [MaccabiPedia website](https://www.maccabipedia.co.il/עמוד_ראשי)
