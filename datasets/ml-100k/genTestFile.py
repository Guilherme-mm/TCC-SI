dataFileName = "u-small.data"
testDataFileName = "u-small_test.data"

actorsDict = {}

dataFileLines = None



with open(dataFileName, 'r') as dataFile:
    for line in dataFile:
        linePositions = line.split('\t')

        if not actorsDict.get(linePositions[0], False):
            actorsDict[linePositions[0]] = 0

        actorsDict[linePositions[0]] = actorsDict[linePositions[0]] + 1

for key, value in actorsDict.items():
    if value <= 1:
        del actorsDict[key]


with open(testDataFileName, 'a') as testDataFile:
    removedLines = 0

    for key, value in actorsDict.items():
        with open(dataFileName, 'r') as dataFile:
            dataFileLines = dataFile.readlines()

        with open(dataFileName, 'w') as dataFile:
            if value < 2:
                continue

            actorRemovedOnThisLoop = False

            for line in dataFileLines:
                linePositions = line.split('\t')
                actorId = linePositions[0]

                if actorRemovedOnThisLoop:
                    dataFile.write(line)
                    continue

                if key == actorId and removedLines <= 300:
                    testDataFile.write(line)
                    removedLines = removedLines + 1
                    actorsDict[actorId] = actorsDict[actorId] - 1
                    actorRemovedOnThisLoop = True
                    continue


                dataFile.write(line)
