# Weather Observations in Python #
#### Python-weather provides web and Python API access to observed current weather conditions from the [National Oceanic and Atmospheric Administration](http://www.weather.gov/) for around 2000+ locations across the United States and US Territories. Program parses XML feeds from zip file on disk or live from the web. At the API level, it parses observations into python dictionary format with the `Weather.Station` class. Module includes WSGI and CGI applications. ####

## Practical Usage ##

```
>>> import Weather
>>> station = Weather.location2station('baltimore,md')
>>> station
<Weather.Station KDMH: Baltimore, Inner Harbor, MD>
>>> station['weather'],station['temp_f'],station['observation_time']
('Partly Cloudy',69.0,'Last Updated on Aug 23, 4:51 am EDT')
```


## ApiUsage ##
## LocalizationIntegration ##
## WebApplications ##
