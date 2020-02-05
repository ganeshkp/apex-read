#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created By: Ganeshkumar patil

Created Date: 05-Feb-2020

Description: Reads REST log file and provides required information of the file.

"""

import itertools, os, sys
SKIP_JUNK_DATA=0

def parseArgs(args):
    if "-h" in args:
        print(__doc__)
        sys.exit(0)
    if "-f" in args:
        # Get the index of the option
        index = args.index("-f")
        FILE_NAME = args[index + 1]
    else:
        print("Alias file name needs to be provided. please check 'python validateAliasFile.py -h' for help")
        exit(1)

    return FILE_NAME

class ApexRead():
    def __init__(self, restFile):
        self.monIdList=[]
        self.aliasList=[]
        self.monIdData={}
        self.monIdPathMap={}
        self.mainDict={}

        self.extractAliasList(restFile)
        self.extractdata(restFile)

    def extractdata(self, restFile):
        try:
            logFile = open(restFile, 'r')
            for line in itertools.islice(logFile, SKIP_JUNK_DATA, None):
                line = line.strip()
                if line.startswith("//"):
                    continue

                # Check for data values
                if line.startswith("#E"):
                    allData = line.split(',')

                    monId = allData[1]
                    if ((allData[6] == ' ') or (allData[7] == ' ')) or \
                            ((allData[6] == "0") and (allData[7] == "0")) or \
                            ((allData[6] == "0.000000") and (allData[7] == "0.000000")):
                        continue
                    elif monId in self.monIdList:
                        data = allData[7]
                        time = allData[3] + "." + allData[4]
                        self.addToApexDataDict(monId, time, data)
            logFile.close()
        except Exception as err:
            print(f"Issue in extracting data:{err}")

    def extractAliasList(self, restFile):
        logFile = open(restFile, 'r')
        for line in itertools.islice(logFile, SKIP_JUNK_DATA, None):
            line = line.strip()
            if line.startswith("//"):
                continue
            # Check for data values
            if line.startswith("#A"):
                allData = line.split(',')
                self.monIdList.append(allData[1])
                self.aliasList.append(allData[2])
                self.monIdPathMap[allData[2]]=allData[1]
        #GET UNIQUE VALUES FROM self.monIdList
        self.monIdList=sorted(list(set(self.monIdList)))
        logFile.close()

    def addToApexDataDict(self, key, timeInfo, val):
        if key in self.monIdData.keys():
            dict1=self.monIdData[key]
            timeList=dict1["time"]
            dataList=dict1["value"]
        else:
            timeList=[]
            dataList=[]

        timeList.append(timeInfo)
        dataList.append(val)
        dict2={}
        dict2["time"]=timeList
        dict2["value"]=dataList
        self.monIdData[key]=dict2

    def getPathList(self, *args):
        finalList=self.aliasList
        sigNamelist=[]

        try:
            if len(args) > 0:
                finalList=[]
                for path in self.aliasList:
                    if args[0] == os.path.basename(path):
                        sigNamelist.append(path)
                if len(args)==1:
                    finalList=sigNamelist
                else:
                    for path in sigNamelist:
                        if self.allSubstringInString(list(args), path)==True:
                            finalList.append(path)
        except Exception as err:
            print(f"Issue in getting path list:{err}")

        #RETURN FINAL LIST OF PATHS
        return finalList

    def getAllEventsFromPath(self, path):
        monId=0
        valueDict={}

        try:
            for key, value in self.monIdPathMap.items():
                if key==path:
                    monId=value
                    break
            for key, value in self.monIdData.items():
                if key==monId:
                    valueDict=value
                    break
        except Exception as err:
            print(f"Issue in reading all events:{err}")
        return valueDict

    def getLatestEventFromPath(self, path):
        monId= 0
        time=0
        value=0
        valueDict = {}

        try:
            for key, value in self.monIdPathMap.items():
                if key == path:
                    monId = value
                    break
            for key, value in self.monIdData.items():
                if key == monId:
                    valueDict = value
                    break

            timeList=valueDict["time"]
            dataList=valueDict["value"]

            time=timeList[len(timeList)-1]
            value=dataList[len(dataList)-1]
        except Exception as err:
            print(f"Issue in reading events:{err}")
        return (time, value)

    def getAllEventsFromMonId(self, monId):
        valueDict = {}
        monId=str(monId)

        try:
            for key, value in self.monIdData.items():
                if key == monId:
                    valueDict = value
                    break
        except Exception as err:
            print(f"Issue in reading all events from monID:{err}")
        return valueDict


    def getLatestEventFromMonId(self, monId):
        monId=str(monId)
        time = 0
        value = 0
        valueDict = {}

        try:
            for key, value in self.monIdData.items():
                if key == monId:
                    valueDict = value
                    break

            timeList = valueDict["time"]
            dataList = valueDict["value"]

            time = timeList[len(timeList) - 1]
            value = dataList[len(dataList) - 1]
        except Exception as err:
            print(f"Issue in reading events:{err}")
        return (time, value)

    def allSubstringInString(self, args, path):
        counter=0
        for substring in args:
            if substring in path:
                counter=counter+1
        if counter==len(args):
            return True
        else:
            return False

