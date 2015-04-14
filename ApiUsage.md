## API Usage ##
Install the module in the usual fashion, then try it out in Python

```
>>> import Weather
>>> Weather.fetch()
```

This will take a minute while it fetches the current observations from NOAA.

_Hint: if you run this say every hour or so (say in a cronjob) it will keep the observation base current._

Now find a station to parse. Station takes a NOAA station identifier. To find stations by location (city,state,zip,etc) look to LocalizationIntegration

Get a list of available stations by identifier

```
>>> Weather.stations()
<generator object at 0xb7c39eec>
```

Lookup a station observation record based by identifier. Instance is a dictionary of all available data, with some special features.

```
>>> station = Weather.Station('KMTN')
```

Grab the datetime instance of the most current observation (if available)

```
>>> station.datetime()
datetime.datetime(2008, 7, 23, 8, 50)
```

Use the instance like a dictionary

```
>>> station.items()
[('icon_url_name','bkn.jpg'),('heat_index_f', None),('weather','Mostly Cloudy'),...]
```

Output all the availalbe observation data in key => value pairs

```
>>> station.pprint()
icon_url_name => 'bkn.jpg'
heat_index_f => None
weather => 'Mostly Cloudy'
...
```

New versions of the module will include `zipcode,city,state,zipcode,etc.` from the LocalizationIntegration data