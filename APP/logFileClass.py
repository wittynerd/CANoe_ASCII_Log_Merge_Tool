from datetime import datetime
import os 


class LogHandler:
    def __init__(self, fileList:list) -> None:
        self.fileList = fileList
        pass

    def updateTime(self, fileIndex, offset):
        for lineIndex in range(6, len(self.fileList[fileIndex].lines)):
            splitList = self.fileList[fileIndex].lines[lineIndex].split(" ")
            for i in range(0, len(splitList)):
                a = splitList[i]
                try:
                    k = a.split(".")
                    if(k[0].isnumeric() and k[1].isnumeric()):
                        splitList[i] = "{:.6f}".format(float(splitList[i]) + offset)
                        # print(' '.join(splitList))
                        self.fileList[fileIndex].lines[lineIndex] = ' '.join(splitList)
                        break
                    else:
                        pass
                    pass
                except Exception as e:
                    print(i, e)
                    pass
                pass
        pass

    def sortFilesByTimestamp(self):
        self.fileDict = {}
        for i in range(0, len(self.fileList)):
            self.fileDict[self.fileList[i].startTime] = self.fileList[i]
            pass

        self.fileDict = dict(sorted(self.fileDict.items()))
        # print(self.fileDict)
        self.fileList = list(self.fileDict.values())
        pass

    def mergeFiles(self):
        self.sortFilesByTimestamp()
        mergedFilePath = self.fileList[0].fileDir + '/MergedFile_' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.asc'

        self.mergedFile = open(mergedFilePath, 'w+')
        self.mergedFile.writelines(self.fileList[0].lines[0:-1])

        for i in range(1, len(self.fileList)):
            timeOffset = self.fileList[i].startTime - self.fileList[0].startTime
            self.updateTime(i, timeOffset.seconds)
            self.mergedFile.writelines(self.fileList[i].lines[6:-1])
            pass

        self.mergedFile.writelines(self.fileList[i].lines[-1])
        self.mergedFile.close()
        pass

    pass

class LogFile:
    def __init__(self, filePath) -> None:
        self.fileDir = os.path.dirname(filePath)
        self.file = open(filePath, 'r')
        self.lines = self.file.readlines()
        self.startTime = " ".join(self.lines[4].split(" ")[3:8])
        self.startTime = self.startTime[:-1]
        self.startTime = datetime.strptime(self.startTime, "%b %d %I:%M:%S %p %Y")
        # print(self.startTime)
        # print(self.lines[6:-2])
        pass
    pass


if __name__ == '__main__':
    dirPath = os.getcwd()
    logFiles = []
    entries = os.scandir(dirPath)
    for entry in entries:
        if((entry.name.lower().endswith('.asc') == True) and (entry.name.startswith('MergedFile') == False)):
            filePath = dirPath + f'/{entry.name}'
            logFiles.append(LogFile(filePath))
            pass
        pass

    # print(logFiles)    

    logHandler = LogHandler(logFiles)
    logHandler.mergeFiles()
    pass
else:
    pass