#!/usr/bin/python
# -*- coding: utf-8 -*-


class Team(object):
    def __init__(self, name):
        """
        :type name: str.
        """
        self.name = name

    def __repr__(self):
        return "Name: {self.name} \n\n".format(self=self)
