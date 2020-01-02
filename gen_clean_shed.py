#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script to generate a cleaning schedule in LaTeX or plain csv.
'''

# General settings:
year = 2019
switch_week = 0 # first week of the summer holidays
output_format = 'latex'
filename = 'schedule.tex'

# LaTeX-specific settings:
language = 'en'
holiday_weeks = [1,10,28,29,30,31,32,33,34,35,52]
filename_header = 'header.tex'
filename_footer = 'footer.tex'

from datetime import date, timedelta
import locale
import ast

def get_week_days(week):
    d = date(year,1,1)
    if(d.weekday()>3):
        d = d + timedelta(7-d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week-1)*7)
    return d + dlt,  d + dlt + timedelta(days=6)

'''
Writes the contents of inf to of, substituting tokens that appear in strings.
'''
def insert_file(inf, of, strings):
    file = open(inf, 'r')
    for line in file:
        for token, string in strings.items():
            line = line.replace(token, string)
        of.write(line)
    return

'''
Writes the contents line to of.
The necessary conversions are made in case the output format is latex.
For csv, no changes are necessary.
'''
def output_line(of, line):
    if output_format == 'csv':
        # the line is already in the correct format:
        # weekno., chore1, chore2, chore3, chore4
        # where choreX denotes the responsible for the chore, if any
        of.write(line + '\n')

    elif output_format == 'latex':
        # convert the line stepwise to a LaTeX tabular row
        # example:
        # 1 & jan 2 & jan 8 & E \check & F \check &  & G \check \\

        i = int(line.split(',', 1)[0]) # the weekno.

        # highlight the row if it is a holiday week
        if i in holiday_weeks:
            # use different tints for even and odd weeks
            # note: the package xcolor does not seem to support
            # multiple alternating colorschemes in one table
            if i % 2 == 0:
                of.write('\\rowcolor{\evencolor}\n')
            if i % 2 == 1:
                of.write('\\rowcolor{\oddcolor}\n')

        # calculate the dates from the week number
        of.write(str(i) + ' & ' +  get_week_days(i)[0].strftime('%b'))
        of.write(' ' + get_week_days(i)[0].strftime('%d').lstrip('0'))
        of.write(' & ' + get_week_days(i)[1].strftime('%b'))
        of.write(' ' + get_week_days(i)[1].strftime('%d').lstrip('0'))

        # the remainder can simply be substituted
        rest = line.split(',', 1)[-1]
        rest = rest.replace(',,', ', & ')
        rest = rest.replace(',', ' \\check & ')
        of.write(' & ' + rest + ' \\check ')
        if i != 0 and i == switch_week:
            of.write('\\sidenotetrue\\tikzmark{sidenote} ' )
        of.write('\\\\\n')
    return

'''
Determines which room is doing what chore for all weeks of the year.
'''
def generate_schedule(of):
    rooms = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H']] # the suffixes
    turn = [3, 1] # 0,3 means A,H etc.

    # i is the weeknumber
    for i in range(1,53):
        line = '' 

        # at the beginning of the summer holidays,
        # the alternation of sides is swapped
        if switch_week == 0:
            switcheroo = (i % 16) // 8
            side = (i-switcheroo) % 2
        elif i < switch_week:
            side = (i-1) % 2
        else:
            side = i % 2

        line += str(i) # weeknumber

        # determine three chores
        for j in range(3):
            if i % 2 == 0 and j == 1:
                # leave chore 2 blank
                line += ','
            line += ',' + rooms[side][turn[side]]
            if i % 2 == 1 and j == 1:
                # leave chore 3 blank
                line += ','
            turn[side] += 1
            if turn[side] == 4:
                turn[side] = 0

        output_line(of, line)
    return

'''
The main function.
'''
def main():
    of = open(filename, 'w')

    if output_format == 'csv':
        generate_schedule(of)

    elif output_format == 'latex':
        # set locale for the name of the month
        if language == 'nl':
            locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
        else:
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

        # load translation strings
        with open('strings-' + language + '.dict','r') as inf:
            strings = ast.literal_eval(inf.read())

        # insert the header
        insert_file(filename_header, of, strings)

        # insert the table body
        generate_schedule(of)

        # insert the footer
        insert_file(filename_footer, of, strings)

main()
