#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Find out whether ISS is visible in front of sun or moon above a location
#
# https://rhodesmill.org/skyfield/earth-satellites.html
#
import os, sys, platform
import urllib, requests, json
import datetime
from skyfield.api import load, wgs84, N, W, EarthSatellite
from pytz import timezone
import ephem
import optparse

parser = optparse.OptionParser()

parser.add_option('-a', '--latitude',
    action="store", dest="latitude",
    help="latitude", default=+49.90072)
parser.add_option('-o', '--longitude',
    action="store", dest="longitude",
    help="longitude", default=+8.68549)
parser.add_option('-e', '--elevation',
    action="store", dest="elevation",
    help="elevation", default=144)
parser.add_option('-l', '--limit',
    action="store", dest="limit",
    help="limit", default=20)
parser.add_option('-d', '--debug',
    action="store_true", dest="debug",
    help="Enable debug output", default=False)

options, args = parser.parse_args()

if options.debug:
  debug = options.debug
else:
  debug = False
verbose = False #True

if options.latitude:
  latitude = float(options.latitude)
if options.longitude:
  longitude = float(options.longitude)
if options.elevation:
  elevation = int(options.elevation)
if options.limit:
  iss_limit = int(options.limit)

europe = timezone('Europe/Berlin')

now = datetime.datetime.now()
theDate = now.strftime("%d.%m.%Y")
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=2)


def iss_now():
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

def astro_night_times(theDate):
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

civil_night_start, civil_night_end, nautical_night_start, nautical_night_end, astronomical_night_start, astronomical_night_end  = astro_night_times(theDate)

def check_iss_sun_moon(iss, timestamp, limit, location):
  try:
    t_sun = ts.utc(int(timestamp.strftime("%Y")), int(timestamp.strftime("%m")), int(timestamp.strftime("%d")), int(timestamp.strftime("%H")), int(timestamp.strftime("%M")), int(timestamp.strftime("%S")))
    sun = eph['sun']
    earth = eph['earth']
    moon = eph['moon']
    location_ = earth + wgs84.latlon(latitude_degrees=float(latitude) * N, longitude_degrees=float(longitude) * W, elevation_m=elevation)
    d = location_.at(t_sun)
    m = d.observe(moon).apparent()
    s = d.observe(sun).apparent()
    alt_sun, az_sun, distance_sun = s.altaz()
    if verbose:
      print("Sun position: " + str(alt_sun.degrees) + ", az: " + str(az_sun.degrees)) # + "( from " + str(latitude) + ", " + str(longitude) + ")")
    alt_moon, az_moon, distance_moon = m.altaz()
    if verbose:
      print("Moon position: " + str(alt_moon.degrees) + ", az: " + str(az_moon.degrees)) # + "( from " + str(latitude) + ", " + str(longitude) + ")")
    difference = iss - location
    topocentric = difference.at(t_sun)
    #print(topocentric.position.km)
    alt_iss, az_iss, distance = topocentric.altaz()
    #ra, dec, distance = topocentric.radec(epoch='date')
    if verbose:
      print("ISS position: " + str(alt_iss.degrees) + ", az: " + str(az_iss.degrees)) # + "( from " + str(latitude) + ", " + str(longitude) + ")")

    #nauticalnighttimestart = timestamp.replace(hour=int(nautical_night_start.strftime("%H")), minute=int(nautical_night_start.strftime("%M")), second=0, microsecond=0)
    #nauticalnighttimeend = timestamp.replace(hour=int(nautical_night_end.strftime("%H")), minute=int(nautical_night_end.strftime("%M")), second=0, microsecond=0)
    # consider night time
    #if nauticalnighttimestart <= timestamp  or timestamp <= nauticalnighttimeend:
        
    # compare positions
    if alt_sun.degrees-limit < alt_iss.degrees < alt_sun.degrees+limit and az_sun.degrees-limit < az_iss.degrees < az_sun.degrees+limit:
      msg = "** ISS transit alert: " + timestamp.strftime('%d.%m.%Y %H:%M:%S') + ": ISS might be in front of the sun in " + str(compass_direction(az_iss.degrees)) + " (ISS: " + str(round(alt_iss.degrees,2)) + ", " + str(round(az_iss.degrees,2)) + " / Sun: " + str(round(alt_sun.degrees,2)) + ", " + str(round(az_sun.degrees,2)) + ")**"
      if debug:
        print(msg)
      return msg
    elif alt_moon.degrees-limit < alt_iss.degrees < alt_moon.degrees+limit and az_moon.degrees-limit < az_iss.degrees < az_moon.degrees+limit:
      msg = "** ISS transit alert: " + timestamp.strftime('%d.%m.%Y %H:%M:%S') + ": ISS might be in front of the moon in " + str(compass_direction(az_iss.degrees)) + " (ISS: " + str(round(alt_iss.degrees,2)) + ", " + str(round(az_iss.degrees,2)) + " / Moon: " + str(round(alt_moon.degrees,2)) + ", " + str(round(az_moon.degrees,2)) + ")**"
      print(msg)
      return msg
    else:
      msg = "**" + timestamp.strftime('%d.%m.%Y %H:%M:%S') + ": ISS above " + str(iss_limit) + "° in " + str(compass_direction(az_iss.degrees)) + " (ISS: " + str(round(alt_iss.degrees,2)) + ", " + str(round(az_iss.degrees,2)) + ")**"
      if debug:
        print(msg)
      #SMArtHomeUtils().telegram_bot_sendtext(msg)
  except Exception as e:
    print(str(e))


