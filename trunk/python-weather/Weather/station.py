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
    def __init__(self, station, force=False):
        SGMLParser.__init__(self)
        UserDict.__init__(self)
        self.force = force
        self.tag = None
        self.station = station.upper()
        self.update()

    def update(self):
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
        if os.path.isfile(ZFILE) and not self.force:
            zfile = zipfile.ZipFile(ZFILE,'r')
            for name in zfile.namelist():
                if name.endswith('%s.xml'%self.station):
                    SGMLParser.feed(self, zfile.read(name))
                    del zfile
                    break
        else:
            wurl = 'http://www.weather.gov/data/current_obs/%s.xml'
            SGMLParser.feed(self, urlopen(wurl%self.station).read())
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
        Parses and returns the observation datetime object
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
        Returns location string usually in <StationName>,<State> format
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

    def html(self):
        """
        Yields HTML source used in web apps
        """
        titler = lambda x: ' '.join(map(lambda y: y.title(), x.split('_')))
        yield '<html><body><table><tr><td><h2>%s: %s</h2><p><b>%s</b></p></td>'%\
            (self.station,self.location(),self.data.get('weather',''))
        yield '<td><img src="%s"></td></tr>'%self.icon()
        yield '<tr><td><p>Currently: %s</p>'%\
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield '<p>Time of observation: %s</p></td></tr>'%self.datetime()
        yield '</table><hr><table><tr><th><h3>Urls</h3></th><th><h3>Metrics</h3></th><th><h3>Info</h3></th></tr>'
        urls,metrics,info = [],[],[]
        for k,v in self.items():
            if not v: continue
            k = titler(k)
            tr = '<tr><th align="right">%s</th><td>%s</td></tr>'
            if type(v) == type(0.):
                metrics.append(tr%(k,'%.3f'%v))
            elif v.startswith('http'):
                urls.append(tr%(k,'<a href="%s">%s</a>'%(v,filter(None,v.split('/'))[-1])))
            else:
                info.append(tr%(k,v))
        r = ['<td valign="top"><table>%s</table></td>'%''.join(locals()[x]) for x in ('urls','metrics','info')]
        yield '<tr>%s</tr></table>'%''.join(r)

    def __repr__(self):
        return '<Station %s: %s>'%(self.station,self.location())

def stations():
    """
    Returns list of station identifiers with included slicing
    """
    if os.path.isfile(ZFILE):
        for name in zipfile.ZipFile(ZFILE,'r').namelist():
            if name.endswith('.xml') and not \
                (name.endswith('index.xml') or name.endswith('null.xml')):
                yield os.path.split(name)[-1].split('.')[0]
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
    print Station('KMTN')['zipcode']
    print location2station('Baltimore,MD')['city']
    print zip2station(21204)['zipcode']
    print state2stations('MD').next().location()