import json
from constants import AppConstants
from random import randint

class Thirukural:
    thirukuralData = []
    total = 0

    def __init__(self):
        self.loadData()
    
    def loadData(self):
        jsonData = open(AppConstants.JSON_FILE_NAME)
        self.thirukuralData = json.load(jsonData)["kural"]
        self.total = len(self.thirukuralData)
        jsonData.close()

    def getThirukural(self):
        number = randint(0, self.total)
        return self.thirukuralData[number]

