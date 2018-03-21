import yaml

class SettingsDataReader:

    def __init__(self, settingsPath):
        self.__settingsDict__ = self.allSettingsInFileToDict(settingsPath=settingsPath)


    def allSettingsInFileToDict(self, settingsPath):
        with open(settingsPath) as setFile:
            settingsDict = yaml.safe_load(setFile)
        return settingsDict


    def getAllSettings(self):
        return self.__settingsDict__

    def getThresh(self):
        return self.__settingsDict__['thresh']

    # {"thresh": 56507.21864411732, "sampling_rate": 2500000, "signal_time": 5,
     # "series_path": "/home/esraa/PycharmProjects/radioSignalPestDet/BugDetectorProgram/seriesExcamplesThreshTest",
     # "gain": 40}

    def getSamplingRate(self):
        return self.__settingsDict__['sampling_rate']

    def getSignalTime(self):
        return self.__settingsDict__['signal_time']

    def getGain(self):
        return self.__settingsDict__['gain']

