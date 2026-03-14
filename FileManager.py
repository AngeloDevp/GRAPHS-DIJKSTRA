from Readers.DataReaderCSV import *
from Readers.DataReaderJSON import *   
from Readers.DataReaderXML import *

class FileManager:
    def GetReader(self, pathFile):
        if pathFile.endswith('.csv'): return DataReaderCSV()
        elif pathFile.endswith('.json'): return DataReaderJSON()
        elif pathFile.endswith('.xml'): return DataReaderXML()
        else: raise ValueError("Formato de archivo no soportado.")