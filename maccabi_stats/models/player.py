#!/usr/bin/python
# -*- coding: utf-8 -*-


class Player(object):
    def __init__(self, name, number):
        """
        :type name: str.
        :type number: int.
        """

        self.name = name
        self.number = number

    def __eq__(self, other):
        return self.name == other.name and self.number == other.number

    def __hash__(self):
        return hash((self.name, self.number))

    def __repr__(self):
        return "\nPlayer Name: {self.name}\n" \
               "Player Number: {self.number}\n\n".format(self=self)
