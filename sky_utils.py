#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# collection of astro calculation helpers
#
#

import os, sys, platform
import urllib, requests, json
import datetime
from pytz import timezone
import ephem

def iss_long_lat():
  try:
    """Get the ISS data from the tracking API"""
    url = "http://api.open-notify.org/iss-now.json"
    details = urllib.request.urlopen(url)
    result = json.loads(details.read())
    loc = result["iss_position"]
    lat = loc["latitude"]
    lon = loc["longitude"]
    return lon,lat
  except Exception as e:
    print(str(e))
    return 0,0

def compass_direction(azimuth):
  direction = ""
  '''
  N: 0
  NE: 45
  E: 90
  ES: 135
  S: 180
  SW: 225
  W: 270
  WN: 315
  '''
  if azimuth >= 0 and azimuth < 15:
    direction = "N"
  if azimuth >= 15 and azimuth < 30:
    direction = "NNE"
  if azimuth >= 30 and azimuth < 60:
    direction = "NE"
  if azimuth >= 60 and azimuth < 75:
    direction = "ENE"
  if azimuth >= 75 and azimuth < 105:
    direction = "E"
  if azimuth >= 105 and azimuth < 135:
    direction = "ESE"
  if azimuth >= 135 and azimuth < 150:
    direction = "SE"
  if azimuth >= 150 and azimuth < 165:
    direction = "SSE"
  if azimuth >= 165 and azimuth < 195:
    direction = "S"
  if azimuth >= 195 and azimuth < 225:
    direction = "SSW"
  if azimuth >= 225 and azimuth < 240:
    direction = "SW"
  if azimuth >= 240 and azimuth < 255:
    direction = "WSW"
  if azimuth >= 255 and azimuth < 285:
    direction = "W"
  if azimuth >= 285 and azimuth < 300:
    direction = "WNW"
  if azimuth >= 300 and azimuth < 330:
    direction = "NW"
  if azimuth >= 330 and azimuth < 345:
    direction = "NWN"
  if azimuth >= 345 and azimuth <= 360:
    direction = "N"
  return direction

def astro_night_times(theDate, latitude, longitude, debug):
  civil_night_start = None
  civil_night_end = None
  nautical_night_start = None
  nautical_night_end = None
  astronomical_night_start = None
  astronomical_night_end = None

  earth = ephem.Observer()
  earth.lat = str(latitude)
  earth.lon = str(longitude)
  earth.date = datetime.datetime.strptime(theDate, "%d.%m.%Y")
  sun = ephem.Sun()
  sun.compute()

  try:
    earth.horizon = "0"
    sunset = ephem.localtime(earth.next_setting(sun))
    sunrise = ephem.localtime(earth.next_rising(sun))

    earth.horizon = "-6"
    civil_night_start = ephem.localtime(earth.next_setting(sun))
    civil_night_end = ephem.localtime(earth.next_rising(sun))

    earth.horizon = "-12"
    nautical_night_start = ephem.localtime(earth.next_setting(sun))
    nautical_night_end = ephem.localtime(earth.next_rising(sun))

    earth.horizon = "-18"
    astronomical_night_start = ephem.localtime(earth.next_setting(sun))
    astronomical_night_end = ephem.localtime(earth.next_rising(sun))

  # ephem throws an "AlwaysUpError" when there is no astronomical twilight (which occurs in summer in nordic countries)
  except ephem.AlwaysUpError:
    if debug:
      print("No astronomical night at the moment: " + str(theDate))

  if debug:
    print("Civil night start: " + str(civil_night_start))
    print("Civil night end: " + str(civil_night_end))
    print("Nautical night start: " + str(nautical_night_start))
    print("Nautical night end: " + str(nautical_night_end))
    print("Astronomical night start: " + str(astronomical_night_start))
    print("Astronomical night end: " + str(astronomical_night_end))

  return civil_night_start, civil_night_end, nautical_night_start, nautical_night_end, astronomical_night_start, astronomical_night_end


