from urllib import urlretrieve
from threading import Thread
import os

pjoin = lambda *x: os.path.join(*x)
OBSURL = 'http://www.weather.gov/data/current_obs/all_xml.zip'
WURL = 'http://www.weather.gov/data/current_obs/%s.xml'
BASE = os.path.dirname(__file__)
ZFILE = pjoin(BASE,'all_xml.zip')


def fetch():
    """Fetch observation base"""
    urlretrieve(OBSURL,ZFILE)

class Fetch(Thread):
    """Thread fetching"""
    def run(self):
        fetch()