if __name__ == '__main__':
  '''
  # ISS now
  try:
    lon, lat = iss_now()
    if debug:
      print("ISS now: " + str(lon) + ", " + str(lat))
  except Exception as e:
    print(str(e))
  '''
  try:
    max_days = 7.0         # download again once 7 days old
    name = "stations.csv"  # custom filename, not 'gp.php' 
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=csv"

    if not load._exists(name) or load.days_old(name) >= max_days:
      load.download(url, filename=name)
    
    ts = load.timescale()

    #http://celestrak.org/NORAD/elements/gp.php?INTDES=1998-067
    line1 = "1 25544U 98067A   24185.20396216  .00014229  00000+0  26067-3 0  9990"
    line2 = "2 25544  51.6391 235.9633 0010118  24.5360  42.7122 15.49535041461038"
    iss = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
    if debug:
      print(iss)
      print(iss.epoch.utc_jpl())

    location = wgs84.latlon(float(latitude), float(longitude))
    
    t0 = ts.utc(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")))
    t1 = ts.utc(int(tomorrow.strftime("%Y")), int(tomorrow.strftime("%m")), int(tomorrow.strftime("%d")))
    t, events = iss.find_events(location, t0, t1, altitude_degrees=20.0)

    event_names = ["rise above " + str(iss_limit) + "°", "culminate", "set below " + str(iss_limit) + "°"]
    for ti, event in zip(t, events):
      name = event_names[event]
      #print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)
      if debug:
        print(ti.astimezone(europe).strftime('%Y %b %d %H:%M:%S') + ": " + str(name))

    eph = load("de421.bsp")
    sunlit = iss.at(t).is_sunlit(eph)
    
    #print("Nautical night: "  + str(nautical_night_start) + "-" + str(nautical_night_end))
    
    rise_above_30_in_sunlight = []
    rise_above_30_in_shadow = []
    for ti, event, sunlit_flag in zip(t, events, sunlit):
      name = event_names[event]
      if sunlit_flag:
        state = "in sunlight"
      else:
        state = "in shadow"

      timestamp = ti.astimezone(europe)
      if debug:
        print(timestamp.strftime('%d.%m.%Y %H:%M:%S') + " " + str(name) + " " + str(state))
      if (name == "rise above " + str(iss_limit) + "°" or name == "culminate" or name == "set below " + str(iss_limit) + "°") and state == "in sunlight":
        rise_above_30_in_sunlight.append(timestamp)
      if name == "rise above " + str(iss_limit) + "°" and state == "in shadow":
        rise_above_30_in_shadow.append(timestamp)

    ISS_transits = []
    if debug:
      print("")
      print("ISS rises/culminates/sets in sunlight:")
    for i in rise_above_30_in_sunlight:
      transit_alarm = check_iss_sun_moon(iss, i, 0.3, location)
      if transit_alarm:
        ISS_transits.append(transit_alarm)
    if ISS_transits:
      print("ISS transits expected:")
      for i in ISS_transits:
        print(i)
    else:
      print("No ISS transits expected.")
  except Exception as e:
    print(str(e))


