# ISS Sun/Moon Transit Detector
Simple ISS sun/moon transit detector. Makes use of the skyfield API to find out whether the ISS is visible in front of the sun or the moon from a specific location.
The next days ISS sightings above the location are compared the the suns and the moons positions at that time. If there is a match a message is printed.
The ISS location/sighting data is determined by its TLE data from http://celestrak.org/NORAD/elements/gp.php?INTDES=1998-067. This is time dependent and might change over time.


## Requirements
### Software
#### Requirements
- Raspberry Pi OS, e.g. Bookworm
- Python3, pip3

#### Installations
```sudo apt install python3-pip```

```sudo pip3 install pyephem --break-system-packages```

```sudo pip3 install skyfield --break-system-packages```

```sudo pip3 install pytz --break-system-packages```


## Usage

```
python3 ISS_transit_detector.py --latitude 50.0 --longitude 10.0 --elevation 100 --limit 35 
```
