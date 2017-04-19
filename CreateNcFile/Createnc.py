import netCDF4 as netcdf_helpers
import MySQLdb
import numpy as np


db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="mstdb",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

listOfUnDiacritizedCharacterQuery = "select * from UnDiacOneHotEncoding"
cur.execute(listOfUnDiacritizedCharacterQuery)
listOfUnDiacritizedCharacter = cur.fetchall()


listOfDiacritizedCharacterQuery = "select * from DiacOneHotEncoding "
cur.execute(listOfDiacritizedCharacterQuery)
listOfDiacritizedCharacter = cur.fetchall()


listOfRecordsInParsedDocumentQuery = "select * from ParsedDocument where SentenceNumber<=500 order by idCharacterNumber asc "
cur.execute(listOfRecordsInParsedDocumentQuery)
listOfRecordsInParsedDocument = cur.fetchall()


numOfseqs = int(listOfRecordsInParsedDocument[-1][5])  # number of sentences
numTimeSteps = len(listOfRecordsInParsedDocument)
inputPatternSize = len(listOfUnDiacritizedCharacter)
numOfLabels = len(listOfDiacritizedCharacter)

#  maxLabelLength = len(listOfDiacritizedCharacter)  # I need to recheck it again
maxTargetStringLength = 5000  # i need to recheck it again
maxSeqTagLength = 800  # i need to recheck it again

# numTargetClasses = len(listOfDiacritizedCharacter)
labels = []
targetStrings = []
seqTags = []
seqLengths = []
targetClasses = []
input = []
# seqTagsdim = maxSeqTagLength * numOfseqs
sentence = ""

flag = True
searchCounter = 0
letterCounterForEachSentence = 0
SEQLengths = []
sentenceNumber = listOfRecordsInParsedDocument[0][5]
# Create Data of SEQ Length Variable
for eachItem in range(0, len(listOfRecordsInParsedDocument)):

    if listOfRecordsInParsedDocument[eachItem][5] == sentenceNumber:
        letterCounterForEachSentence += 1
    else:
        SEQLengths.append(letterCounterForEachSentence)
        sentenceNumber = listOfRecordsInParsedDocument[eachItem][5]
        letterCounterForEachSentence = 1

flag = True
searchCounter = 0

# Create Data of Input Variable
for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    yourLabel = listOfRecordsInParsedDocument[eachItem][2]
    flag = True
    while flag:
        if listOfUnDiacritizedCharacter[searchCounter][1] == yourLabel:
            flag = False
            input.append(listOfUnDiacritizedCharacter[searchCounter][2])
            searchCounter = 0
        else:
            searchCounter += 1


# convert unicode to string
input = [x.encode('ascii') for x in input]

# convert array of string to array of char to be compatible with NETCDF
# you will find strange values, but do not worry, it will exported correctly
input = netcdf_helpers.stringtochar(np.array(input))

str_list = []
for eachItem in range(0, len(input)):
    test = [x for x in input[eachItem] if (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
    str_list.append(test)
purifiedInput = netcdf_helpers.stringtochar(np.array(str_list))

# extract one hot encoding column
labels = [col[2] for col in listOfDiacritizedCharacter]

# convert unicode to string
labels = [x.encode('ascii') for x in labels]

# convert array of string to array of char to be compatible with NETCDF
# you will find strange values, but do not worry, it will exported correctly
labels = netcdf_helpers.stringtochar(np.array(labels))
str_list = []
for eachItem in range(0, len(labels)):
    test = [x for x in labels[eachItem] if (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
    str_list.append(test)
purifiedLabels = netcdf_helpers.stringtochar(np.array(str_list))


flag = True
searchCounter = 0
targetClasses = []

for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    yourLabel = listOfRecordsInParsedDocument[eachItem][3]
    flag = True
    while flag:
        if listOfDiacritizedCharacter[searchCounter][1] == yourLabel:
            flag = False
            targetClasses.append(listOfDiacritizedCharacter[searchCounter][2])
            searchCounter = 0
        else:
            searchCounter += 1

targetClasses = netcdf_helpers.stringtochar(np.array(targetClasses))

str_list = []
for eachItem in range(0, len(targetClasses)):
    test = [x for x in targetClasses[eachItem] if (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
    str_list.append(test)

purifiedTargetClasses = str_list

outputFilename = "NCFile.nc"

# create a new .nc file
dataset = netcdf_helpers.Dataset(outputFilename, 'w', format='NETCDF4')

# create the dimensions
# dataset.createDimension('numSeqs', len(seqLengths))
inputPattSize = len(purifiedInput[0])
maxLabelLength = len(purifiedLabels[0])
dataset.createDimension('numTimesteps', len(input))
dataset.createDimension('inputPattSize', len(purifiedInput[0]))
dataset.createDimension('numLabels', len(labels))
dataset.createDimension('maxLabelLength', len(purifiedLabels[0]))  # you get this value from the array 'labels'
dataset.createDimension('numSeqs', len(SEQLengths))
dataset.createDimension('numTimeSteps', len(purifiedTargetClasses))
dataset.createDimension('width', len(purifiedTargetClasses[0]))

# create the variables

netCDFLabels = dataset.createVariable('netCDFLabels', 'S1', ('numLabels', 'maxLabelLength'))
netCDFLabels[:] = purifiedLabels

netCDFInput = dataset.createVariable('netCDFInput', 'S1', ('numTimesteps', 'inputPattSize'))
netCDFInput[:] = purifiedInput

netCDFSEQLengths = dataset.createVariable('netCDFSEQLengths', 'i4', ('numSeqs'))
netCDFSEQLengths[:] = SEQLengths

netCDFLabels = dataset.createVariable('netCDFLabels', 'i4', ('numTimeSteps', 'width'))
netCDFLabels[:] = purifiedTargetClasses

# write the data to disk
print "writing data to", outputFilename
#file.close()

