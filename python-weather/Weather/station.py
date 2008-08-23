import os
import zipfile
from sgmllib import SGMLParser
from UserDict import UserDict
from urllib import urlopen
from datetime import datetime
from Weather.data import rows
from Weather.globals import *

class Station(SGMLParser,UserDict):
    """
    SGMLParser and dictionary for NOAA XML weather data by station name

    @param station: The NOAA station identifier to search, eg KMTN
    @param force: Boolean for whether an update should be forced
    """
    def __init__(self, station):
        SGMLParser.__init__(self)
        UserDict.__init__(self)
        self.tag = None
        self.station = station.upper()
        self.update()

    def update(self):
        self.data = {}
        # csv update
        keys = ('latitude','longitude','city','state','zipcode')
        for row in rows():
            if self.station == row[0]:
                UserDict.update(self, dict(zip(keys,row[2:-1])))
                break
        if not self.data:
            raise AttributeError,'Station %s not found'%self.station
        # sgmllib update
        self.reset()
        if os.path.isfile(ZFILE):
            zfile = zipfile.ZipFile(ZFILE,'r')
            for name in zfile.namelist():
                if name.endswith('%s.xml'%self.station):
                    SGMLParser.feed(self, zfile.read(name))
                    del zfile
                    break
        else:
            Fetch().start()
            SGMLParser.feed(self, urlopen(WURL%self.station).read())
        self.close()


    def unknown_starttag(self, tag, attrs):
        self.tag = tag
        self.data[tag] = None

    def handle_data(self, text):
        text = text.rstrip()
        if self.tag and text:
            if text in ('None','NA') or not text:
                value = None
            else:
                try: value = float(text)
                except ValueError:
                    try: value = int(text)
                    except ValueError:
                        value = str(text)
            self.data[self.tag] = value

    def datetime(self):
        """
        Parses and returns the observation datetime object (if possible)
        """
        if 'observation_time_rfc822' in self.data \
           and self.data['observation_time_rfc822']:
            tstr = self.data['observation_time_rfc822']
            tstr = ' '.join(tstr.split(' ')[:-2])
            return datetime.strptime(tstr, '%a, %d %b %Y %H:%M:%S')
        elif 'observation_time' in self.data:
            return datetime.strptime(self.data['observation_time'] \
                +' %s'%datetime.now().year,
                'Last Updated on %b %d, %H:%M %p %Z %Y')
        return ''


    def icon(self):
        """
        Returns URL of weather icon if it exists
        """
        try:
            return self.data['icon_url_base']+self.data['icon_url_name']
        except KeyError:
            return ''

    def location(self):
        """
        Returns location string usually in `StationName,State` format
        """
        try:
            return self.data['location']
        except KeyError:
            return self.data['station_name']

    def pprint(self):
        """
        Pretty print the weather items (for debugging)
        """
        for i in self.items():
            print '%s => %r'%i

    def __repr__(self):
        return '<Weather.Station %s>'%self

    def __str__(self):
        return '%s: %s'%(self.station,self.location())

def stations():
    """
    Returns list of station identifiers with included slicing
    """
    if os.path.isfile(ZFILE):
        zfile = zipfile.ZipFile(ZFILE,'r')
        for name in zfile.namelist():
            if name.endswith('index.xml'):
                for l in zfile.read(name).splitlines():
                    if l.find('station_id')>-1:
                        yield l.split('>')[1].split('<')[0]
                break
    else:
        fetch()
        for s in stations(): yield s


def state2stations(state):
    """
    Translate a state identifier (ie DC) into a list of
    Station instances from that state
    """
    state = state.upper()
    for row in rows():
        if row[5]==state:
            yield Station(row[0])

def zip2station(zipcode):
    """
    Translate a zipcode into Station instance by closest match
    """
    # zipcode of len 5 and oh yea, the best is just that low
    zipcode,best = int(str(zipcode)[:5]),0
    for row in rows():
        # dont ask about the replacements...
        zip = int(row[6].replace('X','5').replace('H','5'))
        if abs(zipcode-zip) < abs(zipcode-best):
            best,result = zip,row[0]
    return Station(result)

def location2station(location):
    """
    Translate `City,State` pairs like 'Washington,DC'
    into Station instance by closest match
    """
    # just shity and state, prease!
    city,state = map(lambda x: x.strip().lower(),
                     location.split(',')[:2])
    for row in rows():
        if row[5].lower() == state:
            if row[4].lower() == city:
                return Station(row[0])

if __name__ == '__main__':
    print Station('KMTN')
    print location2station('Baltimore, MD')
    print zip2station(21204)
    print len([x for x in stations()])