from City import *   

import csv
import json
import xml.etree.ElementTree as ET
from Readers.DataReaderCache import DataReaderCache

class DataReader:
    def __init__(self):
        self.dataReaderCache = DataReaderCache()
    def LoadCities(self, pathFile):
        pass
    def LoadFlights(self, pathFile):
        pass