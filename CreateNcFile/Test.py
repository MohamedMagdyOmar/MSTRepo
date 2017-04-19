# -*- coding: utf-8 -*-
import netCDF4 as netcdf_helpers
import MySQLdb
import datetime
import numpy as np



db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="mstdb",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()


# listOfWordsAndCorrespondingSentenceNumberQuery = "select * from ListOfWordsAndSentencesInEachDoc order by idword asc"
#
# cur.execute(listOfWordsAndCorrespondingSentenceNumberQuery)
# listOfWordsAndCorrespondingSentenceNumber = cur.fetchall()

listOfParsedDocQuery = "select * from parseddocument order by idCharacterNumber asc"
cur.execute(listOfParsedDocQuery)
listOfParsedDoc= cur.fetchall()

listOfDiacritizedCharacterQuery = "select * from DiacOneHotEncoding"

cur.execute(listOfDiacritizedCharacterQuery)
listOfDiacritizedCharacter = cur.fetchall()

counter = 1
targetStrings = []
seqTags = []
sentence = ""

# for eachItem in range(0, len(listOfParsedDoc)):
#     if int(listOfWordsAndCorrespondingSentenceNumber[eachItem][2]) == counter:
#         word = listOfWordsAndCorrespondingSentenceNumber[eachItem][1].encode('utf-8')
#
#         sentence += word + " "
#     else:
#         counter += 1
#         targetStrings.append(sentence)
#         sentence = ""
#         word = str(listOfWordsAndCorrespondingSentenceNumber[eachItem][1].encode('utf-8'))
#         sentence += word + " "

searchCounter = 0
for eachItem in range(0, len(listOfParsedDoc)):
    if int(listOfParsedDoc[eachItem][5]) == counter:
        yourLabel = listOfParsedDoc[eachItem][3]
        flag = True
        while flag:
            if listOfDiacritizedCharacter[searchCounter][1] == yourLabel:
                flag = False
                targetStrings.append(listOfDiacritizedCharacter[searchCounter][2])
                searchCounter = 0
            else:
                searchCounter += 1

str_out = np.array(['targetStrings'], dtype='object')
str_list = []

targetStrings = (np.array(targetStrings))

for eachItem in range(0, len(targetStrings)):
   test = [x for x in targetStrings[eachItem] if (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
   str_list.append(test)
purifiedTargetStrings = netcdf_helpers.stringtochar(np.array(str_list))

outputFilename = "TestTargetSeq.nc"

# create a new .nc file
dataset = netcdf_helpers.Dataset(outputFilename, 'w', format='NETCDF4')


x = len(targetStrings)
purifiedTargetStrings = netcdf_helpers.stringtochar(np.array(purifiedTargetStrings))
dataset.createDimension('numSeqs', len(purifiedTargetStrings))
dataset.createDimension('maxTargStringLength', len(purifiedTargetStrings[0]))  # you get this value from the array 'labels'
# create the variables

netCDFTargetStrings = dataset.createVariable('netCDFTargetStrings', 'S1', ('numSeqs','maxTargStringLength'))
netCDFTargetStrings[:] = purifiedTargetStrings

x = 1