from urllib import urlretrieve
import os

pjoin = lambda *x: os.path.join(*x)
OBSURL = 'http://www.weather.gov/data/current_obs/all_xml.zip'
BASE = os.path.dirname(__file__)
ZFILE = pjoin(BASE,'all_xml.zip')

def fetch(obsurl=OBSURL):
    """Fetch observation base"""
    urlretrieve(OBSURL,ZFILE)
