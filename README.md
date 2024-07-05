# ISS Sun/Moon Transit Detector
Simple ISS sun/moon transit detector. Makes use of the skyfield API to find out whether the ISS is visible in front of the sun or the moon from a specific location.
The next days ISS sightings above the location are compared to the sun's and the moon's positions at that time. If there is a match a message is printed.
The ISS location/sighting data is determined by its TLE data from http://celestrak.org/NORAD/elements/gp.php?INTDES=1998-067. This is time dependent and might change over time.


## Requirements
### Software
#### Requirements
- Linux
- Python3, pip3

#### Installations
```sudo apt install python3-pip```

```sudo pip3 install pyephem --break-system-packages```

```sudo pip3 install skyfield --break-system-packages```

```sudo pip3 install pytz --break-system-packages```


## Usage

```
python3 ISS_transit_detector.py --latitude 50.0 --longitude 10.0 --elevation 100 --iss_rise_limit 35 --range 0.03 --debug
```

## Output
The script output should be similar to this if the debug option is used:
```
...
ISS (ZARYA) catalog #25544 epoch 2024-07-03 04:53:42 UTC
A.D. 2024-Jul-03 04:53:42.3306 UTC
2024 Jul 04 03:02:16: rise above 20°
2024 Jul 04 03:04:27: culminate
2024 Jul 04 03:06:38: set below 20°
...
06.07.2024 01:26:19 rise above 20° in shadow
06.07.2024 01:28:27 culminate in sunlight
06.07.2024 01:30:37 set below 20° in sunlight

ISS rises/culminates/sets in sunlight:
**04.07.2024 03:02:16: ISS above 20° in E (ISS: -36.44, 101.75)**
**04.07.2024 03:04:27: ISS above 20° in E (ISS: -40.8, 102.29)**
**04.07.2024 03:06:38: ISS above 20° in E (ISS: -45.12, 102.79)**
...
**06.07.2024 01:28:27: ISS above 20° in E (ISS: -40.95, 92.46)**
**06.07.2024 01:30:37: ISS above 20° in E (ISS: -45.23, 93.13)**
...
No ISS transits expected.
```
