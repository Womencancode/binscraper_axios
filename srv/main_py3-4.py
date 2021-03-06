#!/usr/bin/env python3

import scrollphat
import fourletterphat
import json
from datetime import datetime
from time import sleep

def date_bin(currdate, currfulldate):
    firstLetter = ' '
    secondLetter = ' '
    match = False

    try:
        data = openJSON()
    except:
        binletters = "{}{}".format(firstLetter, secondLetter)
        fourletterphat.print_str("{}{}".format(currdate, binletters))
        fourletterphat.show()
        return

    for i in data:
        if i['bin'] == 'Grey Bin (General waste)':
            if i['date'] == currfulldate:
                firstLetter = 'G'
                match = True

    for i in data:
        if i['bin'] == '240Ltr Green Bin (Recycling)':
            if i['date'] == currfulldate:
                secondLetter = 'G'
                match = True

    for i in data:
        if i['bin'] == '240Ltr Brown Bin (Garden waste)':
            if i['date'] == currfulldate:
                secondLetter = 'B'
                match = True
    
    binletters = "{}{}".format(firstLetter, secondLetter)
    fourletterphat.print_str("{}{}".format(currdate, binletters))
    if match:
        binday = True
    else:
        binday = False
    
    fourletterphat.show()

def weekday(currday):
    scrollphat.write_string("{}".format(currday), 0)
    
def clearHats():
    scrollphat.clear()
    fourletterphat.clear()

def dimHats():
    fourletterphat.set_brightness(0)
    scrollphat.set_brightness(1)

def brightenHats():
    fourletterphat.set_brightness(14)
    scrollphat.set_brightness(14)

def openJSON():
    with open("../binDates.json", "r") as read_file:
        data = json.load(read_file)
    return data


delta_day = 0
delta_hour = 0
binday = False


weekdays = {
        0:"Mo",
        1:"Tue",
        2:"We",
        3:"Thu",
        4:"Fri",
        5:"Sat",
        6:"Sun"
        }

dimHats()

while True:
    now_hour = datetime.now().hour

    if delta_hour != now_hour:

        currday = datetime.today().weekday()
        currdate = datetime.today().day
        currfulldate = datetime.today().strftime('%d/%m/%Y')

        if currday > delta_day:
            delta_day = currday

        weekday(weekdays[currday])
        date_bin(currdate, currfulldate)

    delta_hour = now_hour

    sleep(60)

    # if delta_hour > 0 or delta_hour < 7:
    #     clearHats()

    # if delta_hour > 7 and not binday:
    #     dimHats()
    # if delta_hour > 7 and binday or delta_hour < 8 and binday:
    #     brightenHats()
    # if delta_hour > 8 and binday:
    #     dimHats()

