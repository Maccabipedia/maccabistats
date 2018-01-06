#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum


class CompetitionTypes(Enum):
    GOAL_SCORE = 'Score-Goal'
    RED_CARD = 'Red-Card'
    YELLOW_CARD = 'Yellow-Card'
    LINE_UP = 'Line-Up'
    SUBSTITUTION_IN = 'Substitution-In'
    SUBSTITUTION_OUT = 'Substitution-Out'
    GOAL_ASSIST = 'Assist-Goal'
