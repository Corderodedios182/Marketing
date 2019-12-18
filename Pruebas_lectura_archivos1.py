#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 12:01:38 2019

@author: carlos
"""

###########
#DATA CAMP#
###########

two_hurricanes = ["10/7/2016","6/21/2017"]

from datetime import date
from datetime import timedelta

# Create dates
two_hurricanes_dates = [date(2019, 12, 11), date(2019, 12, 15)]

two_hurricanes_dates[0].year

two_hurricanes_dates[1].weekday()

min(two_hurricanes_dates)

(two_hurricanes_dates[1] - two_hurricanes_dates[0]).days

td = timedelta(days = 4)

two_hurricanes_dates[0] + td

print(two_hurricanes_dates[0])

print( [date(2019, 12, 11).isoformat()] )

#ISO FORMAT 8601 

fechas = ['2019-12-01','2019-11-02','2019-12-30']

sorted(fechas)

date(2019,1,12).strftime("%Y/%m/%d")
