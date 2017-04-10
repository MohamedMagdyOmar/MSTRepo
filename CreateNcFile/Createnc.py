# -*- coding: utf-8 -*-
import netcdf_helpers
import MySQLdb
import datetime
import numpy as np

docName = "الجامع الصحيح المسمى صحيح مسلم.txt"

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="MSTDB",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

listOfUnDiacritizedCharacterQuery = "select * from UnDiacOneHotEncoding where UnDiacritizedCharacter!='' and " \
                                    "UnDiacritizedCharacter!='.' "

cur.execute(listOfUnDiacritizedCharacterQuery)
listOfUnDiacritizedCharacter = cur.fetchall()

listOfDiacritizedCharacterQuery = "select * from DiacOneHotEncoding where DiacritizedCharacter!='' and " \
                                  "DiacritizedCharacter!='.' "

cur.execute(listOfDiacritizedCharacterQuery)
listOfDiacritizedCharacter = cur.fetchall()

listOfWordsAndCorrespondingSentenceNumberQuery = "select * from ListOfWordsAndSentencesInEachDoc order by idword asc"

cur.execute(listOfWordsAndCorrespondingSentenceNumberQuery)
listOfWordsAndCorrespondingSentenceNumber = cur.fetchall()

listOfRecordsInParsedDocumentQuery = "select * from ParsedDocument where UnDiacritizedCharacter!='.' and  " \
                                     "UnDiacritizedCharacter!='' order by idCharacterNumber asc "

cur.execute(listOfRecordsInParsedDocumentQuery)
listOfRecordsInParsedDocument = cur.fetchall()

test = listOfRecordsInParsedDocument[-1]
numOfseqs = int(listOfRecordsInParsedDocument[-1][5])  # number of sentences
numTimeSteps = len(listOfRecordsInParsedDocument)
inputPatternSize = len(listOfUnDiacritizedCharacter)
numOfLabels = len(listOfDiacritizedCharacter)
maxLabelLength = len(listOfDiacritizedCharacter)  # I need to recheck it again
maxTargetStringLength = 5000  # i need to recheck it again
maxSeqTagLength = 800  # i need to recheck it again

numTargetClasses = len(listOfDiacritizedCharacter)
labels = []
targetStrings = []
seqTags = []
seqLengths = []
targetClasses = []
input = set();
seqTagsdim = maxSeqTagLength * numOfseqs
sentence = ""

for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    yourLabel = (listOfRecordsInParsedDocument[eachItem][3]).encode('ascii', 'ignore')
    labels.append(yourLabel)

counter = 1
for eachItem in range(0, len(listOfWordsAndCorrespondingSentenceNumber)):
    if int(listOfWordsAndCorrespondingSentenceNumber[eachItem][2]) == counter:
        sentence += listOfWordsAndCorrespondingSentenceNumber[eachItem][1] + " "
    else:
        counter += 1
        targetStrings.append(sentence)
        sentence = ""
        sentence += listOfWordsAndCorrespondingSentenceNumber[eachItem][1] + " "

for x in range(1, seqTagsdim):
    seqTags.append(docName);

counter = 1
length = 0
for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    if int(listOfRecordsInParsedDocument[eachItem][5]) == counter:
        length += 1
    else:
        length = length * 403
        counter += 1
        seqLengths.append(length)
        length = 1

print datetime.datetime.now();
flag = True;
searchCounter = 0
targetClasses = set();
for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    yourLabel = listOfRecordsInParsedDocument[eachItem][3]
    flag = True
    while flag:
        if listOfDiacritizedCharacter[searchCounter][1] == yourLabel:
            flag = False
            targetClasses.add(listOfDiacritizedCharacter[searchCounter][2])
            searchCounter = 0
        else:
            searchCounter += 1
'''
queryResult = ""
targetClasses = set();
print datetime.datetime.now();

for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    yourLabel = listOfRecordsInParsedDocument[eachItem][3]

    yourLabel = yourLabel.encode('utf-8', 'ignore')
    yourLabel = '"' + yourLabel +'"'
    testQuery = "select DiacritizedCharacterOneHotEncoding from DiacOneHotEncoding where DiacritizedCharacter=" + yourLabel
    cur.execute(testQuery)
    queryResult = cur.fetchall()
    targetClasses.add(test);

print datetime.datetime.now();
'''

print datetime.datetime.now();

flag = True;
searchCounter = 0

for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    yourLabel = listOfRecordsInParsedDocument[eachItem][2]
    flag = True
    while flag:
        if listOfUnDiacritizedCharacter[searchCounter][1] == yourLabel:
            flag = False
            input.add(listOfUnDiacritizedCharacter[searchCounter][2])
            searchCounter = 0
        else:
            searchCounter += 1

print datetime.datetime.now();


outputFilename = "TestNCFile"

# create a new .nc file
file = netcdf_helpers.NetCDFFile(outputFilename, 'w')

# create the dimensions
netcdf_helpers.createNcDim(file, 'numSeqs', len(seqLengths));
netcdf_helpers.createNcDim(file, 'numTimesteps', len(input))
netcdf_helpers.createNcDim(file, 'inputPattSize', 403)
netcdf_helpers.createNcDim(file, 'numLabels', len(labels));

# create the variables

netcdf_helpers.createNcStrings(file, 'labels', labels, ('numLabels', 'maxLabelLength'), 'labels');
netcdf_helpers.createNcStrings(file, 'targetStrings', targetStrings, ('numSeqs', 'maxTargStringLength'),
                               'target strings');
netcdf_helpers.createNcStrings(file, 'seqTags', seqTags, ('numSeqs', 'maxSeqTagLength'), 'sequence tags')
netcdf_helpers.createNcVar(file, 'seqLengths', seqLengths, 'i', ('numSeqs',), 'sequence lengths')
#netcdf_helpers.createNcStrings(file, 'wordTargetStrings', wordTargetStrings, ('numSeqs', 'maxWordTargStringLength'),
#                               'target strings')
netcdf_helpers.createNcVar(file, 'inputs', input, 'f', ('numTimesteps', 'inputPattSize'), 'input patterns')


# write the data to disk
print "writing data to", outputFilename
file.close()

