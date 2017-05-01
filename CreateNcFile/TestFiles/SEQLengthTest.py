# -*- coding: utf-8 -*-
import netCDF4 as netcdf_helpers
import MySQLdb
import datetime
import numpy as np


docName = "الجامع الصحيح المسمى صحيح مسلم.txt"

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="mstdb",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

listOfRecordsInParsedDocument = "select * from ParsedDocument"

cur.execute(listOfRecordsInParsedDocument)
listOfParsedDoc = cur.fetchall()

flag = True
searchCounter = 0
letterCounterForEachSentence = 0
SEQLengths = []
sentenceNumber = listOfParsedDoc[0][5]
# Create Data of Input Variable
for eachItem in range(0, len(listOfParsedDoc)):

    if listOfParsedDoc[eachItem][5] == sentenceNumber:
        letterCounterForEachSentence += 1
    else:
        SEQLengths.append(letterCounterForEachSentence)
        sentenceNumber = listOfParsedDoc[eachItem][5]
        letterCounterForEachSentence = 1


outputFilename = "SEQLengthsNCFile.nc"

# create a new .nc file
dataset = netcdf_helpers.Dataset(outputFilename, 'w', format='NETCDF4')

dataset.createDimension('numSeqs', len(SEQLengths))

netCDFSEQLengths = dataset.createVariable('netCDFSEQLengths', 'i4', ('numSeqs'))
netCDFSEQLengths[:] = SEQLengths
