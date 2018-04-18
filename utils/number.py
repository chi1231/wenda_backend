#!/usr/bin/env python
# encoding: utf-8



def get_kilo_from_number(number):
    if number >= 1000:
        return "%.1fk" % (number / 1000)

    return "%d" % number
