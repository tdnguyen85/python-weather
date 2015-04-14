## Localization ##

The newer versions of the module have localization features builtin so you can look up weather stations by city,state, and zipcode. This is all thanks to a bit of data mining to locate the closest zipcode to any given station based on latitude and longitude. The zipcode info was provided by [Zipcode Database Project](http://zips.sourceforge.net/).



### Usage ###

Import the station module

```
from Weather import station
```

Now fetch a Station instance by a city and state pair

```
>>> station.location2station('Baltimore, MD')
<Station KDMH: Baltimore, Inner Harbor, MD>
```


You can also fetch a listing of Stations in any given state

```
>>> station.state2stations('MD').next()
<Station KADW: Camp Springs / Andrews Air Force Base, MD>
```