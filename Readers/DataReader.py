from City import *   

import csv
import json
import xml.etree.ElementTree as ET
from Readers.GeoLocatorCache import GeoLocatorCache

class DataReader:
    def __init__(self):
        self.geoLocatorCache = GeoLocatorCache()
    def LoadCities(self, pathFile):
        pass
    def LoadFlights(self, pathFile):
        pass